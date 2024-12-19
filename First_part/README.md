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

#### b)Explain what sim_seconds, sim_insts and host_inst_rate mean.

* sim_seconds is the time that the simulation needs for execution (in seconds)
* sim_insts is the number of instructions that were simulated
* host_inst_rate is the rate of instructions simulated per second

#### c)How many committed instructions do we have? Why isn't this number the same as the statistics that are presented about GEM5?

In the file stats.txt it appears that the number of commited instructions is equal to 5027 (line 27)
```bash
system.cpu_cluster.cpus.committedInsts           5027                       # Number of instructions committed
```
* #### c)How many times was L2 cache accesed? How can we calculate that?.

* In the file stats.txt it appears that the number of L2 acceses is equal to 474 times (lines 840-42)
  ```bash
  system.cpu_cluster.l2.overall_accesses::.cpu_cluster.cpus.inst          327                       # number of overall (read+write) accesses
  system.cpu_cluster.l2.overall_accesses::.cpu_cluster.cpus.data          147                       # number of overall (read+write) accesses
  system.cpu_cluster.l2.overall_accesses::total          474                       # number of overall (read+write) accesses
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






























# REFERENCES

https://www.gem5.org/documentation/general_docs/cpu_models/minor_cpu
https://www.gem5.org/documentation/general_docs/cpu_models/SimpleCPU
