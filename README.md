# SECOND PART

## First step. Execute SPEC CPU2006 Benchmarks on GEM5

### First question. What informations can you get about the memory system of the CPU that we are simulating?

From the config.ini file i got: 

|Size characteristics|config.ini|
|---------------|----------------|
|L1D|line 155/line 179:[system.cpu.dcache]/size=65536|
|L1I|line 789/line 813:[system.cpu.icache]/size=32768|
|L2|line 994/line 1018:[system.l2]/size=2097152|
|Cache line|line 155: "cache_line_size": 64|


### Second Question

 | Characteristics | specbzip | specmcf | spechmmer | sjeng | speclbm |
 | ------ | ------ | ------ | ------ | ------ | ------ |
 | Execution time |line 12: 0.083982|line12: 0.064955 |line 12: 0.05936 |line 12: 0.513528 |line 12: 0.174671 |
 | CPI |line 29: 1.679650|line 29: 1.299095|line 29: 1.187917 |line 29: 10.270554 |line 29: 3.493415 |
 | L1 Instruction cache miss rates|line 780: 0.000077|line 781: 0.023612 |line 739: 0.000221 |line 779: 0.000020 |line 770: 0.000094 |
 | L1 Data cache miss rates |line 867: 0.014798|line 868: 0.002107 |line 827: 0.001637 |line 865: 0.121831 |line 856: 0.060972 |
 | L2 cache miss rates |line 320: 0.282163|line 320: 0.055046 |line 318: 0.077760 |line 320: 0.999972 |line 320: 0.999944 |

Below there are 5 different graphs, each representing one of the characteristics that were just mentioned, over all of the 5 benchmarks. This [pyhton code]() was used for generating the graphs using the [stats.txt files]() from the benchmarks.

![execution_time](https://github.com/user-attachments/assets/fec541e8-908a-44b4-a2ba-5fc09b668bf0)
![cpi](https://github.com/user-attachments/assets/c1647cad-cf51-460b-b1b6-c07da9d69d41)
![li_miss_rate](https://github.com/user-attachments/assets/e34c820e-9776-4e24-9e3b-4dff0cb6a2aa)
![ld_miss_rate](https://github.com/user-attachments/assets/143fb88e-58c4-44aa-a88d-cabf74134db2)
![l2_miss_rate](https://github.com/user-attachments/assets/a93ba7e8-96b4-450d-aeb6-2c317d38dda0)


