import math

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def get_adelic_metrics(n):
    """
    Runs the Collatz orbit for n until it reaches 1.
    Returns:
        k (odd steps), S (total steps), 
        Stress (log2 of the 'miss' factor),
        Drift (geometric contraction)
    """
    if n < 1: return None
    
    current = n
    k = 0 # odd steps
    S = 0 # total steps
    
    # Standard Collatz Trajectory
    while current != 1:
        if current % 2 == 0:
            current //= 2
            S += 1
        else:
            current = 3 * current + 1
            current //= 2 # Optimization: 3n+1 is always even
            S += 2        # Counts as 2 steps (multiply + divide)
            k += 1
            
    # --- The Adelic Calculation ---
    
    # The Equation of State:
    # 1 = (3^k * n + K) / 2^S
    # Therefore: K = 2^S - 3^k * n
    # Wait, if n goes to 1, then n_end = 1.
    # 1 * 2^S = 3^k * n + K
    # K = 2^S - 3^k * n
    
    pow_2_S = 1 << S
    pow_3_k = 3 ** k
    
    K = pow_2_S - (pow_3_k * n)
    
    # The Gap D is the denominator difference for a hypothetical cycle
    # D = |2^S - 3^k|
    Gap = abs(pow_2_S - pow_3_k)
    
    if Gap == 0: return None # Should not happen for S != k*log3/log2
    
    # The Alignment:
    # How much of the Gap does the Kernel share?
    alignment = gcd(abs(K), Gap)
    
    # Adelic Stress:
    # If alignment == Gap, Stress is 0 (Cycle Candidate).
    # If alignment == 1, Stress is maximal (Total Repulsion).
    # Metric = log2(Gap) - log2(alignment)
    # This measures "How many bits of the Gap remain unsatisfied?"
    
    stress = math.log2(Gap) - math.log2(alignment)
    
    return {
        "n": n,
        "k": k,
        "S": S,
        "Gap_Bits": math.log2(Gap),
        "Stress": stress,
        "Repulsion_Ratio": stress / math.log2(Gap) # Normalized 0 to 1
    }