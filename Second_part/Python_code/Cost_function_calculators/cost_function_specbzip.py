# Given data for each benchmark (updated with SPECHMMER configurations)
benchmarks = [
    {'name': 'SPECBZIP0', 'L1i_size': 32, 'L1d_size': 64, 'L2_size': 2, 'L1i_assoc': 2, 'L1d_assoc': 2, 'L2_assoc': 8, 'cacheline_size': 64, 'CPI': 1.67965},
    {'name': 'SPECBZIP1', 'L1i_size': 32, 'L1d_size': 64, 'L2_size': 4, 'L1i_assoc': 2, 'L1d_assoc': 2, 'L2_assoc': 16, 'cacheline_size': 64, 'CPI': 1.59611},
    {'name': 'SPECBZIP2', 'L1i_size': 32, 'L1d_size': 128, 'L2_size': 4, 'L1i_assoc': 2, 'L1d_assoc': 4, 'L2_assoc': 16, 'cacheline_size': 64, 'CPI': 1.56834},
    {'name': 'SPECBZIP3', 'L1i_size': 32, 'L1d_size': 128, 'L2_size': 4, 'L1i_assoc': 2, 'L1d_assoc': 4, 'L2_assoc': 16, 'cacheline_size': 128, 'CPI': 1.55565}
]

# Coefficients for the cost formula
a, b, c, d, e, f, g = 0.175, 0.175, 0.25, 0.1, 0.1, 0.15, 0.05

# Calculate the cost for each benchmark
for benchmark in benchmarks:
    # Compute Resource Cost (Cost2)
    resource_cost = (
        a * (benchmark['L1i_size'] / 32) +
        b * (benchmark['L1d_size'] / 64) +
        c * (benchmark['L2_size'] / 2) +
        d * (benchmark['L1i_assoc'] / 2) +
        e * (benchmark['L1d_assoc'] / 2) +
        f * (benchmark['L2_assoc'] / 8) +
        g * (benchmark['cacheline_size'] / 64)
    )
    
    # Compute Speed Cost (Cost1)
    speed_cost = abs(benchmark['CPI'] - 1)
    
    # Total Cost
    total_cost = speed_cost + resource_cost
    
    # Print the results for the benchmark
    print(f"Benchmark: {benchmark['name']}")
    print(f"CPI: {benchmark['CPI']}")
    print(f"Resource Cost: {resource_cost:.4f}")
    print(f"Speed Cost: {speed_cost:.4f}")
    print(f"Total Cost: {total_cost:.4f}")
    print("-" * 40)
