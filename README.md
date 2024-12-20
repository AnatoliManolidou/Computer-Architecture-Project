# SECOND PART

## First step. Execute SPEC CPU2006 Benchmarks σon GEM5

### First question. What informations can you get abouth the memory system of the CPU that we are simulating?

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
 | Execution time |line 12: 0.083982|line12: 0.064955 | 0.05936 | 0.513528 | 0.174671 |
 | CPI |line 29: 1.679650|line 29: 1.299095| 1.187917 | 10.270554 | 3.493415 |
 | L1 Instruction cache miss rates|line 780: 0.000077|line 781: 0.023612 | 0.000221 | 0.000020 | 0.000094 |
 | L1 Data cache miss rates |line 867: 0.014798|line 868: 0.002107 | 0.001637 | 0.121831 | 0.060972 |
 | L2 cache miss rates |line 320: 0.282163|line 320: 0.055046 | 0.077760 | 0.907550 | 0.999944 |
