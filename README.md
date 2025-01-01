# SECOND PART

## First step. Execute SPEC CPU2006 Benchmarks on GEM5

### First question. What informations can you get about the memory system of the CPU that we are simulating?

From the `config.ini` file: 

|Size characteristics|config.ini|
|---------------|----------------|
|L1D|`line 155/line 179:` [system.cpu.dcache]/size=65536|
|L1I|`line 789/line 813:` [system.cpu.icache]/size=32768|
|L2|`line 994/line 1018:` [system.l2]/size=2097152|
|Cache line|`line 155:`  "cache_line_size": 64|


l1d assoc = 2
l1i assoc = 2
l2 assoc = 8


### Second Question. Benchmark analysis

These are the commands that were used:

```shell

$ ./build/ARM/gem5.opt -d spec_results/specbzip configs/example/se.py --cpu-type=MinorCPU --caches --l2cache -c spec_cpu2006/401.bzip2/src/specbzip -o "spec_cpu2006/401.bzip2/data/input.program 10" -I 100000000

$ ./build/ARM/gem5.opt -d spec_results/specmcf configs/example/se.py --cpu-type=MinorCPU --caches --l2cache -c spec_cpu2006/429.mcf/src/specmcf -o "spec_cpu2006/429.mcf/data/inp.in" -I 100000000

$ ./build/ARM/gem5.opt -d spec_results/spechmmer configs/example/se.py --cpu-type=MinorCPU --caches --l2cache -c spec_cpu2006/456.hmmer/src/spechmmer -o "--fixed 0 --mean 325 --num 45000 --sd 200 --seed 0 spec_cpu2006/456.hmmer/data/bombesin.hmm" -I 100000000

$ ./build/ARM/gem5.opt -d spec_results/specsjeng configs/example/se.py --cpu-type=MinorCPU --caches --l2cache -c spec_cpu2006/458.sjeng/src/specsjeng -o "spec_cpu2006/458.sjeng/data/test.txt" -I 100000000

$ ./build/ARM/gem5.opt -d spec_results/speclibm configs/example/se.py --cpu-type=MinorCPU --caches --l2cache -c spec_cpu2006/470.lbm/src/speclibm -o "20 spec_cpu2006/470.lbm/data/lbm.in 0 1 spec_cpu2006/470.lbm/data/100_100_130_cf_a.of" -I 100000000

```
And these are the results that were extracted from the `stats.txt` file of each benchmark:

# Results
 | Characteristics | specbzip | specmcf | spechmmer | specsjeng | speclibm |
 | ------ | ------ | ------ | ------ | ------ | ------ |
 | Execution time |`line 12:` 0.083982|`line12:` 0.064955 |`line 12:` 0.05936 |`line 12:` 0.513528 |`line 12:` 0.174671 |
 | CPI |`line 29:` 1.679650|`line 29:` 1.299095|`line 29:` 1.187917 |`line 29:` 10.270554 |`line 29:` 3.493415 |
 | L1 Instruction cache miss rates|`line 780:` 0.000077|line 781: 0.023612 |line 739: 0.000221 |line 779: 0.000020 |line 770: 0.000094 |
 | L1 Data cache miss rates |line 867: 0.014798|line 868: 0.002107 |line 827: 0.001637 |line 865: 0.121831 |line 856: 0.060972 |
 | L2 cache miss rates |line 320: 0.282163|line 320: 0.055046 |line 318: 0.077760 |line 320: 0.999972 |line 320: 0.999944 |

Below there are 5 different graphs, each representing one of the characteristics that were just mentioned, over all of the 5 benchmarks. This [pyhton code](https://github.com/AnatoliManolidou/Computer-Architecture-Project/blob/main/Second_part/Python_code/Part2_Graphs2.py) was used for generating the graphs while using the [stats.txt files](https://github.com/AnatoliManolidou/Computer-Architecture-Project/tree/main/Second_part/Benchmarks_results) from the benchmarks.

![execution_time](https://github.com/user-attachments/assets/fec541e8-908a-44b4-a2ba-5fc09b668bf0)
![cpi](https://github.com/user-attachments/assets/c1647cad-cf51-460b-b1b6-c07da9d69d41)
![li_miss_rate](https://github.com/user-attachments/assets/e34c820e-9776-4e24-9e3b-4dff0cb6a2aa)
![ld_miss_rate](https://github.com/user-attachments/assets/143fb88e-58c4-44aa-a88d-cabf74134db2)
![l2_miss_rate](https://github.com/user-attachments/assets/a93ba7e8-96b4-450d-aeb6-2c317d38dda0)


### Third question. Effect of Changing CPU Frequency

After running the benchmarks for the two new frequency configurations, here are the results related to the clock from the stats.txt files. These snippets were derived from the specmcf benchmark, where the clock values were the same across all benchmarks.

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

lines 114-118
```bash
"clk_domain": {
            "name": "clk_domain", 
            "clock": [
                1000
            ],
```
and lines 160-164
```bash
"cpu_clk_domain": {
            "name": "cpu_clk_domain", 
            "clock": [
                1000
            ],
```
Now, if we add one more processor it would more likely inherit the `cpu_clk_domain`, since this new CPU operates with a seperate clock that is independed from the rest of the system. Finally, using the [pyhton code](https://github.com/AnatoliManolidou/Computer-Architecture-Project/blob/main/Second_part/Python_code/Part2_Graphs2.py) that was used before (now modified to extract only the graph for execution time) we obtained the following graphs:
![execution_time_1GHz](https://github.com/user-attachments/assets/fa803096-e3f1-4b4b-9cf7-0a593e924aa2)
![execution_time_3GHz](https://github.com/user-attachments/assets/8db07496-97ab-4749-8442-98d31d7ff7d7)

When comparing these graphs to the one for the default frequency, we do not see perfect scaling. This is because execution time does not depend solely on the CPU's frequency. There are many other factors influencing execution time, and changing just one parameter (like the CPU frequency) will not result in a perfectly linear reduction in execution time.

### Fourth Question. Changing the memory configuration.

For changing the memory configuration, the benchmark `speclibm` was chosen, and the following command was used:

```bash
./build/ARM/gem5.opt -d spec_results_memory/speclibm configs/example/se.py --cpu-type=MinorCPU --cpu-clock=1GHz --mem-type=DDR3_2133_8x8 --caches --l2cache -c spec_cpu2006/470.lbm/src/speclibm -o '20 spec_cpu2006/470.lbm/data/lbm.in 0 1 spec_cpu2006/470.lbm/data/100_100_130_cf_a.of' -I 100000000
```
Now the memory type is set to `DDR3_2133_8x8` {Important! `DDR3_2113_x64` was not listed}. From `stats.txt` we have the following:

```bash
sim_seconds                                  0.257413                       # Number of seconds simulated
```

while for `DDR3_1600_x64` we had:

```bash
sim_seconds                                  0.174671                       # Number of seconds simulated
```

# STEP 2

After taking into consideration these [results](#results) from step 1, for each characteristic the following conclusions were made:

* Cache Line Size
The effectiveness of the cache line size depends on spatial locality. For benchmarks like `sjeng` and `speclibm`, higher L2 miss rates might indicate poor spatial locality.

* L2 Cache Associativity
Extremely high L2 miss rates for `sjeng` and `speclibm` suggest either capacity or conflict misses. So we should increase associativity if increasing size alone does not resolve the high miss rates and specifically, moving from 4-way to 8-way or higher. Associativity improvements are often more effective when combined with larger cache sizes.

* L2 Cache Size
The highest L2 cache miss rates are in `speclibm` (0.999944) and `sjeng` (0.999972), indicating severe L2 capacity issues. Other benchmarks like specbzip, specmcf, and spechmm show manageable miss rates (< 0.3). Thus, an increase in L2 cache size significantly for `sjeng` and `speclibm` was tested, as these benchmarks heavily rely on L2.

* L1 Data Cache Associativity
Moderate miss rates for `sjeng` and `speclibm` suggest potential conflict misses. An increase in associativity for L1 data cache for `sjeng` and `speclibm` was tested.

* L1 Data Cache Size

Agaim, `sjeng` (0.121831) and `speclibm` (0.060972) show relatively higher L1 data cache miss rates compared to others. Other benchmarks have very low miss rates, indicating sufficient L1 data cache size. Increase L1 data cache size specifically for `sjeng` and `speclibm`. These benchmarks appear to have larger data sets or higher spatial locality.

* L1 Instruction Cache Associativity
no change

* L1 Instruction Cache Size
no change 


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

### SPECMCF

From the [chart](#results), it is apparent that the L1 instruction cache has a high miss rate. To mitigate this, in the first test, I doubled both the size and associativity of the L1 instruction cache. In the second test, I quadrupled these parameters. For the third test, I reverted the L1I size to 64kB and its associativity to 4, but doubled the cache line size instead.

The commands used are as follows:

```bash
$ ./build/ARM/gem5.opt -d spec_results_opt/specmcf/1 configs/example/se.py --cpu-type=MinorCPU --caches --l2cache --l1d_size=64kB --l1i_size=64kB --l2_size=2MB --l1i_assoc=4 --l1d_assoc=2 --l2_assoc=8 --cacheline_size=64 --cpu-clock=1GHz -c spec_cpu2006/429.mcf/src/specmcf -o "spec_cpu2006/429.mcf/data/inp.in" -I 100000000 

$ ./build/ARM/gem5.opt -d spec_results_opt/specmcf/2 configs/example/se.py --cpu-type=MinorCPU --caches --l2cache --l1d_size=64kB --l1i_size=128kB --l2_size=2MB --l1i_assoc=8 --l1d_assoc=2 --l2_assoc=8 --cacheline_size=64 --cpu-clock=1GHz -c spec_cpu2006/429.mcf/src/specmcf -o "spec_cpu2006/429.mcf/data/inp.in" -I 100000000

$ ./build/ARM/gem5.opt -d spec_results_opt/specmcf/3 configs/example/se.py --cpu-type=MinorCPU --caches --l2cache --l1d_size=64kB --l1i_size=64kB --l2_size=2MB --l1i_assoc=4 --l1d_assoc=2 --l2_assoc=8 --cacheline_size=128 --cpu-clock=1GHz -c spec_cpu2006/429.mcf/src/specmcf -o "spec_cpu2006/429.mcf/data/inp.in" -I 100000000 
```

### SPECSJENG

From the [chart](#results), `specsjeng` exhibits a very high CPI. Both the L1 data and L2 caches have significant miss rates. To address these, in the first test, I doubled the size and associativity of the L1 data cache. In the second test, I applied the same doubling to the L2 cache. For the third test, I combined the configurations of the first two tests. Finally, in the fourth test, I added a doubling of the cache line size on top of the third test’s configurations.

The commands used are as follows:

```bash
$ ./build/ARM/gem5.opt -d spec_results_opt/specsjeng/1 configs/example/se.py --cpu-type=MinorCPU --caches --l2cache --l1d_size=128kB --l1i_size=32kB --l2_size=2MB --l1i_assoc=2 --l1d_assoc=4 --l2_assoc=8 --cacheline_size=64 --cpu-clock=1GHz -c spec_cpu2006/458.sjeng/src/specsjeng -o "spec_cpu2006/458.sjeng/data/test.txt" -I 100000000  > double l1d size = 64 , double l1d associativity = 4

$ ./build/ARM/gem5.opt -d spec_results_opt/specsjeng/2 configs/example/se.py --cpu-type=MinorCPU --caches --l2cache --l1d_size=64kB --l1i_size=32kB --l2_size=4MB --l1i_assoc=2 --l1d_assoc=2 --l2_assoc=16 --cacheline_size=64 --cpu-clock=1GHz -c spec_cpu2006/458.sjeng/src/specsjeng -o "spec_cpu2006/458.sjeng/data/test.txt" -I 100000000  > double l2 size = 4MB , double l2 associativity = 16

$ ./build/ARM/gem5.opt -d spec_results_opt/specsjeng/3 configs/example/se.py --cpu-type=MinorCPU --caches --l2cache --l1d_size=128kB --l1i_size=32kB --l2_size=4MB --l1i_assoc=2 --l1d_assoc=4 --l2_assoc=16 --cacheline_size=64 --cpu-clock=1GHz -c spec_cpu2006/458.sjeng/src/specsjeng -o "spec_cpu2006/458.sjeng/data/test.txt" -I 100000000  > double l2 size = 4MB , double l2 associativity = 16 double l1d size = 64 , double l1d associativity = 4

$ ./build/ARM/gem5.opt -d spec_results_opt/specsjeng/4 configs/example/se.py --cpu-type=MinorCPU --caches --l2cache --l1d_size=128kB --l1i_size=32kB --l2_size=4MB --l1i_assoc=2 --l1d_assoc=4 --l2_assoc=16 --cacheline_size=128 --cpu-clock=1GHz -c spec_cpu2006/458.sjeng/src/specsjeng -o "spec_cpu2006/458.sjeng/data/test.txt" -I 100000000  > double l2 size = 4MB , double l2 associativity = 16 double l1d size = 64 , double l1d associativity = 4, double cache line size = 128
```

### SPECHMMER

By looking at this [chart](#results), we can see that the `spechmmer` benchmark already exhibits a satisfactory CPI, being close to 1. However, since the L2 cache had the highest miss rate among the caches, I first doubled its size and associativity. Then, in the second test i kept the configurations of the first test and doubled the size of the L1 data cache and its associativity aswell. Lastly, in the third test, since there was an slight improvement in the second test compared to the first one,i retained the second test's optimizations and doubled the cache line size.

The commands used are as follows:

```bash
$ ./build/ARM/gem5.opt -d spec_results_opt/spechmmer/1 configs/example/se.py --cpu-type=MinorCPU --caches --l2cache --l1d_size=64kB --l1i_size=32kB --l2_size=4MB --l1i_assoc=2 --l1d_assoc=2 --l2_assoc=16 --cacheline_size=64 --cpu-clock=1GHz -c spec_cpu2006/456.hmmer/src/spechmmer -o "--fixed 0 --mean 325 --num 45000 --sd 200 --seed 0 spec_cpu2006/456.hmmer/data/bombesin.hmm" -I 100000000 > double l2 size and l2 associativity

$ ./build/ARM/gem5.opt -d spec_results_opt/spechmmer/2 configs/example/se.py --cpu-type=MinorCPU --caches --l2cache --l1d_size=128kB --l1i_size=32kB --l2_size=4MB --l1i_assoc=2 --l1d_assoc=4 --l2_assoc=16 --cacheline_size=64 --cpu-clock=1GHz -c spec_cpu2006/456.hmmer/src/spechmmer -o "--fixed 0 --mean 325 --num 45000 --sd 200 --seed 0 spec_cpu2006/456.hmmer/data/bombesin.hmm" -I 100000000 > double l2 size and l2 associativity and l1d

$ ./build/ARM/gem5.opt -d spec_results_opt/spechmmer/3 configs/example/se.py --cpu-type=MinorCPU --caches --l2cache --l1d_size=128kB --l1i_size=32kB --l2_size=4MB --l1i_assoc=2 --l1d_assoc=4 --l2_assoc=16 --cacheline_size=128 --cpu-clock=1GHz -c spec_cpu2006/456.hmmer/src/spechmmer -o "--fixed 0 --mean 325 --num 45000 --sd 200 --seed 0 spec_cpu2006/456.hmmer/data/bombesin.hmm" -I 100000000 > double l2 size and l2 associativity and l1d and cache line size
```

### SPECBZIP

By looking at this [chart](#results), we can see that the `spechmmer` benchmark already exhibits a satisfactory CPI, being close to 1. However, since the L2 cache had the highest miss rate among the caches, I first doubled its size and associativity. Then, in the second test i kept the configurations of the first test and doubled the size of the L1 data cache and its associativity aswell. Lastly, in the third test, since there was an slight improvement in the second test compared to the first one,i retained the second test's optimizations and doubled the cache line size.

The commands used are as follows:

```bash
$ ./build/ARM/gem5.opt -d spec_results_opt/spechmmer/1 configs/example/se.py --cpu-type=MinorCPU --caches --l2cache --l1d_size=64kB --l1i_size=32kB --l2_size=4MB --l1i_assoc=2 --l1d_assoc=2 --l2_assoc=16 --cacheline_size=64 --cpu-clock=1GHz -c spec_cpu2006/456.hmmer/src/spechmmer -o "--fixed 0 --mean 325 --num 45000 --sd 200 --seed 0 spec_cpu2006/456.hmmer/data/bombesin.hmm" -I 100000000 > double l2 size and l2 associativity

$ ./build/ARM/gem5.opt -d spec_results_opt/spechmmer/2 configs/example/se.py --cpu-type=MinorCPU --caches --l2cache --l1d_size=128kB --l1i_size=32kB --l2_size=4MB --l1i_assoc=2 --l1d_assoc=4 --l2_assoc=16 --cacheline_size=64 --cpu-clock=1GHz -c spec_cpu2006/456.hmmer/src/spechmmer -o "--fixed 0 --mean 325 --num 45000 --sd 200 --seed 0 spec_cpu2006/456.hmmer/data/bombesin.hmm" -I 100000000 > double l2 size and l2 associativity and l1d

$ ./build/ARM/gem5.opt -d spec_results_opt/spechmmer/3 configs/example/se.py --cpu-type=MinorCPU --caches --l2cache --l1d_size=128kB --l1i_size=32kB --l2_size=4MB --l1i_assoc=2 --l1d_assoc=4 --l2_assoc=16 --cacheline_size=128 --cpu-clock=1GHz -c spec_cpu2006/456.hmmer/src/spechmmer -o "--fixed 0 --mean 325 --num 45000 --sd 200 --seed 0 spec_cpu2006/456.hmmer/data/bombesin.hmm" -I 100000000 > double l2 size and l2 associativity and l1d and cache line size
```





# REFERENCES

[GEM5 stats](https://www.gem5.org/documentation/learning_gem5/part1/gem5_stats/)


