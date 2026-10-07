"""
Phase 5: Dynamic Programming Applications
- 0/1 Knapsack: Resource allocation under budget / capacity constraints.
- Longest Common Subsequence (LCS): Requirement specification and preference matching.
- Matrix Chain Multiplication (MCM): Optimization of multi-stage supply chain operation pipeline.
- Resource Allocation Problem: Multi-project / multi-center utility maximization under finite resources.
- Brute Force vs DP Benchmarking and Complexity Tables.
"""

import os
import sys
import time
from typing import List, Tuple, Dict, Any, Optional

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ==============================================================================
# 1. 0/1 Knapsack for Resource Allocation
# ==============================================================================

def knapsack_01_dp(
    weights: List[int],
    values: List[float],
    capacity: int,
    item_names: Optional[List[str]] = None
) -> Tuple[float, List[int], List[str]]:
    """
    0/1 Knapsack using Dynamic Programming.
    Time Complexity: O(N * W)
    Space Complexity: O(N * W)
    Returns:
        - max_value: float
        - selected_indices: List[int]
        - selected_names: List[str]
    """
    n = len(weights)
    dp = [[0.0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        w = weights[i - 1]
        v = values[i - 1]
        for c in range(capacity + 1):
            if w <= c:
                dp[i][c] = max(dp[i - 1][c], dp[i - 1][c - w] + v)
            else:
                dp[i][c] = dp[i - 1][c]

    # Backtracking to find selected items
    selected_indices: List[int] = []
    c = capacity
    for i in range(n, 0, -1):
        if abs(dp[i][c] - dp[i - 1][c]) > 1e-9:
            selected_indices.append(i - 1)
            c -= weights[i - 1]

    selected_indices.reverse()
    selected_names = [item_names[idx] if item_names else f"Item-{idx}" for idx in selected_indices]
    return dp[n][capacity], selected_indices, selected_names


def knapsack_01_brute_force(weights: List[int], values: List[float], capacity: int) -> float:
    """Brute force recursive 0/1 Knapsack. Time Complexity: O(2^N)."""
    def _recurse(idx: int, rem_cap: int) -> float:
        if idx < 0 or rem_cap <= 0:
            return 0.0
        # Exclude
        res_ex = _recurse(idx - 1, rem_cap)
        # Include
        res_in = 0.0
        if weights[idx] <= rem_cap:
            res_in = values[idx] + _recurse(idx - 1, rem_cap - weights[idx])
        return max(res_ex, res_in)

    return _recurse(len(weights) - 1, capacity)


# ==============================================================================
# 2. Longest Common Subsequence (LCS) for Preference Matching
# ==============================================================================

def lcs_preference_matching(
    client_specs: List[str],
    supplier_capabilities: List[str]
) -> Tuple[int, List[str], float]:
    """
    Computes Longest Common Subsequence between client spec tags and supplier capabilities.
    Returns:
        - lcs_length: int
        - common_subsequence: List[str]
        - similarity_score: float in [0.0, 1.0] (Sorensen-Dice coefficient based on LCS)
    Time Complexity: O(M * N)
    Space Complexity: O(M * N)
    """
    m = len(client_specs)
    n = len(supplier_capabilities)

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if client_specs[i - 1] == supplier_capabilities[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Reconstruct LCS
    lcs_sequence = []
    i, j = m, n
    while i > 0 and j > 0:
        if client_specs[i - 1] == supplier_capabilities[j - 1]:
            lcs_sequence.append(client_specs[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    lcs_sequence.reverse()
    lcs_len = dp[m][n]
    denom = (m + n) if (m + n) > 0 else 1
    similarity = (2.0 * lcs_len) / denom
    return lcs_len, lcs_sequence, similarity


# ==============================================================================
# 3. Matrix Chain Multiplication (MCM) for Pipeline Optimization
# ==============================================================================

def matrix_chain_order_dp(dims: List[int], stage_names: Optional[List[str]] = None) -> Tuple[int, str]:
    """
    Optimizes multi-stage logistics processing transformation pipeline using MCM DP.
    dims: [p0, p1, p2, ..., pn] for n matrices/stages where stage i has dimension dims[i-1] x dims[i].
    Time Complexity: O(N^3)
    Space Complexity: O(N^2)
    Returns:
        - min_multiplications: minimum cost
        - optimal_parenthesization: string showing optimal sequence grouping
    """
    n = len(dims) - 1
    # m[i][j] stores minimum operations
    m = [[0] * n for _ in range(n)]
    # s[i][j] stores optimal split point k
    s = [[0] * n for _ in range(n)]

    for chain_len in range(2, n + 1):
        for i in range(n - chain_len + 1):
            j = i + chain_len - 1
            m[i][j] = sys.maxsize
            for k in range(i, j):
                cost = m[i][k] + m[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                if cost < m[i][j]:
                    m[i][j] = cost
                    s[i][j] = k

    names = stage_names if stage_names else [f"Stage{i+1}" for i in range(n)]

    def _build_parentheses(i: int, j: int) -> str:
        if i == j:
            return names[i]
        k = s[i][j]
        left_str = _build_parentheses(i, k)
        right_str = _build_parentheses(k + 1, j)
        return f"({left_str} * {right_str})"

    return m[0][n - 1], _build_parentheses(0, n - 1)


def matrix_chain_brute_force(dims: List[int]) -> int:
    """Recursive brute force MCM. Time Complexity: O(2^N) / Catalan number."""
    def _recurse(i: int, j: int) -> int:
        if i == j:
            return 0
        min_ops = sys.maxsize
        for k in range(i, j):
            cost = _recurse(i, k) + _recurse(k + 1, j) + dims[i] * dims[k + 1] * dims[j + 1]
            if cost < min_ops:
                min_ops = cost
        return min_ops

    return _recurse(0, len(dims) - 2)


# ==============================================================================
# 4. Resource Allocation Problem (RAP) for Demand Satisfaction
# ==============================================================================

def resource_allocation_dp(
    total_resources: int,
    utility_matrix: List[List[float]],
    target_names: Optional[List[str]] = None
) -> Tuple[float, List[int]]:
    """
    Resource Allocation Problem:
    Allocate 'total_resources' (e.g. delivery trucks or funding tranches) across M centers.
    utility_matrix[j][r] is the satisfaction utility if center j is given r resource units.
    Diminishing marginal returns are naturally handled.
    Time Complexity: O(M * R^2)
    Space Complexity: O(M * R)
    Returns:
        - max_total_utility: float
        - optimal_allocations: List[int] representing resource units given to each center
    """
    m = len(utility_matrix)  # number of centers
    r_max = total_resources

    # dp[j][r] = max utility from first (j+1) centers using at most r resources
    dp = [[0.0] * (r_max + 1) for _ in range(m)]
    decision = [[0] * (r_max + 1) for _ in range(m)]

    # Base case: first center (j = 0)
    for r in range(r_max + 1):
        dp[0][r] = utility_matrix[0][r]
        decision[0][r] = r

    # DP iterations for subsequent centers
    for j in range(1, m):
        for r in range(r_max + 1):
            best_val = -1.0
            best_alloc = 0
            for alloc in range(r + 1):
                val = dp[j - 1][r - alloc] + utility_matrix[j][alloc]
                if val > best_val:
                    best_val = val
                    best_alloc = alloc
            dp[j][r] = best_val
            decision[j][r] = best_alloc

    # Backtracking to reconstruct optimal allocation vector
    allocations = [0] * m
    remaining = r_max
    for j in range(m - 1, -1, -1):
        allocated = decision[j][remaining]
        allocations[j] = allocated
        remaining -= allocated

    return dp[m - 1][r_max], allocations


# ==============================================================================
# Demonstration & Performance Benchmarking
# ==============================================================================

def run_phase5_demo():
    from dataset.sample_data import DEMAND_RECORDS, SUPPLY_RECORDS

    print("================================================================================")
    print("PHASE 5 DEMO: Dynamic Programming Applications in Demand-Supply Matching")
    print("================================================================================")

    # --------------------------------------------------------------------------
    # 1. 0/1 Knapsack Demonstration
    # --------------------------------------------------------------------------
    print("\n--- 1. 0/1 Knapsack: Demand Allocation under Total Warehouse/Vehicle Capacity ---")
    weights = [d["quantity"] for d in DEMAND_RECORDS]
    # Value = urgency * quantity * 1.5
    values = [round(d["urgency"] * d["quantity"] * 1.5, 1) for d in DEMAND_RECORDS]
    item_names = [f"{d['id']} ({d['client'][:18]})" for d in DEMAND_RECORDS]
    truck_capacity = 220  # total units

    print(f"Vehicle Capacity Limit: {truck_capacity} units")
    print("Available Demand Requests:")
    for i in range(len(weights)):
        print(f"  [{i+1}] {item_names[i]:<28} | Required Qty: {weights[i]:>3} units | Utility Value: {values[i]:>6.1f}")

    # Run DP Knapsack
    t0 = time.perf_counter()
    max_val_dp, sel_indices, sel_names = knapsack_01_dp(weights, values, truck_capacity, item_names)
    t_dp = (time.perf_counter() - t0) * 1000

    # Run Brute Force Knapsack
    t0 = time.perf_counter()
    max_val_bf = knapsack_01_brute_force(weights, values, truck_capacity)
    t_bf = (time.perf_counter() - t0) * 1000

    total_weight_used = sum(weights[i] for i in sel_indices)
    print(f"\nOptimal 0/1 Knapsack Solution:")
    print(f"  Maximum Total Utility Achieved: {max_val_dp:.1f} (Brute Force Match: {max_val_bf:.1f})")
    print(f"  Vehicle Capacity Utilized: {total_weight_used}/{truck_capacity} units")
    print(f"  Selected Demands to Fulfill ({len(sel_indices)} requests):")
    for name in sel_names:
        print(f"    -> {name}")

    print(f"\n  Runtime Benchmarking (N={len(weights)}, W={truck_capacity}):")
    print(f"    DP Solver Time:          {t_dp:.4f} ms")
    print(f"    Brute-Force Solver Time: {t_bf:.4f} ms")

    # --------------------------------------------------------------------------
    # 2. LCS Demonstration for Specification Matching
    # --------------------------------------------------------------------------
    print("\n--- 2. Longest Common Subsequence (LCS): Specification / Preference Matching ---")
    client_reqs = ["sterile", "cold_chain", "express", "certified", "insured"]
    supplier_specs_A = ["cold_chain", "express", "certified"]
    supplier_specs_B = ["sterile", "standard_ground", "certified", "insured"]

    print(f"Client Spec Sequence:   {client_reqs}")
    for name, supp_specs in [("Supplier A (BioPharm)", supplier_specs_A), ("Supplier B (RegionalMed)", supplier_specs_B)]:
        lcs_len, lcs_seq, sim = lcs_preference_matching(client_reqs, supp_specs)
        print(f"\n  Evaluation vs {name}:")
        print(f"    Supplier Specs:       {supp_specs}")
        print(f"    LCS Matched Sequence: {lcs_seq} (Length: {lcs_len})")
        print(f"    Contract Match Score: {sim * 100:.1f}%")

    # --------------------------------------------------------------------------
    # 3. Matrix Chain Multiplication Demonstration
    # --------------------------------------------------------------------------
    print("\n--- 3. Matrix Chain Multiplication: Logistics Processing Pipeline Optimization ---")
    # Pipeline stages: Raw Intake (A1: 10x30), Sorting & Inspection (A2: 30x5), Packaging (A3: 5x60), Dispatch Load (A4: 60x10)
    pipeline_dims = [10, 30, 5, 60, 10]
    stage_labels = ["Intake", "Inspection", "Packaging", "Dispatch"]

    t0 = time.perf_counter()
    min_cost_dp, opt_sequence = matrix_chain_order_dp(pipeline_dims, stage_labels)
    t_mcm_dp = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    min_cost_bf = matrix_chain_brute_force(pipeline_dims)
    t_mcm_bf = (time.perf_counter() - t0) * 1000

    print(f"Pipeline Stage Dimensions: {pipeline_dims}")
    print(f"Minimum Computational/Coordination Cost: {min_cost_dp:,} scalar operations")
    print(f"Optimal Execution Hierarchy: {opt_sequence}")
    print(f"Runtime: DP = {t_mcm_dp:.4f} ms | Brute Force = {t_mcm_bf:.4f} ms")

    # --------------------------------------------------------------------------
    # 4. Resource Allocation Problem (RAP) Demonstration
    # --------------------------------------------------------------------------
    print("\n--- 4. Resource Allocation Problem: Multi-Center Utility Maximization ---")
    centers = ["North Emergency Clinic", "Central Trauma Center", "South Community Shelter"]
    fleet_vehicles = 6  # Total delivery trucks to allocate
    # Non-linear utility tables showing diminishing marginal returns:
    # utility[center][trucks_allocated]
    utility_data = [
        [0.0, 18.0, 32.0, 42.0, 48.0, 52.0, 55.0],  # Clinic
        [0.0, 25.0, 45.0, 60.0, 70.0, 75.0, 78.0],  # Trauma Center (high initial impact)
        [0.0, 12.0, 22.0, 30.0, 36.0, 40.0, 43.0]   # Community Shelter
    ]

    max_util, alloc_vec = resource_allocation_dp(fleet_vehicles, utility_data, centers)
    print(f"Total Available Transport Fleet: {fleet_vehicles} vehicles")
    print(f"Maximum Total Societal Utility: {max_util:.1f}")
    print("Optimal Fleet Distribution:")
    for i, c_name in enumerate(centers):
        units = alloc_vec[i]
        u = utility_data[i][units]
        print(f"  -> {c_name:<26}: {units} vehicles (Utility Contribution: {u:.1f})")

    # --------------------------------------------------------------------------
    # 5. Summary Complexity & Efficiency Comparison Table
    # --------------------------------------------------------------------------
    print("\n--- 5. Dynamic Programming vs Brute Force Complexity Comparison ---")
    print(f"{'DP Algorithm':<30} | {'Brute Force Complexity':<24} | {'Dynamic Programming':<22}")
    print("-" * 82)
    print(f"{'0/1 Knapsack':<30} | {'O(2^N)':<24} | {'O(N * W)':<22}")
    print(f"{'Longest Common Subsequence':<30} | {'O(2^(M+N))':<24} | {'O(M * N)':<22}")
    print(f"{'Matrix Chain Multiplication':<30} | {'O(4^N / N^(3/2)) (Catalan)':<24} | {'O(N^3)':<22}")
    print(f"{'Resource Allocation Problem':<30} | {'O(C(K+M-1, M-1))':<24} | {'O(M * K^2)':<22}")


if __name__ == "__main__":
    run_phase5_demo()
