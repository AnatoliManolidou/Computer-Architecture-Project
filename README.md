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

#### a) Write a C program that implements the fibonacci sequence and then run simulations with GEM5, using different types of CPU.

Execution times|MinorCPU|TimingSimpleCPU|
|--------------|--------|---------------|
|sim_seconds|0.000036|0.000042|
|host_seconds|0.09|0.09|                      

#### b) What are your comments about the above results?

  We can see that when we used the `MinorCPU` type the simulation needed less time to execute than when we used `TimingSimpleCPU`. That comes from the fact that `MinorCPU` is based on pipelining and `TimingSimpleCPU` processes instructions sequentially.

#### c) Run new simulations for the above types of CPUs using different CPU frequency and memory type.

* Changing the frequency of the CPU

  For `MinorCPU` the following command was used:

  ```bash
  ./build/ARM/gem5.opt -d fib_results_minor_freq configs/example/se.py --cpu-type=MinorCPU --cpu-clock=0.7GHz --caches -c tests/test-progs/fibonacci/fib
  ```

  So by changing the frequency to 0.7GHz, i noticed that the sim_seconds got a higher value (previously it was equal to 0.000036 seconds). Specifically

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

For this test, i decided to change the memory type from `DDR3_1800_8x8` to `DDR4_2400_16x4`.

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

[GEM5 MinorCPU](https://www.gem5.org/documentation/general_docs/cpu_models/minor_cpu)\
[GEM5 SimpleCPU](https://www.gem5.org/documentation/general_docs/cpu_models/SimpleCPU)\
[GEM5 Statistics overview](https://www.gem5.org/documentation/learning_gem5/part1/gem5_stats/)


# SECOND PART

## First step. Execute SPEC CPU2006 Benchmarks on GEM5

### First question: What informations can you get about the memory system of the CPU that we are simulating?

From the `config.ini` file: 

|Size characteristics|config.ini|
|---------------|----------------|
|L1D|`line 155/line 179:` [system.cpu.dcache]/size=65536|
|L1I|`line 789/line 813:` [system.cpu.icache]/size=32768|
|L2|`line 994/line 1018:` [system.l2]/size=2097152|
|Cache line|`line 155:`  "cache_line_size": 64|

### Second Question: Benchmark analysis

These are the commands that were used:

```shell

$ ./build/ARM/gem5.opt -d spec_results/specbzip configs/example/se.py --cpu-type=MinorCPU --caches --l2cache -c spec_cpu2006/401.bzip2/src/specbzip -o "spec_cpu2006/401.bzip2/data/input.program 10" -I 100000000

$ ./build/ARM/gem5.opt -d spec_results/specmcf configs/example/se.py --cpu-type=MinorCPU --caches --l2cache -c spec_cpu2006/429.mcf/src/specmcf -o "spec_cpu2006/429.mcf/data/inp.in" -I 100000000

$ ./build/ARM/gem5.opt -d spec_results/spechmmer configs/example/se.py --cpu-type=MinorCPU --caches --l2cache -c spec_cpu2006/456.hmmer/src/spechmmer -o "--fixed 0 --mean 325 --num 45000 --sd 200 --seed 0 spec_cpu2006/456.hmmer/data/bombesin.hmm" -I 100000000

$ ./build/ARM/gem5.opt -d spec_results/specsjeng configs/example/se.py --cpu-type=MinorCPU --caches --l2cache -c spec_cpu2006/458.sjeng/src/specsjeng -o "spec_cpu2006/458.sjeng/data/test.txt" -I 100000000

$ ./build/ARM/gem5.opt -d spec_results/speclibm configs/example/se.py --cpu-type=MinorCPU --caches --l2cache -c spec_cpu2006/470.lbm/src/speclibm -o "20 spec_cpu2006/470.lbm/data/lbm.in 0 1 spec_cpu2006/470.lbm/data/100_100_130_cf_a.of" -I 100000000

```
And these are the results that were extracted from the `stats.txt` file of each benchmark:

<a id="results"></a>

 | Characteristics | specbzip | specmcf | spechmmer | specsjeng | speclibm |
 | ------ | ------ | ------ | ------ | ------ | ------ |
 | Execution time |`line 12:` 0.083982|`line12:` 0.064955 |`line 12:` 0.05936 |`line 12:` 0.513528 |`line 12:` 0.174671 |
 | CPI |`line 29:` 1.679650|`line 29:` 1.299095|`line 29:` 1.187917 |`line 29:` 10.270554 |`line 29:` 3.493415 |
 | L1 Instruction cache miss rates|`line 780:` 0.000077|`line 781:` 0.023612 |`line 739:` 0.000221 |`line 779:` 0.000020 |`line 770:` 0.000094 |
 | L1 Data cache miss rates |`line 867:` 0.014798|`line 868:` 0.002107 |`line 827:` 0.001637 |`line 865:` 0.121831 |`line 856:` 0.060972 |
 | L2 cache miss rates |`line 320:` 0.282163|`line 320:` 0.055046 |`line 318:` 0.077760 |`line 320:` 0.999972 |`line 320:` 0.999944 |

Below there are 5 different graphs, each representing one of the characteristics that were just mentioned, over all of the 5 benchmarks. This [python code](https://github.com/AnatoliManolidou/Computer-Architecture-Project/blob/main/Second_part/Python_code/graphs_question2.py) was used for generating the graphs while using the [stats.txt files](https://github.com/AnatoliManolidou/Computer-Architecture-Project/tree/main/Second_part/Benchmarks_results) from the benchmarks.

![execution_time](https://github.com/user-attachments/assets/fec541e8-908a-44b4-a2ba-5fc09b668bf0)
![cpi](https://github.com/user-attachments/assets/c1647cad-cf51-460b-b1b6-c07da9d69d41)
![li_miss_rate](https://github.com/user-attachments/assets/e34c820e-9776-4e24-9e3b-4dff0cb6a2aa)
![ld_miss_rate](https://github.com/user-attachments/assets/143fb88e-58c4-44aa-a88d-cabf74134db2)
![l2_miss_rate](https://github.com/user-attachments/assets/a93ba7e8-96b4-450d-aeb6-2c317d38dda0)


### Third question: Effect of Changing CPU Frequency

After running the benchmarks for the two new frequency configurations, here are the results related to the clock from the `stats.txt` files. These snippets were derived from the `specmcf` benchmark, where the clock values were the same across all benchmarks.

* **Default CPU clock frequency**:

```bash
system.cpu_clk_domain.clock                       500                       # Clock period in ticks
```
```bash
system.clk_domain.clock                          1000                       # Clock period in ticks
```

* **Setting the CPU clock frequency at 1GHz**:

#### Commands:

```shell

$ ./build/ARM/gem5.opt -d spec_results2/specbzip configs/example/se.py --cpu-type=MinorCPU --cpu-clock=1GHz --caches --l2cache -c spec_cpu2006/401.bzip2/src/specbzip -o "spec_cpu2006/401.bzip2/data/input.program 10" -I 100000000

$ ./build/ARM/gem5.opt -d spec_results2/specmcf configs/example/se.py --cpu-type=MinorCPU --cpu-clock=1GHz --caches --l2cache -c spec_cpu2006/429.mcf/src/specmcf -o "spec_cpu2006/429.mcf/data/inp.in" -I 100000000

$ ./build/ARM/gem5.opt -d spec_results2/spechmmer configs/example/se.py --cpu-type=MinorCPU --cpu-clock=1GHz --caches --l2cache -c spec_cpu2006/456.hmmer/src/spechmmer -o "--fixed 0 --mean 325 --num 45000 --sd 200 --seed 0 spec_cpu2006/456.hmmer/data/bombesin.hmm" -I 100000000

$ ./build/ARM/gem5.opt -d spec_results2/specsjeng configs/example/se.py --cpu-type=MinorCPU --cpu-clock=1GHz --caches --l2cache -c spec_cpu2006/458.sjeng/src/specsjeng -o "spec_cpu2006/458.sjeng/data/test.txt" -I 100000000

$ ./build/ARM/gem5.opt -d spec_results2/speclibm configs/example/se.py --cpu-type=MinorCPU --cpu-clock=1GHz --caches --l2cache -c spec_cpu2006/470.lbm/src/speclibm -o "20 spec_cpu2006/470.lbm/data/lbm.in 0 1 spec_cpu2006/470.lbm/data/100_100_130_cf_a.of" -I 100000000
```

#### Results:
```bash
system.cpu_clk_domain.clock                      1000                       # Clock period in ticks
```
```bash
system.clk_domain.clock                          1000                       # Clock period in ticks
```
* **Setting the CPU clock frequency at 3GHz**:

#### Commands:

```shell

$ ./build/ARM/gem5.opt -d spec_results3/specbzip configs/example/se.py --cpu-type=MinorCPU --cpu-clock=3GHz --caches --l2cache -c spec_cpu2006/401.bzip2/src/specbzip -o "spec_cpu2006/401.bzip2/data/input.program 10" -I 100000000

$ ./build/ARM/gem5.opt -d spec_results3/specmcf configs/example/se.py --cpu-type=MinorCPU --cpu-clock=3GHz --caches --l2cache -c spec_cpu2006/429.mcf/src/specmcf -o "spec_cpu2006/429.mcf/data/inp.in" -I 100000000

$ ./build/ARM/gem5.opt -d spec_results3/spechmmer configs/example/se.py --cpu-type=MinorCPU --cpu-clock=3GHz --caches --l2cache -c spec_cpu2006/456.hmmer/src/spechmmer -o "--fixed 0 --mean 325 --num 45000 --sd 200 --seed 0 spec_cpu2006/456.hmmer/data/bombesin.hmm" -I 100000000

$ ./build/ARM/gem5.opt -d spec_results3/specsjeng configs/example/se.py --cpu-type=MinorCPU --cpu-clock=3GHz --caches --l2cache -c spec_cpu2006/458.sjeng/src/specsjeng -o "spec_cpu2006/458.sjeng/data/test.txt" -I 100000000

$ ./build/ARM/gem5.opt -d spec_results3/speclibm configs/example/se.py --cpu-type=MinorCPU --cpu-clock=3GHz --caches --l2cache -c spec_cpu2006/470.lbm/src/speclibm -o "20 spec_cpu2006/470.lbm/data/lbm.in 0 1 spec_cpu2006/470.lbm/data/100_100_130_cf_a.of" -I 100000000
```

#### Results:
```bash
system.cpu_clk_domain.clock                       333                       # Clock period in ticks
```
```bash
system.clk_domain.clock                          1000                       # Clock period in ticks
```
### Final conclusions:

* Default frequency:
The CPU is clocked at 2GHz. This is because the clock period is 500 ticks, and using the formula $\frac{10^{12}}{500}$ gives us 2GHz. The system overall is clocked at 1GHz, as the clock period is 1000 ticks, and $\frac{10^{12}}{1000}$ gives us 1GHz.

* 1GHz:
The CPU is clocked at 1GHz. This is because the clock period is 1000 ticks, and $\frac{10^{12}}{1000}$

​gives us 1GHz. The system overall is also clocked at 1GHz, with the same clock period of 1000 ticks.

* 3GHz:
The CPU is clocked at 3GHz, as the clock period is 333 ticks, and $\frac{10^{12}}{333}$
 gives us 3GHz. The system overall is still clocked at 1GHz, with the same clock period of 1000 ticks..

From all the above, we can see that when we change the `--cpu-clock=` configuration only the CPU's frequency changes while the overall system's frequency remains the same. This happens because GEM5 models systems with independent clock domains, meaning different components can run at different clock frequencies. Thus, The `--cpu-clock=` parameter explicitly sets only the frequency for the CPU clock domain `(cpu_clk_domain)`.

Upon inspecting the `config.json` file, we can see that the `clk_domain` and `cpu_clk_domain` are completely separate. Here are the relevant snippets from `config.json`:

`lines 114-118`

```bash
"clk_domain": {
            "name": "clk_domain", 
            "clock": [
                1000
            ],
```

and `lines 160-164`

```bash
"cpu_clk_domain": {
            "name": "cpu_clk_domain", 
            "clock": [
                1000
            ],
```
Now, if we add one more processor it would more likely inherit the `cpu_clk_domain`, since this new CPU operates with a seperate clock that is independed from the rest of the system. Finally, using the [pyhton code](https://github.com/AnatoliManolidou/Computer-Architecture-Project/blob/main/Second_part/Python_code/Part2_Graphs2.py) that was used before (now modified to extract only the graph for execution time) the following graphs were obtained:
![execution_time_1GHz](https://github.com/user-attachments/assets/fa803096-e3f1-4b4b-9cf7-0a593e924aa2)
![execution_time_3GHz](https://github.com/user-attachments/assets/8db07496-97ab-4749-8442-98d31d7ff7d7)

When comparing these graphs to the one for the default frequency, we do not see perfect scaling. This is because execution time does not depend solely on the CPU's frequency. There are many other factors influencing execution time, and changing just one parameter (like the CPU frequency) will not result in a perfectly linear reduction in execution time.

### Fourth Question. Changing the memory configuration.

For changing the memory configuration, the benchmark `speclibm` was chosen, and the following command was used:

```bash
./build/ARM/gem5.opt -d spec_results_memory/speclibm configs/example/se.py --cpu-type=MinorCPU --cpu-clock=1GHz --mem-type=DDR3_2133_8x8 --caches --l2cache -c spec_cpu2006/470.lbm/src/speclibm -o '20 spec_cpu2006/470.lbm/data/lbm.in 0 1 spec_cpu2006/470.lbm/data/100_100_130_cf_a.of' -I 100000000
```
Now the memory type is set to `DDR3_2133_8x8` {`DDR3_2113_x64` was not listed so `DDR3_2133_8x8` was used}. From `stats.txt` we have the following: 

```bash
sim_seconds                                  0.257413                       # Number of seconds simulated
```

while for `DDR3_1600_x64` we had:

```bash
sim_seconds                                  0.174671                       # Number of seconds simulated
```

# STEP 2. Trying to achieve maximum efficiency for the system in each benchmark 

After taking into consideration these [results](#results) from step 1, for each characteristic the following conclusions were made:

* Cache Line Size
The effectiveness of the cache line size depends on spatial locality. For benchmarks like `sjeng` and `speclibm`, higher L2 miss rates might indicate poor spatial locality. Despote that, i increased the cache line size in all of the benchmarks.

* L2 Cache Size
The highest L2 cache miss rates are in `speclibm` (0.999944) and `specsjeng` (0.999972), indicating severe L2 capacity issues. Other benchmarks like `specbzip`, `specmcf`, and `spechmmer` show manageable miss rates (< 0.3). Thus, an increase in L2 cache size significantly for `specsjeng` and `speclibm` was tested, as these benchmarks heavily rely on L2. An increase was also tested in the `spechmmer` and `specbzip`.

* L2 Cache Associativity
As mentioned above, the `speclibm` and `specsjeng` showed a high miss rate for the L2 cache, so an increase in its associativity was also tested. Moreover, an increase in the associativity of the L2 cache was tested for the `spehmmer` and `specbzip` benchmarks aswell.

* L1 Data Cache Size
Again, `specsjeng` (0.121831) and `speclibm` (0.060972) show relatively higher L1 data cache miss rates compared to others. Other benchmarks have very low miss rates, indicating sufficient L1 data cache size. So an increase in L1 data cache size specifically for `specsjeng` and `speclibm` is much needed. Also, i tested an increase in the size of the L1 cache in `spechmmer` and `specbzip` aswell.

* L1 Data Cache Associativity
Moderate miss rates for `specsjeng` and `speclibm` suggest potential conflict misses. Thus, an increase in associativity for L1 data cache for `specsjeng` and `speclibm` was tested. Also, i tested an increase in the associativity of the L1 cache in `spechmmer` and `specbzip` aswell.

* L1 Instruction Cache Size
The only benchmark that showed a high miss rate for the L1 instruction cache, was the `specmcf`. So an increase in the size of the l1 instruction cache was tested.

* L1 Instruction Cache Associativity
As mentioned above, the `specmcf` showed a high miss rate for the L1 instruction cache, so an increase in its associativity was also tested.

Lastly, this [python code](https://github.com/AnatoliManolidou/Computer-Architecture-Project/blob/main/Second_part/Python_code/optimizations_graph.py) was used in order to obtain all of the following graphs.

## SPECLIBM

From the [chart](#results), it is evident that the miss rate of the L1 data cache is quite high. To address this, in the first test, I doubled both the associativity and size of the L1 data cache. Similarly, the L2 cache also exhibited a high miss rate, so in the second test, I doubled the size and associativity of the L2 cache while retaining the L1D configurations from the first test. For the third test, I used the configurations from the first test but doubled the cache line size and associativity of the L2 cache. In the fourth test, I retained the configurations from the third test and further doubled the cache line size. Finally, in the fifth test, I evaluated the effect of increasing only the cache line size (doubling the initial size).

The commands used are as follows:

```bash
$ ./build/ARM/gem5.opt -d spec_results_opt/speclibm/1 configs/example/se.py --cpu-type=MinorCPU --caches --l2cache --l1d_size=128kB --l1i_size=32kB --l2_size=2MB --l1i_assoc=2 --l1d_assoc=4 --l2_assoc=8 --cacheline_size=64 --cpu-clock=1GHz -c spec_cpu2006/470.lbm/src/speclibm -o "20 spec_cpu2006/470.lbm/data/lbm.in 0 1 spec_cpu2006/470.lbm/data/100_100_130_cf_a.of" -I 100000000  

$ ./build/ARM/gem5.opt -d spec_results_opt/speclibm/2 configs/example/se.py --cpu-type=MinorCPU --caches --l2cache --l1d_size=128kB --l1i_size=32kB --l2_size=4MB --l1i_assoc=2 --l1d_assoc=4 --l2_assoc=16 --cacheline_size=64 --cpu-clock=1GHz -c spec_cpu2006/470.lbm/src/speclibm -o "20 spec_cpu2006/470.lbm/data/lbm.in 0 1 spec_cpu2006/470.lbm/data/100_100_130_cf_a.of" -I 100000000

$ ./build/ARM/gem5.opt -d spec_results_opt/speclibm/3 configs/example/se.py --cpu-type=MinorCPU --caches --l2cache --l1d_size=128kB --l1i_size=32kB --l2_size=2MB --l1i_assoc=2 --l1d_assoc=4 --l2_assoc=16 --cacheline_size=128 --cpu-clock=1GHz -c spec_cpu2006/470.lbm/src/speclibm -o "20 spec_cpu2006/470.lbm/data/lbm.in 0 1 spec_cpu2006/470.lbm/data/100_100_130_cf_a.of" -I 100000000 

$ ./build/ARM/gem5.opt -d spec_results_opt/speclibm/4 configs/example/se.py --cpu-type=MinorCPU --caches --l2cache --l1d_size=128kB --l1i_size=32kB --l2_size=4MB --l1i_assoc=2 --l1d_assoc=4 --l2_assoc=16 --cacheline_size=128 --cpu-clock=1GHz -c spec_cpu2006/470.lbm/src/speclibm -o "20 spec_cpu2006/470.lbm/data/lbm.in 0 1 spec_cpu2006/470.lbm/data/100_100_130_cf_a.of" -I 100000000 

$ ./build/ARM/gem5.opt -d spec_results_opt/speclibm/5 configs/example/se.py --cpu-type=MinorCPU --caches --l2cache --l1d_size=64kB --l1i_size=32kB --l2_size=2MB --l1i_assoc=2 --l1d_assoc=2 --l2_assoc=8 --cacheline_size=128 --cpu-clock=1GHz -c spec_cpu2006/470.lbm/src/speclibm -o "20 spec_cpu2006/470.lbm/data/lbm.in 0 1 spec_cpu2006/470.lbm/data/100_100_130_cf_a.of" -I 100000000
```
![opt_speclibm](https://github.com/user-attachments/assets/fa9b6993-3a43-412f-a2eb-0a32c63ee1dd)

## SPECMCF

From the [chart](#results), it is apparent that the L1 instruction cache has a high miss rate. To mitigate this, in the first test, I doubled both the size and associativity of the L1 instruction cache. In the second test, I quadrupled these parameters. For the third test, I reverted the L1I size to 64kB and its associativity to 4, but doubled the cache line size instead.

The commands used are as follows:

```bash
$ ./build/ARM/gem5.opt -d spec_results_opt/specmcf/1 configs/example/se.py --cpu-type=MinorCPU --caches --l2cache --l1d_size=64kB --l1i_size=64kB --l2_size=2MB --l1i_assoc=4 --l1d_assoc=2 --l2_assoc=8 --cacheline_size=64 --cpu-clock=1GHz -c spec_cpu2006/429.mcf/src/specmcf -o "spec_cpu2006/429.mcf/data/inp.in" -I 100000000 

$ ./build/ARM/gem5.opt -d spec_results_opt/specmcf/2 configs/example/se.py --cpu-type=MinorCPU --caches --l2cache --l1d_size=64kB --l1i_size=128kB --l2_size=2MB --l1i_assoc=8 --l1d_assoc=2 --l2_assoc=8 --cacheline_size=64 --cpu-clock=1GHz -c spec_cpu2006/429.mcf/src/specmcf -o "spec_cpu2006/429.mcf/data/inp.in" -I 100000000

$ ./build/ARM/gem5.opt -d spec_results_opt/specmcf/3 configs/example/se.py --cpu-type=MinorCPU --caches --l2cache --l1d_size=64kB --l1i_size=64kB --l2_size=2MB --l1i_assoc=4 --l1d_assoc=2 --l2_assoc=8 --cacheline_size=128 --cpu-clock=1GHz -c spec_cpu2006/429.mcf/src/specmcf -o "spec_cpu2006/429.mcf/data/inp.in" -I 100000000 
```
![opt_specmcf](https://github.com/user-attachments/assets/c8741e36-5334-48d5-822a-8d29c001d588)

## SPECSJENG

From the [chart](#results), `specsjeng` exhibits a very high CPI. Both the L1 data and L2 caches have significant miss rates. To address these, in the first test, I doubled the size and associativity of the L1 data cache. In the second test, I applied the same doubling to the L2 cache. For the third test, I combined the configurations of the first two tests. Finally, in the fourth test, I added a doubling of the cache line size on top of the third test’s configurations.

The commands used are as follows:

```bash
$ ./build/ARM/gem5.opt -d spec_results_opt/specsjeng/1 configs/example/se.py --cpu-type=MinorCPU --caches --l2cache --l1d_size=128kB --l1i_size=32kB --l2_size=2MB --l1i_assoc=2 --l1d_assoc=4 --l2_assoc=8 --cacheline_size=64 --cpu-clock=1GHz -c spec_cpu2006/458.sjeng/src/specsjeng -o "spec_cpu2006/458.sjeng/data/test.txt" -I 100000000 

$ ./build/ARM/gem5.opt -d spec_results_opt/specsjeng/2 configs/example/se.py --cpu-type=MinorCPU --caches --l2cache --l1d_size=64kB --l1i_size=32kB --l2_size=4MB --l1i_assoc=2 --l1d_assoc=2 --l2_assoc=16 --cacheline_size=64 --cpu-clock=1GHz -c spec_cpu2006/458.sjeng/src/specsjeng -o "spec_cpu2006/458.sjeng/data/test.txt" -I 100000000 

$ ./build/ARM/gem5.opt -d spec_results_opt/specsjeng/3 configs/example/se.py --cpu-type=MinorCPU --caches --l2cache --l1d_size=128kB --l1i_size=32kB --l2_size=4MB --l1i_assoc=2 --l1d_assoc=4 --l2_assoc=16 --cacheline_size=64 --cpu-clock=1GHz -c spec_cpu2006/458.sjeng/src/specsjeng -o "spec_cpu2006/458.sjeng/data/test.txt" -I 100000000
$ ./build/ARM/gem5.opt -d spec_results_opt/specsjeng/4 configs/example/se.py --cpu-type=MinorCPU --caches --l2cache --l1d_size=128kB --l1i_size=32kB --l2_size=4MB --l1i_assoc=2 --l1d_assoc=4 --l2_assoc=16 --cacheline_size=128 --cpu-clock=1GHz -c spec_cpu2006/458.sjeng/src/specsjeng -o "spec_cpu2006/458.sjeng/data/test.txt" -I 100000000
```
![opt2_specsjeng](https://github.com/user-attachments/assets/a0a4b94e-7579-488f-8bc0-87fdbad0ed7d)

## SPECHMMER

By looking at this [chart](#results), we can see that the `spechmmer` benchmark already exhibits a satisfactory CPI, being close to 1. However, since the L2 cache had the highest miss rate among the caches, I first doubled its size and associativity. Then, in the second test i kept the configurations of the first test and doubled the size of the L1 data cache and its associativity aswell. Lastly, in the third test, since there was an slight improvement in the second test compared to the first one,i retained the second test's optimizations and doubled the cache line size.

The commands used are as follows:

```bash
$ ./build/ARM/gem5.opt -d spec_results_opt/spechmmer/1 configs/example/se.py --cpu-type=MinorCPU --caches --l2cache --l1d_size=64kB --l1i_size=32kB --l2_size=4MB --l1i_assoc=2 --l1d_assoc=2 --l2_assoc=16 --cacheline_size=64 --cpu-clock=1GHz -c spec_cpu2006/456.hmmer/src/spechmmer -o "--fixed 0 --mean 325 --num 45000 --sd 200 --seed 0 spec_cpu2006/456.hmmer/data/bombesin.hmm" -I 100000000

$ ./build/ARM/gem5.opt -d spec_results_opt/spechmmer/2 configs/example/se.py --cpu-type=MinorCPU --caches --l2cache --l1d_size=128kB --l1i_size=32kB --l2_size=4MB --l1i_assoc=2 --l1d_assoc=4 --l2_assoc=16 --cacheline_size=64 --cpu-clock=1GHz -c spec_cpu2006/456.hmmer/src/spechmmer -o "--fixed 0 --mean 325 --num 45000 --sd 200 --seed 0 spec_cpu2006/456.hmmer/data/bombesin.hmm" -I 100000000 

$ ./build/ARM/gem5.opt -d spec_results_opt/spechmmer/3 configs/example/se.py --cpu-type=MinorCPU --caches --l2cache --l1d_size=128kB --l1i_size=32kB --l2_size=4MB --l1i_assoc=2 --l1d_assoc=4 --l2_assoc=16 --cacheline_size=128 --cpu-clock=1GHz -c spec_cpu2006/456.hmmer/src/spechmmer -o "--fixed 0 --mean 325 --num 45000 --sd 200 --seed 0 spec_cpu2006/456.hmmer/data/bombesin.hmm" -I 100000000
```
![opt_spechmmer](https://github.com/user-attachments/assets/9637c5e4-fa54-4c4f-ad7c-db2871aea2e8)

## SPECBZIP

By looking at this [chart](#results) and at the intial graphs, we can see that the `specbzip` benchmark represents similar results with the `spechmmer` benchmark. Thus, i applied the exact same tests on the `specbzip` benchmark as the `spechmmer`benchmark. 

The commands used are as follows:

```bash
$ ./build/ARM/gem5.opt -d spec_results_opt/specbzip/2 configs/example/se.py --cpu-type=MinorCPU --caches --l2cache --l1d_size=64kB --l1i_size=32kB --l2_size=4MB --l1i_assoc=2 --l1d_assoc=2 --l2_assoc=16 --cacheline_size=64 --cpu-clock=1GHz -c spec_cpu2006/401.bzip2/src/specbzip -o "spec_cpu2006/401.bzip2/data/input.program 10" -I 100000000 

$ ./build/ARM/gem5.opt -d spec_results_opt/specbzip/3 configs/example/se.py --cpu-type=MinorCPU --caches --l2cache --l1d_size=128kB --l1i_size=32kB --l2_size=4MB --l1i_assoc=2 --l1d_assoc=4 --l2_assoc=16 --cacheline_size=64 --cpu-clock=1GHz -c spec_cpu2006/401.bzip2/src/specbzip -o "spec_cpu2006/401.bzip2/data/input.program 10" -I 100000000

$ ./build/ARM/gem5.opt -d spec_results_opt/specbzip/4 configs/example/se.py --cpu-type=MinorCPU --caches --l2cache --l1d_size=128kB --l1i_size=32kB --l2_size=4MB --l1i_assoc=2 --l1d_assoc=4 --l2_assoc=16 --cacheline_size=128 --cpu-clock=1GHz -c spec_cpu2006/401.bzip2/src/specbzip -o "spec_cpu2006/401.bzip2/data/input.program 10" -I 100000000

```
![opt_specbzip](https://github.com/user-attachments/assets/2ee0d86a-6d24-4d1f-8993-210a5a938ae1)

## STEP3: Cost function

The cost function we were asked to design must capture the effects of increasing all the characteristics tested in the previous section. Since we need to emphasize both the system’s speed and the circuit's size, my initial approach to defining the concept is as follows:

![Cost Function](https://latex.codecogs.com/png.latex?\bg_white%20\text{Cost}%20=%20|\text{CPI}%20-%201|%20+%20\text{Resource%20Cost})

As shown, the function consists of two main components:

* ![Speed Cost](https://latex.codecogs.com/png.latex?\bg_white%20\text{Cost}_1%20=%20|\text{CPI}%20-%201|)

This term represents the performance cost. A higher CPI indicates a slower system, so deviations from the ideal CPI of 1 are penalized.

* ![Resource Cost](https://latex.codecogs.com/png.latex?\bg_white%20\text{Cost}_2%20=%20\text{Resource%20Cost})

This term quantifies the hardware cost associated with the system's configuration. Since increases in cache size and associativity have varying impacts on the circuit's size and complexity, the resource cost is expanded into the following detailed formula:

![Formula](https://latex.codecogs.com/png.latex?\bg_white%20\text{Cost2}%20=%20a%20\cdot%20\frac{\text{L1%20instruction%20cache%20size}}{32%20\text{kB}}%20+%20b%20\cdot%20\frac{\text{L1%20data%20cache%20size}}{64%20\text{kB}}%20+%20c%20\cdot%20\frac{\text{L2%20cache%20size}}{2%20\text{MB}}%20+%20d%20\cdot%20\frac{\text{L1%20instruction%20cache%20associativity}}{2}%20+%20e%20\cdot%20\frac{\text{L1%20data%20cache%20associativity}}{2}%20+%20f%20\cdot%20\frac{\text{L2%20cache%20associativity}}{8}%20+%20g%20\cdot%20\frac{\text{Cache%20line%20size}}{64%20\text{kB}})

In this formulation:

`a`, `b`, `c`, `d`, `e`, `f`, and `g` are weights that reflect the relative cost impact of each parameter.
The denominators represent baseline values, allowing the function to express the relative increase in cost compared to standard configurations.

We know that L1 caches are more expensive than L2 caches. L2 caches have a lower cost per bit due to their greater distance from the core and slower access times. On the other hand, L1 caches, being closer to the core, have a higher cost per bit due to their speed and proximity. Therefore, a larger coefficient was assigned to L1 caches to reflect their higher impact on the overall cost.

An increase in cache line size is the least costly change in terms of circuit complexity. Cache line size has a moderate effect on both speed and circuit size. Larger block sizes can improve hit rates (due to spatial locality), but they also increase transfer time. As such, a relatively small coefficient was chosen for this parameter.

Higher **associativity** results in more complex circuits. Associativity increases the number of comparators and multiplexers, which directly affects the circuit's physical size and design complexity. While it can improve hit rates, higher associativity also increases dynamic power consumption approximately linearly as more data is read out simultaneously. The coefficients for associativity were chosen to reflect these trade-offs.

Finally, the coefficients assigned to cache size and associativity balance their relative costs:
- **Cache size**: Larger caches require more physical space on the chip, significantly increasing the circuit's size. 
- **Associativity**: Higher associativity adds to design complexity and power consumption.

### Coefficients
The coefficients used in the cost function are as follows:
- `a = 0.175` (L1 instruction cache size)
- `b = 0.175` (L1 data cache size)
- `c = 0.25` (L2 cache size)
- `d = 0.1` (L1 instruction cache associativity)
- `e = 0.1` (L1 data cache associativity)
- `f = 0.15` (L2 cache associativity)
- `g = 0.05` (Cache line size)

These coefficients were chosen to represent the relative impact of each parameter on the system’s speed and circuit size, ensuring a balanced and accurate cost function.

After using these [python codes](https://github.com/AnatoliManolidou/Computer-Architecture-Project/tree/main/Second_part/Python_code/Cost_function_calculators), we have the following chart that represents the cost for each arcitecture of each benchmark: 

|Benchmark|L1D Size|L1I Size|L2 Size|L1D Associativity|L1I Associativity|L2 Associativity|Cache line Size|CPI|Cost2|Cost1|Cost|
|---------|--------|--------|-------|-----------------|-----------------|----------------|---------------|---|-----|-----|----|
|SPECLIBM0|64kB|32kB|2MB|2|2|8|64B|3.49342|1.0000|2.4934|3.4934|
|SPECLIBM1|128kB|32kB|2MB|4|2|8|64B|2.62326|1.2750|1.6233|2.8983|
|SPECLIBM2|128kB|32kB|4MB|4|2|16|64B|3.92024|1.6750|2.9202|4.5952|
|SPECLIBM3|128kB|32kB|2MB|4|2|16|128B|2.62326|1.4750|1.6233|3.0983|
|SPECLIBM4|128kB|32kB|4MB|4|2|16|128B|2.62076|1.7250|1.6208|3.3458
|SPECLIBM5|64kB|32kB|2MB|2|2|8|128B|1.99046|1.0500|0.9905|2.0405|
|         |    |    |   | | | |    |       |      |      |      |
|SPECMCF0|64kB|32kB|2MB|2|2|8|64B|1.29910|1.0000|0.2991|1.2991|
|SPECMCF1|64kB|64kB|2MB|2|4|8|64B|1.13938|1.2750|0.1394|1.4144|
|SPECMCF2|64kB|128kB|2MB|2|8|8|64B|1.13938|1.8250|0.1394|1.9644|
|SPECMCF3|64kB|64kB|2MB|2|4|8|128B|1.11297|1.3250|0.1130|1.4380|
|         |    |    |   | | | |    |       |      |      |      |
|SPECSJENG0|64kB|32kB|2MB|2|2|8|64B|10.27055|1.0000|9.2706|10.2706|
|SPECSJENG1|128kB|32kB|2MB|4|2|8|64B|7.04060|1.2750|6.0406|7.3156|
|SPECSJENG2|64kB|32kB|4MB|2|2|16|64B|7.03982|1.4000|6.0398|7.4398|
|SPECSJENG3|128kB|32kB|4MB|4|2|16|64B|7.03974|1.6750|6.0397|7.7147|
|SPECSJENG4|128kB|32kB|4MB|4|2|16|128B|4.97296|1.7250|3.9730|5.6980|
|SPECSJENG5|128kB|32kB|2MB|2|2|8|64B|1.33754|1.1750|0.3375|1.5125|
|SPECSJENG6|64kB|32kB|2MB|4|2|8|64B|7.04056|1.1000|6.0406|7.1406|
|         |    |    |   | | | |    |       |      |      |      |
|SPECHMMER0|64kB|32kB|2MB|2|2|8|64B|1.18792|1.0000|0.1879|1.1879|
|SPECHMMER1|64kB|32kB|4MB|2|2|16|64B|1.18530|1.4000|0.1853|1.5853|
|SPECHMMER2|128kB|32kB|4MB|4|2|16|64B|1.18327|1.6750|0.1833|1.8583|
|SPECHMMER3|128kB|32kB|4MB|4|2|16|128B|1.17879|1.7250|0.1788|1.9038|
|         |    |    |   | | | |    |       |      |      |      |
|SPECBZIP0|64kB|32kB|2MB|2|2|8|64B|1.67965|1.0000|0.6797|1.6797|
|SPECBZIP1|64kB|32kB|4MB|2|2|16|64B|1.59611|1.4000|0.5961|1.9961|
|SPECBZIP2|128kB|32kB|4MB|4|2|16|64B|1.56834|1.6750|0.5683|2.2433|
|SPECBZIP3|128kB|32kB|4MB|4|2|16|128B|1.55565|1.7250|0.5556|2.2807|

From the above chart, as regards the best architectures for both cost & performance, for each benchmark we can conclude the following:

`SPECLIBM`: **SPECLIBM5** (Cost: 2.0405, CPI: 1.99046)\
`SPECMCF`: **SPECMCF0** (Cost: 1.2991, CPI: 1.29910)\
`SPECSJENG`: **SPECSJENG5** (Cost: 1.5125, CPI: 1.33754)\
`SPECHMMER`: **SPECHMMER0** (Cost: 1.1879, CPI: 1.18792)\
`SPECBZIP`: **SPECBZIP0** (Cost: 1.6797, CPI: 1.67965)

These architectures represent the best balance of minimizing cost and maximizing performance for each benchmark.



# REFERENCES

[GEM5 stats](https://www.gem5.org/documentation/learning_gem5/part1/gem5_stats/)\
[GEM5 cache](https://www.gem5.org/documentation/learning_gem5/part1/cache_config/)\
[Caches(1)](https://courses.cs.washington.edu/courses/cse378/07au/lectures/L18-Cache-Wrap-up.pdf)\
[Ccahes(2)](https://courses.cs.washington.edu/courses/cse378/09au/lectures/cse378au09-20.pdf)\
[Cache Memory Design Trade-offs](https://www2.it.uu.se/research/publications/lic/2003-009/2003-009.pdf)\
[Associativity](https://gab.wallawalla.edu/~curt.nelson/cptr380/lecture/chapter5%20-%20set%20associative%20caches.pdf)
