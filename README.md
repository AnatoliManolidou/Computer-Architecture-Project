# SECOND PART

## First step. Execute SPEC CPU2006 Benchmarks on GEM5

### First question. What informations can you get about the memory system of the CPU that we are simulating?

From the `config.ini` file i got: 

|Size characteristics|config.ini|
|---------------|----------------|
|L1D|line 155/line 179:[system.cpu.dcache]/size=65536|
|L1I|line 789/line 813:[system.cpu.icache]/size=32768|
|L2|line 994/line 1018:[system.l2]/size=2097152|
|Cache line|line 155: "cache_line_size": 64|


### Second Question

These are the commands that were used:

```shell

$ ./build/ARM/gem5.opt -d spec_results/specbzip configs/example/se.py --cpu-type=MinorCPU --caches --l2cache -c spec_cpu2006/401.bzip2/src/specbzip -o "spec_cpu2006/401.bzip2/data/input.program 10" -I 100000000

$ ./build/ARM/gem5.opt -d spec_results/specmcf configs/example/se.py --cpu-type=MinorCPU --caches --l2cache -c spec_cpu2006/429.mcf/src/specmcf -o "spec_cpu2006/429.mcf/data/inp.in" -I 100000000

$ ./build/ARM/gem5.opt -d spec_results/spechmmer configs/example/se.py --cpu-type=MinorCPU --caches --l2cache -c spec_cpu2006/456.hmmer/src/spechmmer -o "--fixed 0 --mean 325 --num 45000 --sd 200 --seed 0 spec_cpu2006/456.hmmer/data/bombesin.hmm" -I 100000000

$ ./build/ARM/gem5.opt -d spec_results/specsjeng configs/example/se.py --cpu-type=MinorCPU --caches --l2cache -c spec_cpu2006/458.sjeng/src/specsjeng -o "spec_cpu2006/458.sjeng/data/test.txt" -I 100000000

$ ./build/ARM/gem5.opt -d spec_results/speclibm configs/example/se.py --cpu-type=MinorCPU --caches --l2cache -c spec_cpu2006/470.lbm/src/speclibm -o "20 spec_cpu2006/470.lbm/data/lbm.in 0 1 spec_cpu2006/470.lbm/data/100_100_130_cf_a.of" -I 100000000

```
And these are the results that were extracted from the `stats.txt` file of each benchmark:

 | Characteristics | specbzip | specmcf | spechmmer | sjeng | speclbm |
 | ------ | ------ | ------ | ------ | ------ | ------ |
 | Execution time |line 12: 0.083982|line12: 0.064955 |line 12: 0.05936 |line 12: 0.513528 |line 12: 0.174671 |
 | CPI |line 29: 1.679650|line 29: 1.299095|line 29: 1.187917 |line 29: 10.270554 |line 29: 3.493415 |
 | L1 Instruction cache miss rates|line 780: 0.000077|line 781: 0.023612 |line 739: 0.000221 |line 779: 0.000020 |line 770: 0.000094 |
 | L1 Data cache miss rates |line 867: 0.014798|line 868: 0.002107 |line 827: 0.001637 |line 865: 0.121831 |line 856: 0.060972 |
 | L2 cache miss rates |line 320: 0.282163|line 320: 0.055046 |line 318: 0.077760 |line 320: 0.999972 |line 320: 0.999944 |

Below there are 5 different graphs, each representing one of the characteristics that were just mentioned, over all of the 5 benchmarks. This [pyhton code](https://github.com/AnatoliManolidou/Computer-Architecture-Project/blob/main/Second_part/Python_code/Part2_Graphs2.py) was used for generating the graphs while using the [stats.txt files](https://github.com/AnatoliManolidou/Computer-Architecture-Project/tree/main/Second_part/Benchmarks_results) from the benchmarks.

![execution_time](https://github.com/user-attachments/assets/fec541e8-908a-44b4-a2ba-5fc09b668bf0)
![cpi](https://github.com/user-attachments/assets/c1647cad-cf51-460b-b1b6-c07da9d69d41)
![li_miss_rate](https://github.com/user-attachments/assets/e34c820e-9776-4e24-9e3b-4dff0cb6a2aa)
![ld_miss_rate](https://github.com/user-attachments/assets/143fb88e-58c4-44aa-a88d-cabf74134db2)
![l2_miss_rate](https://github.com/user-attachments/assets/a93ba7e8-96b4-450d-aeb6-2c317d38dda0)


### Third question

After running all the benchmarks for the two new frequency configurations, these are the results from the stats.txt about the clock (for all the benchmarks and for the three frequencies, the clock informations on stats.txt files were the same, thus the following snippets were derived from the `specmcf` benchmark).

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
** Final conclusions:

* Default frequency:
  The CPU is clocked at 2GHz, since we have 500 ticks and 1/500=2GHZ

* 1GHz:
The CPU is clocked at 1GHz, since we have 1000 ticks and 1/1000=1GHz

* 3GHz:
The CPU is clocked at 3GHz, since we have 333 ticks and 1/333=3GHz  




