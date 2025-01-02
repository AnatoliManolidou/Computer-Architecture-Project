import os
import re
import matplotlib.pyplot as plt

def extract_cpi(file_path):
    """
    Extract the CPI value from a stats.txt file.
    Assumes that the file contains a line like 'cpi: <value>'.
    """
    with open(file_path, 'r') as file:
        for line in file:
            if 'cpi' in line.lower():
                match = re.search(r"system\.cpu\.cpi\s+([\d.]+)", line, re.IGNORECASE)
                if match:
                    return float(match.group(1))
    return None

def find_stats_files(base_dir):
    """
    Recursively find all stats.txt files in subdirectories of the given base directory.
    """
    stats_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file == "stats.txt":
                stats_files.append(os.path.join(root, file))
    return stats_files

def plot_cpi(stats_files, custom_labels):
    """
    Generate a plot for CPI values extracted from a list of stats.txt files.
    Each y-axis label will have a custom label provided by the `custom_labels` dictionary.
    """
    optimizations = []
    cpi_values = []

    for stats_file in stats_files:
        # Use the directory name as the optimization label
        optimization = os.path.basename(os.path.dirname(stats_file))
        cpi = extract_cpi(stats_file)
        
        if cpi is not None:
            optimizations.append(optimization)
            cpi_values.append(cpi)
        else:
            print(f"Warning: CPI value not found in {stats_file}")

    # Sort the data by optimization labels for consistent plotting
    sorted_data = sorted(zip(optimizations, cpi_values), key=lambda x: x[0])
    optimizations, cpi_values = zip(*sorted_data) if sorted_data else ([], [])

    # Use custom labels for the y-axis
    custom_labels_mapped = [custom_labels.get(opt, opt) for opt in optimizations]

    # Plot the CPI values
    plt.figure(figsize=(8, 6))
    plt.plot(custom_labels_mapped, cpi_values, marker='o', linestyle='-', color='b')
    plt.title("CPI Across different configurations for SPECBZIP")
    plt.xlabel("")
    plt.ylabel("CPI (Cycles per Instruction)")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Annotate each point with its exact CPI value (3 digits precision)
    for i, cpi in enumerate(cpi_values):
        plt.text(custom_labels_mapped[i], cpi, f"{cpi:.5f}", fontsize=9, ha='right', va='bottom', color='black')

    plt.show()

# Example usage for different benchmarks
benchmarks = {
    "spechmmer": {
        "base_directory": r"C:\Users\anato\OneDrive\Υπολογιστής\Computer-Architecture-Project\Second_part\spec_results_optimizations\spechmmer",
        "custom_labels": {
            "1": "Initial configurations",
            "2": "Double L2 size\n and associativity",
            "3": "Double L2 and L1D size\n and associativity",
            "4": "Double L2 and L1D size and\n associativity and double cache line size"
        }
    },
    "speclibm": {
        "base_directory": r"C:\Users\anato\OneDrive\Υπολογιστής\Computer-Architecture-Project\Second_part\spec_results_optimizations\speclibm",
        "custom_labels": {
            "1": "Initial configurations",
            "2": "Double L1D size\n and associativity",
            "3": "Double L2 and L1D size\n and associativity",
            "4": "Double L2 and L1D size and\n associativity and double cache line size",
            "5": "Double L1D size and associativity,\n double L2 associativity and cache line size",
            "6": "Double cache line size only"
        }
    },
    "specsjeng": {
        "base_directory": r"C:\Users\anato\OneDrive\Υπολογιστής\Computer-Architecture-Project\Second_part\spec_results_optimizations\specsjeng",
        "custom_labels": {
            "1": "Initial configurations",
            "2": "Double L1D size\n and associativity",
            "3": "Double L2 size\n and associativity",
            "4": "Double L2 and L1D size\n and associativity",
            "5": "Double L2 and L1D size and\n associativity and double cache line size"
        }
    },
    "specbzip": {
        "base_directory": r"C:\Users\anato\OneDrive\Υπολογιστής\Computer-Architecture-Project\Second_part\spec_results_optimizations\specbzip",
        "custom_labels": {
            "1": "Initial configurations",
            "2": "Double L2 size\n and associativity",
            "3": "Double L2 and L1D size\n and associativity",
            "4": "Double L2 and L1D size and\n associativity and double cache line size"
        }
    },
    "specmcf": {
        "base_directory": r"C:\Users\anato\OneDrive\Υπολογιστής\Computer-Architecture-Project\Second_part\spec_results_optimizations\specmcf",
        "custom_labels": {
            "1": "Initial configurations",
            "2": "Double L1I size\n and associativity",
            "3": "Quadruple L1I size\n and associativity",
            "4": "Double L1I size and associativity\n and double cache line size",
        }
    }
}

# Loop through each benchmark and generate plots
for benchmark_name, config in benchmarks.items():
    print(f"Processing {benchmark_name}...")
    stats_files = find_stats_files(config["base_directory"])
    if stats_files:
        plot_cpi(stats_files, config["custom_labels"])
    else:
        print(f"No stats.txt files found for {benchmark_name}.")
