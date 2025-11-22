import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

def analyze():
    print("Loading Data...")
    df = pd.read_csv("collatz_adelic_data.csv")
    
    # Hypothesis: Stress scales linearly with k (Cycle Length)
    x = df['k']
    y = df['Stress']
    
    # Calculate Repulsion Slope
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    
    print(f"--- Analysis Results ---")
    print(f"Correlation (R^2): {r_value**2:.4f}")
    print(f"Repulsion Slope: {slope:.4f} bits per odd step")
    print(f"Intercept: {intercept:.4f}")
    
    # Visualization
    plt.figure(figsize=(12, 8))
    
    # Scatter plot (use small alpha for density)
    plt.scatter(x, y, s=1, alpha=0.1, color='black', label='Trajectory Stress')
    
    # Trend line
    trend_x = np.array([0, x.max()])
    trend_y = slope * trend_x + intercept
    plt.plot(trend_x, trend_y, color='red', linewidth=2, label=f'Mean Repulsion (Slope={slope:.2f})')
    
    # Ideal Line (Drift)
    # The geometric drift is ~0.415 bits per step (log2 3 - log2 2 approx)
    # If Stress > Drift, cycle impossible.
    
    plt.xlabel("Cycle Length k (Odd Steps)")
    plt.ylabel("Adelic Stress (Bits of Unsatisfied Gap)")
    plt.title("Empirical Evidence of Adelic Repulsion in 3x+1")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.savefig("adelic_repulsion_plot.png")
    print("Plot saved as adelic_repulsion_plot.png")
    plt.show()

if __name__ == "__main__":
    analyze()