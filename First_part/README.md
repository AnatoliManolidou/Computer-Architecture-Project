# FIRST PART
## First Question: Key characteristics of the system (derived from the starter_se.py file).

* CPU type: Looking at the `starter_se.py` file, in the _line 191_ we see this snippet of code:
  ```python
  parser.add_argument("--cpu", type=str, choices=cpu_types.keys(),
                        default="atomic",
                        help="CPU model to use")
  ```
  This sets the default CPU type as `atomic`. But when we run this command in the shell:
  ```bash
  $ ./build/ARM/gem5.opt -d hello_result configs/example/arm/starter_se.py --cpu="minor" "tests/test-progs/hello/bin/arm/linux/hello"
  ```
  we set the CPU type as `minor`. The shell command dominates the default set in the `starter__se.sy` file.

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
|Cache line size         |_line 15:_ cache_line_size=64|_line 112:_ "cache_line_size": 64|
|Voltage domain for system components         |line 1453: voltage=3.3|_lines 102-07:_ "voltage_domain": {"name":"voltage_domain","eventq_index": 0, "voltage": [3.3],|
|Memory bus type         |_line 1419:_ type=CoherentXBar|_line 30:_ "type": "CoherentXBar"|
|Voltage for the CPU core         |_lines 1223-26:_ [system.cpu_cluster.voltage_domain] type=VoltageDomain eventq_index=0 voltage=1.2|_lines 127-35:_ "cpu_cluster": {"name": "cpu_cluster", "thermal_domain": null, "voltage_domain": {"name": "voltage_domain", "eventq_index": 0, "voltage": [1.2],|
|CPU type         |_line 67:_ type=MinorCPU|_line 429:_ "type": "MinorCPU"|
|Number of memory ranks per channel         |_line 1296:_ ranks_per_channel=2|_line 1771:_ "ranks_per_channel": 2|

We can notice that both the configuration files say that the memory ranks per channel are equal to 2 but this does not allign with the python configuration file. Despite the fact that we did not add any configuration when we run GEM5. We get 2 memory ranks per channel from the configuration files, because of the memory type that we selected `(DDR3_1600_8x8)`.

#### b)Explain what sim_seconds, sim_insts and host_inst_rate mean.

* sim_seconds is the time that the simulation needs for execution (in seconds)
* sim_insts is the number of instructions that were simulated
* host_inst_rate is the rate of instructions simulated per second

#### c)How many committed instructions do we have? Why isn't this number the same as the statistics that are presented about GEM5?

In the file `stats.txt` it appears that the number of commited instructions is equal to 5027 _(line 27)_
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
If we sum all these up, it amounts to `8153` fetched instructions. We can see that this number does not allign with the commited instructions. That is due to the fact that the fetched insructions include discarded instructions that were not ecexuted because of a branch misprediction or a pipeline hazard, cache miss etc.

* #### d)How many times was L2 cache accesed? How can we calculate that?

* In the file stats.txt it appears that the number of L2 acceses is equal to 474 times _(lines 840-42)_
  ```bash
  system.cpu_cluster.l2.overall_accesses::.cpu_cluster.cpus.inst          327                       # number of overall (read+write) accesses
  system.cpu_cluster.l2.overall_accesses::.cpu_cluster.cpus.data          147                       # number of overall (read+write) accesses
  system.cpu_cluster.l2.overall_accesses::total          474                       # number of overall (read+write) accesses
  ```

The number of times that the L2 cache was accessed is equal to the number of times L1 was accessed but a cache miss occured, as regards data. The following snippet is from _line 23_:

  ```bash
  system.cpu_cluster.cpus.branchPred.indirectMisses          147                       # Number of indirect misses.
  ```

## Third Question: In order CPU models.

According to [gem5.org](https://www.gem5.org), we have the following `in order CPU models`:

* **SimpleCPU**\
  This is a CPU model that is well suited for the case where a non detailed model is sufficient. This specific model has been broken into three different new classes.\
  _1.BaseSimpleCPU_\
  The BaseSimpleCPU is the foundational class for other simple CPU models in the gem5 simulator. It manages the essential state and common functions needed for the CPU's operation, such as checking for interrupts, setting up fetch requests, and advancing the program counter (PC). This class is not meant to be used directly; instead, it provides a structure and shared functionality for its derived classes, AtomicSimpleCPU and TimingSimpleCPU.\
  _2.AtomicSimpleCPU_\
  AtomicSimpleCPU is a simple CPU model in gem5 where instructions are executed atomically. This means it estimates the cache access time without stalling, making it useful for simulations where speed is more critical than accuracy.. This model does not simulate pipeline stages or the complexities of modern microarchitecture. It is used primarily for quick, high-level simulations where performance modeling detail is not required.\
  _3.TimingSimpleCPU_\
  TimingSimpleCPU simulates a CPU with more detail than the atomic model, including the timing of instructions and memory accesses. It models pipeline stages, cache access latencies, and other timing-related aspects of CPU behavior. This CPU model is suitable for more accurate simulations where timing details are crucial but without the complexity of fully detailed microarchitectural simulation. It is slower than the atomic model but more realistic.
* **MinorCPU**\
The Minor CPU is an in-order processor model that strictly follows in-order execution, meaning it processes instructions in the exact order they appear.This model has a fixed pipeline but adaptable data structures and execute behaviour. Also, it does not support multithreading.

* #### a) Write a C program that implements the fibonacci sequence and then run simulations with GEM5, using different types of CPU.

Execution times|MinorCPU|TimingSimpleCPU|
|--------------|--------|---------------|
|sim_seconds|0.000036|0.000042|
|host_seconds|0.09|0.09|                      


* #### b) What are your comments about the above results?

  We can see that when we used the `MinorCPU` type the simulation needed less time to execute than when we used `TimingSimpleCPU`. That comes from the fact that `MinorCPU` is based on pipelining and `TimingSimpleCPU` processes instructions sequentially.

* #### c) Run new simulations for the above types of CPUs using different CPU frequency and memory type.

* Changing the frequency of the CPU

  For `MinorCPU` the following command was used:

  ```bash
  ./build/ARM/gem5.opt -d fib_results_minor_freq configs/example/se.py --cpu-type=MinorCPU --cpu-clock=0.7GHz --caches -c tests/test-progs/fibonacci/fib
  ```

  So by changing the frequency to 7GHz, i noticed that the sim_seconds got a higher value (previously it was equal to 0.000036 seconds). Specifically

  ```bash
  sim_seconds                                  0.000053                       # Number of seconds simulated
  ```
  That makes sense since by lowering the clock speed of the CPU, more time is needed in order for the simulation to execute.
  
  For `MinorCPU` the following command was used:

  ```bash
    ./build/ARM/gem5.opt -d fib_results_timing__freq configs/example/se.py --cpu-type=TimingSimpleCPU --cpu-clock=0.7GHz --caches -c tests/test-progs/fibonacci/fib
  ```
  And got these results:
  
  ```bash
  sim_seconds                                  0.000072                       # Number of seconds simulated
  ```
  Again, for the same reason that was mentioned before we can see that more time is needed for the simulation's execution (previously it was equal to 0.000042) seconds.

* Changing the memory type

For this test, i decided to change the mmeory type from `DDR3_1800_8x8` to `DDR4_2400_16x4`.

For `MinorCPU` the following command was used:

```bash
/build/ARM/gem5.opt -d fib_results_minor_mem configs/example/se.py --cpu-type=MinorCPU --mem-type=DDR4_2400_16x4 --caches -c tests/test-progs/fibonacci/fib
```
And got these results:

 ```bash
  sim_seconds                                  0.000035                       # Number of seconds simulated
```
We can notice that there is a sligh improvement about the execution time (only 1000ns).

For `TimingSimpleCPU` i used the following command:

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
