import re
import matplotlib.pyplot as plt
import os

# Function to extract data from stats file
def extract_data(file_path, metrics):
    data = {}
    with open(file_path, 'r') as f:
        content = f.read()
        for metric, regex in metrics.items():
            match = re.search(regex, content)
            if match:
                data[metric] = float(match.group(1))
    return data

# Define the metrics to extract
metrics = {
    'execution_time': r"sim_seconds\s+([\d.]+)",
    # 'cpi': r"system\.cpu\.cpi\s+([\d.]+)",
    # 'li_miss_rate': r"system\.cpu\.icache\.overall_miss_rate::total\s+([\d.]+)",
    # 'ld_miss_rate': r"system\.cpu\.dcache\.overall_miss_rate::total\s+([\d.]+)",
    # 'l2_miss_rate': r"system\.l2\.overall_miss_rate::total\s+([\d.]+)"
}

# Define the file paths and benchmark names
files = {
    "specbzip": r'C:\Users\anato\OneDrive\Υπολογιστής\Computer-Architecture-Project\Second_part\spec_results3\specbzip\stats.txt',
    "spechmmer": r'C:\Users\anato\OneDrive\Υπολογιστής\Computer-Architecture-Project\Second_part\spec_results3\spechmmer\stats.txt',
    "speclibm": r'C:\Users\anato\OneDrive\Υπολογιστής\Computer-Architecture-Project\Second_part\spec_results3\speclibm\stats.txt',
    "specsjeng": r'C:\Users\anato\OneDrive\Υπολογιστής\Computer-Architecture-Project\Second_part\spec_results3\specmcf\stats.txt',
    "specmcf": r'C:\Users\anato\OneDrive\Υπολογιστής\Computer-Architecture-Project\Second_part\spec_results3\specsjeng\stats.txt'
}

# Extract data
data = {}
for benchmark, file_path in files.items():
    if os.path.exists(file_path):
        data[benchmark] = extract_data(file_path, metrics)
    else:
        print(f"File not found: {file_path}")

# Prepare data for plotting
benchmarks = list(data.keys())
execution_times = [data[bm].get('execution_time', 0) for bm in benchmarks]
# cpi = [data[bm].get('cpi', 0) for bm in benchmarks]
# l1_miss_rate = [data[bm].get('li_miss_rate', 0) for bm in benchmarks]
# ld_miss_rate = [data[bm].get('ld_miss_rate', 0) for bm in benchmarks]
# l2_miss_rate = [data[bm].get('l2_miss_rate', 0) for bm in benchmarks]

# Plotting
def plot_metric(metric_values, title, ylabel, benchmarks, filename):
    plt.figure(figsize=(10, 6))
    plt.bar(benchmarks, metric_values, color='skyblue')
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel("Benchmarks")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()

plot_metric(execution_times, "Execution Time across Benchmarks for --cpu-clock=3GHz", "Execution Time (s)", benchmarks, "execution_time.png")
# plot_metric(cpi, "CPI across Benchmarks", "CPI", benchmarks, "cpi.png")
# plot_metric(l1_miss_rate, "L1 Instruction Cache Overall Miss Rate across Benchmarks", "LI Miss Rate", benchmarks, "li_miss_rate.png")
# plot_metric(ld_miss_rate, "L1 Data Cache Overall Miss Rate across Benchmarks", "LD Miss Rate", benchmarks, "ld_miss_rate.png")
# plot_metric(l2_miss_rate, "L2 Cache Overall Miss Rate across Benchmarks", "L2 Miss Rate", benchmarks, "l2_miss_rate.png")

