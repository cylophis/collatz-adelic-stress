import pandas as pd
import multiprocessing
from time import time
from collatz_metric import get_adelic_metrics

def worker(n):
    return get_adelic_metrics(n)

def main():
    # Settings
    START = 3
    END = 100000  # Start small. Increase to 10^7 or 10^9 later.
    CORES = multiprocessing.cpu_count()

    print(f"--- Mining Adelic Stress Data (Range: {START}-{END}) ---")
    print(f"--- Using {CORES} Cores ---")
    
    start_time = time()
    
    pool = multiprocessing.Pool(processes=CORES)
    data = pool.map(worker, range(START, END, 2)) # Only check odds
    pool.close()
    pool.join()
    
    # Filter Nones
    data = [d for d in data if d is not None]
    
    df = pd.DataFrame(data)
    csv_name = "collatz_adelic_data.csv"
    df.to_csv(csv_name, index=False)
    
    print(f"--- Done. Saved {len(df)} rows to {csv_name} ---")
    print(f"--- Time: {time() - start_time:.2f}s ---")

if __name__ == "__main__":
    main()