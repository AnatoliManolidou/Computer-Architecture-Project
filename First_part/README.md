<<<<<<< HEAD
# Copyright (c) 2016-2017 ARM Limited
# All rights reserved.
#
# The license below extends only to copyright in the software and shall
# not be construed as granting a license to any other intellectual
# property including but not limited to intellectual property relating
# to a hardware implementation of the functionality of the software
# licensed hereunder.  You may use the software subject to the license
# terms below provided that you ensure that this notice is replicated
# unmodified and in its entirety in all distributions of the software,
# modified or unmodified, in source code or in binary form.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#  Authors:  Andreas Sandberg
#            Chuan Zhu
#            Gabor Dozsa
#

"""This script is the syscall emulation example script from the ARM
Research Starter Kit on System Modeling. More information can be found
at: http://www.arm.com/ResearchEnablement/SystemModeling
"""

from __future__ import print_function
from __future__ import absolute_import

import os
import m5
from m5.util import addToPath
from m5.objects import *
import argparse
import shlex

m5.util.addToPath('../..')

from common import ObjectList
from common import MemConfig
from common.cores.arm import HPI

import devices



# Pre-defined CPU configurations. Each tuple must be ordered as : (cpu_class,
# l1_icache_class, l1_dcache_class, walk_cache_class, l2_Cache_class). Any of
# the cache class may be 'None' if the particular cache is not present.
cpu_types = {
    "atomic" : ( AtomicSimpleCPU, None, None, None, None),
    "minor" : (MinorCPU,
               devices.L1I, devices.L1D,
               devices.WalkCache,
               devices.L2),
    "hpi" : ( HPI.HPI,
              HPI.HPI_ICache, HPI.HPI_DCache,
              HPI.HPI_WalkCache,
              HPI.HPI_L2)
}


class SimpleSeSystem(System):
    '''
    Example system class for syscall emulation mode
    '''

    # Use a fixed cache line size of 64 bytes
    cache_line_size = 64

    def __init__(self, args, **kwargs):
        super(SimpleSeSystem, self).__init__(**kwargs)

        # Setup book keeping to be able to use CpuClusters from the
        # devices module.
        self._clusters = []
        self._num_cpus = 0

        # Create a voltage and clock domain for system components
        self.voltage_domain = VoltageDomain(voltage="3.3V")
        self.clk_domain = SrcClockDomain(clock="1GHz",
                                         voltage_domain=self.voltage_domain)

        # Create the off-chip memory bus.
        self.membus = SystemXBar()

        # Wire up the system port that gem5 uses to load the kernel
        # and to perform debug accesses.
        self.system_port = self.membus.slave


        # Add CPUs to the system. A cluster of CPUs typically have
        # private L1 caches and a shared L2 cache.
        self.cpu_cluster = devices.CpuCluster(self,
                                              args.num_cores,
                                              args.cpu_freq, "1.2V",
                                              *cpu_types[args.cpu])

        # Create a cache hierarchy (unless we are simulating a
        # functional CPU in atomic memory mode) for the CPU cluster
        # and connect it to the shared memory bus.
        if self.cpu_cluster.memoryMode() == "timing":
            self.cpu_cluster.addL1()
            self.cpu_cluster.addL2(self.cpu_cluster.clk_domain)
        self.cpu_cluster.connectMemSide(self.membus)

        # Tell gem5 about the memory mode used by the CPUs we are
        # simulating.
        self.mem_mode = self.cpu_cluster.memoryMode()

    def numCpuClusters(self):
        return len(self._clusters)

    def addCpuCluster(self, cpu_cluster, num_cpus):
        assert cpu_cluster not in self._clusters
        assert num_cpus > 0
        self._clusters.append(cpu_cluster)
        self._num_cpus += num_cpus

    def numCpus(self):
        return self._num_cpus

def get_processes(cmd):
    """Interprets commands to run and returns a list of processes"""

    cwd = os.getcwd()
    multiprocesses = []
    for idx, c in enumerate(cmd):
        argv = shlex.split(c)

        process = Process(pid=100 + idx, cwd=cwd, cmd=argv, executable=argv[0])

        print("info: %d. command and arguments: %s" % (idx + 1, process.cmd))
        multiprocesses.append(process)

    return multiprocesses


def create(args):
    ''' Create and configure the system object. '''

    system = SimpleSeSystem(args)

    # Tell components about the expected physical memory ranges. This
    # is, for example, used by the MemConfig helper to determine where
    # to map DRAMs in the physical address space.
    system.mem_ranges = [ AddrRange(start=0, size=args.mem_size) ]

    # Configure the off-chip memory system.
    MemConfig.config_mem(args, system)

    # Parse the command line and get a list of Processes instances
    # that we can pass to gem5.
    processes = get_processes(args.commands_to_run)
    if len(processes) != args.num_cores:
        print("Error: Cannot map %d command(s) onto %d CPU(s)" %
              (len(processes), args.num_cores))
        sys.exit(1)

    # Assign one workload to each CPU
    for cpu, workload in zip(system.cpu_cluster.cpus, processes):
        cpu.workload = workload

    return system


def main():
    parser = argparse.ArgumentParser(epilog=__doc__)

    parser.add_argument("commands_to_run", metavar="command(s)", nargs='*',
                        help="Command(s) to run")
    parser.add_argument("--cpu", type=str, choices=cpu_types.keys(),
                        default="atomic",
                        help="CPU model to use")
    parser.add_argument("--cpu-freq", type=str, default="1GHz")
    parser.add_argument("--num-cores", type=int, default=1,
                        help="Number of CPU cores")
    parser.add_argument("--mem-type", default="DDR3_1600_8x8",
                        choices=ObjectList.mem_list.get_names(),
                        help = "type of memory to use")
    parser.add_argument("--mem-channels", type=int, default=2,
                        help = "number of memory channels")
    parser.add_argument("--mem-ranks", type=int, default=None,
                        help = "number of memory ranks per channel")
    parser.add_argument("--mem-size", action="store", type=str,
                        default="2GB",
                        help="Specify the physical memory size")

    args = parser.parse_args()

    # Create a single root node for gem5's object hierarchy. There can
    # only exist one root node in the simulator at any given
    # time. Tell gem5 that we want to use syscall emulation mode
    # instead of full system mode.
    root = Root(full_system=False)

    # Populate the root node with a system. A system corresponds to a
    # single node with shared memory.
    root.system = create(args)

    # Instantiate the C++ object hierarchy. After this point,
    # SimObjects can't be instantiated anymore.
    m5.instantiate()

    # Start the simulator. This gives control to the C++ world and
    # starts the simulator. The returned event tells the simulation
    # script why the simulator exited.
    event = m5.simulate()

    # Print the reason for the simulation exit. Some exit codes are
    # requests for service (e.g., checkpoints) from the simulation
    # script. We'll just ignore them here and exit.
    print(event.getCause(), " @ ", m5.curTick())
    sys.exit(event.getCode())


if __name__ == "__m5_main__":
    main()
=======
# FIRST PART
## First Question: Key characteristics of the system (derived from the starter_se.py file).

* CPU type: Looking at the starter_se.py file, in the line _191_ we see this snippet of code:
  ```python
  parser.add_argument("--cpu", type=str, choices=cpu_types.keys(),
                        default="atomic",
                        help="CPU model to use")
  ```
  This sets the default CPU type as **atomic**. But when we run this command in the shell:
  ```bash
  $ ./build/ARM/gem5.opt -d hello_result configs/example/arm/starter_se.py --cpu="minor" "tests/test-progs/hello/bin/arm/linux/hello"
  ```
  we set the CPU type as **minor**. The shell command dominates the default set in the starter__se.sy file.

* CPU frequency: 1GHz 
* Physical memory size: 2Gb
* Number of cores: 1
* Number of memory channels: 2
* Number of memory ranks per channel: None
* Type of memory: DDR3_1600_8x8
* Caches:\
   L1 cache: devided into L1I (instruction cache) and L1D (data cache)\
   Walk cache\
   L2 cache\
   Cache line size: 64 bytes
* Voltage domain for system components: 3.3V
* Clock domain for system components: 1GHz
* Voltage for the CPU core: 1.2V
* Memory bus type: SystemXBar

## Second Question: Key characteristics of the system (derived from the stats.txt, config.ini and config.json files).

#### a)Verify the results from _First Question_ using the files stats.txt, config.ini and config.json.

For all the above charecteristics i managed to verify the followings:

Characteristic|config.ini|config.json|
|---------|----------|-----------|
|Cache line size         |line 15: cache_line_size=64|line 112: "cache_line_size": 64|
|Voltage domain for system components         |line 1453: voltage=3.3|lines 102-07: "voltage_domain": {"name":"voltage_domain","eventq_index": 0, "voltage": [3.3],|
|Memory bus type         |line 1419: type=CoherentXBar|line 30: "type": "CoherentXBar"|
|Voltage for the CPU core         |lines 1223-26: [system.cpu_cluster.voltage_domain] type=VoltageDomain eventq_index=0 voltage=1.2|lines 127-35: "cpu_cluster": {"name": "cpu_cluster", "thermal_domain": null, "voltage_domain": {"name": "voltage_domain", "eventq_index": 0, "voltage": [1.2],|
|CPU type         |line 67: type=MinorCPU|line 429: "type": "MinorCPU"|
|Number of memory ranks per channel         |line 1296: ranks_per_channel=2|line 1771: "ranks_per_channel": 2|

  We can notice that both the configuration files say that the memory ranks per channel are equal to 2 but this does not allign with the python configuration file. Despite the fact that we did not add any configuration when we run GEM5 in the command. We get 2 memory ranks per channel from the configuration files, because of the memory type that we selected (DDR3_1600_8x8).

#### b)Explain what sim_seconds, sim_insts and host_inst_rate mean.

* sim_seconds is the time that the simulation needs for execution (in seconds)
* sim_insts is the number of instructions that were simulated
* host_inst_rate is the rate of instructions simulated per second

#### c)How many committed instructions do we have? Why isn't this number the same as the statistics that are presented about GEM5?

In the file stats.txt it appears that the number of commited instructions is equal to 5027 (line 27)
```bash
system.cpu_cluster.cpus.committedInsts           5027                       # Number of instructions committed
```
  Commited instructions are the instructions that were executed and retred successfully by the CPU. Aside from the commited ones we also have fetched instructions:

```bash
  system.cpu_cluster.cpus.fetch2.amo_instructions            0                       # Number of memory atomic instructions   successfully decoded
  system.cpu_cluster.cpus.fetch2.fp_instructions            0                       # Number of floating point instructions   successfully decoded
  system.cpu_cluster.cpus.fetch2.int_instructions         5495                       # Number of integer instructions   successfully decoded
  system.cpu_cluster.cpus.fetch2.load_instructions         1830                       # Number of memory load instructions   successfully decoded
  system.cpu_cluster.cpus.fetch2.store_instructions          828                       # Number of memory store   instructions successfully decoded
  system.cpu_cluster.cpus.fetch2.vec_instructions            0                       # Number of SIMD instructions       successfully decoded
```
  If we sum all these up, it amounts to 8153 fetched instructions. We can see that this number does not allign with the commited instructions. That is due to the fact that the fetched insructions include discarded instructions that were not ecexuted because of a branch misprediction or a pipeline hazard, cache miss etc.

* #### d)How many times was L2 cache accesed? How can we calculate that?

* In the file stats.txt it appears that the number of L2 acceses is equal to 474 times (lines 840-42)
  ```bash
  system.cpu_cluster.l2.overall_accesses::.cpu_cluster.cpus.inst          327                       # number of overall (read+write) accesses
  system.cpu_cluster.l2.overall_accesses::.cpu_cluster.cpus.data          147                       # number of overall (read+write) accesses
  system.cpu_cluster.l2.overall_accesses::total          474                       # number of overall (read+write) accesses
  ```

  The number of times that the L2 cache was accessed is equal to the number of times L1 was accessed but a cache miss occured, as regards data. The followin snippet is from line 23:

  ```bash
  system.cpu_cluster.cpus.branchPred.indirectMisses          147                       # Number of indirect misses.
  ```

## Third Question: In order CPU models.

According to [gem5.org](https://www.gem5.org), we have the following in order CPU models:

* **SimpleCPU**\
  This is a CPU model that is well suited for the case where a non detailed model is sufficient. This specific model has been broken into three different new classes.\
  _1.BaseSimpleCPU_\
  The BaseSimpleCPU can not be run on its own. You must use one of the classes that inherits from BaseSimpleCPU, either AtomicSimpleCPU or TimingSimpleCPU.\
  _2.AtomicSimpleCPU_\
  AtomicSimpleCPU is a simple CPU model in gem5 where instructions are executed atomically, meaning each instruction is completed in a single cycle. This model does not simulate pipeline stages or the complexities of modern microarchitecture. It is used primarily for quick, high-level simulations where performance modeling detail is not required.\
  _3.TimingSimpleCPU_\
  TimingSimpleCPU simulates a CPU with more detail than the atomic model, including the timing of instructions and memory accesses. It models pipeline stages, cache access latencies, and other timing-related aspects of CPU behavior. This CPU model is suitable for more accurate simulations where timing details are crucial but without the complexity of fully detailed microarchitectural simulation. It is slower than the atomic model but more realistic.
* **MinorCPU**\
This model has a fixed pipeline but adaptable data structures and execute behaviour. Also, it does not support multithreading 

* #### a)Wrte a C program that implements the fibonacci sequence and then run simulations with GEM5, using different types of CPU.




Execution times|MinorCPU|TimingSimpleCPU|
|--------------|--------|---------------|
|sim_seconds|0.000036|0.000042|
|host_seconds|0.09|0.09|                      



b)What are your comments about the above results?

  We can see that when we used the MinorCPU type the simulation needed less time to execute than when we used TimingSimpleCPU. That comes from the fact that MinorCPU is based on pipelining and TimingSimpleCPU processes instructions sequentially.

b)Run new simulations for the above types of CPUs using different CPU frequency and memory type.

* Changing the frequency of the CPU

  For MinorCPU i used the following command:

  ```bash
  ./build/ARM/gem5.opt -d fib_results_minor_freq configs/example/se.py --cpu-type=MinorCPU --cpu-clock=0.7GHz --caches -c tests/test-progs/fibonacci/fib
  ```

  So by changing the frequency into 7GHz, i noticed that the sim_seconds got a higher value (previously it was equal to 0.000036 seconds). Specifically

  ```bash
  sim_seconds                                  0.000053                       # Number of seconds simulated
  ```
  That makes sense since by lowering the clock speed of the CPU, more time is needed in order for the simulation to execute.
  
  For MinorCPU i used the following command:

  ```bash
    ./build/ARM/gem5.opt -d fib_results_timing__freq configs/example/se.py --cpu-type=TimingSimpleCPU --cpu-clock=0.7GHz --caches -c tests/test-progs/fibonacci/fib
  ```
  And got these results:
  
  ```bash
  sim_seconds                                  0.000072                       # Number of seconds simulated
  ```
  Again, for the same reason that was mentioned before we can see that more time is needed for the simulation's execution (previously it was equal to 0.000042) seconds.

* Changing the memory type

For this test, i decided to change the mmeory type from DDR3_1800_8x8 to DDR4_2400_16x4.

For MinorCPU i used the following command:

```bash
/build/ARM/gem5.opt -d fib_results_minor_mem configs/example/se.py --cpu-type=MinorCPU --mem-type=DDR4_2400_16x4 --caches -c tests/test-progs/fibonacci/fib
```
And got these results:

 ```bash
  sim_seconds                                  0.000035                       # Number of seconds simulated
```
We can notice that there is a sligh improvement about the execution time (only 1000ns).

For TimingSimpleCPU i used the following command:

```bash
  /build/ARM/gem5.opt -d fib_results_timing_mem configs/example/se.py --cpu-type=TimingSimpleCPU --mem-type=DDR4_2400_16x4 --caches -c tests/test-progs/fibonacci/fib
```
And got these results:

```bash
  sim_seconds                                  0.000042                       # Number of seconds simulated
```
For this type of CPU, we can notice that there is no change in the execution time.















# REFERENCES

https://www.gem5.org/documentation/general_docs/cpu_models/minor_cpu
https://www.gem5.org/documentation/general_docs/cpu_models/SimpleCPU
>>>>>>> 5d01f5f1695583e7130d899674a5d38f92e31708
