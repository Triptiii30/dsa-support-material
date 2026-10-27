"""
Phase 7: Unit 4 - Travelling Salesman Problem (TSP) using Branch and Bound
- Implementation of Least-Cost Branch and Bound (LCBB) with Matrix Reduction.
- Genuine lower-bound calculation and state space tree branch pruning.
- Verification on benchmark instances with known optimal solutions.
- Application to the regional logistics delivery network for optimal multi-stop dispatch.
"""

import os
import sys
import copy
import heapq
import time
from typing import List, Tuple, Dict, Any, Optional

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from dataset.sample_data import LOGISTICS_NODES, LOGISTICS_EDGES
from modules.phase4_shortest_path import floyd_warshall


class TSPNode:
    """
    Represents a search state in the Branch and Bound State Space Tree.
    """
    def __init__(
        self,
        path: List[int],
        reduced_matrix: List[List[float]],
        cost: float,
        vertex: int,
        level: int
    ):
        self.path: List[int] = path
        self.reduced_matrix: List[List[float]] = reduced_matrix
        self.cost: float = cost
        self.vertex: int = vertex
        self.level: int = level

    def __lt__(self, other: "TSPNode") -> bool:
        return self.cost < other.cost


def reduce_matrix(matrix: List[List[float]]) -> Tuple[List[List[float]], float]:
    """
    Reduces the cost matrix by subtracting row and column minimums.
    Returns:
        reduced_matrix: Reduced 2D cost matrix.
        reduction_cost: Sum of all subtracted row and column minimums (lower bound contribution).
    """
    n = len(matrix)
    mat = [row[:] for row in matrix]
    total_reduction = 0.0

    # 1. Row reduction: Subtract min element of each row
    for i in range(n):
        row_min = float("inf")
        for j in range(n):
            if mat[i][j] < row_min:
                row_min = mat[i][j]
        if row_min != float("inf") and row_min > 0:
            for j in range(n):
                if mat[i][j] != float("inf"):
                    mat[i][j] -= row_min
            total_reduction += row_min

    # 2. Column reduction: Subtract min element of each column
    for j in range(n):
        col_min = float("inf")
        for i in range(n):
            if mat[i][j] < col_min:
                col_min = mat[i][j]
        if col_min != float("inf") and col_min > 0:
            for i in range(n):
                if mat[i][j] != float("inf"):
                    mat[i][j] -= col_min
            total_reduction += col_min

    return mat, total_reduction


def solve_tsp_branch_and_bound(
    cost_matrix: List[List[float]],
    node_names: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Solves the Travelling Salesman Problem using Least-Cost Branch and Bound (LCBB).
    Features genuine lower-bound bounding and branch pruning.

    Args:
        cost_matrix: N x N distance/cost matrix with float('inf') on diagonals.
        node_names: Optional human-readable labels for the vertices.

    Returns:
        Dictionary containing optimal tour, cost, initial lower bound, nodes explored,
        branches pruned, and execution time in milliseconds.
    """
    start_time = time.perf_counter()
    n = len(cost_matrix)
    if node_names is None:
        node_names = [f"Location_{i}" for i in range(n)]

    # Compute root matrix reduction and initial lower bound
    root_matrix, initial_lower_bound = reduce_matrix(cost_matrix)

    # Root state in State Space Tree
    root = TSPNode(
        path=[0],
        reduced_matrix=root_matrix,
        cost=initial_lower_bound,
        vertex=0,
        level=1
    )

    # Priority queue stores tuples: (lower_bound, level, counter, node)
    pq: List[Tuple[float, int, int, TSPNode]] = []
    counter = 0
    heapq.heappush(pq, (root.cost, root.level, counter, root))

    best_cost = float("inf")
    best_path_indices: List[int] = []
    nodes_explored = 0
    branches_pruned = 0
    tree_trace: List[Dict[str, Any]] = []

    while pq:
        _, _, _, curr = heapq.heappop(pq)
        nodes_explored += 1

        # If current node's lower bound meets or exceeds best tour found, prune
        if curr.cost >= best_cost:
            branches_pruned += 1
            continue

        # Reached leaf level: all N vertices visited
        if curr.level == n:
            last_v = curr.vertex
            start_v = curr.path[0]
            # Check edge back to starting depot
            if cost_matrix[last_v][start_v] != float("inf"):
                complete_tour = curr.path + [start_v]
                actual_cost = sum(
                    cost_matrix[complete_tour[i]][complete_tour[i + 1]]
                    for i in range(n)
                )
                if actual_cost < best_cost:
                    best_cost = actual_cost
                    best_path_indices = complete_tour
                    tree_trace.append({
                        "event": "NEW_BEST_TOUR",
                        "tour": [node_names[idx] for idx in complete_tour],
                        "cost": actual_cost
                    })
            continue

        # Branching step: generate child states for all unvisited vertices
        curr_v = curr.vertex
        for next_v in range(n):
            if next_v not in curr.path and cost_matrix[curr_v][next_v] != float("inf"):
                edge_cost = curr.reduced_matrix[curr_v][next_v]
                if edge_cost == float("inf"):
                    continue

                # Child matrix transformation:
                # 1. Set row curr_v to infinity (cannot leave curr_v again)
                # 2. Set col next_v to infinity (cannot enter next_v again)
                # 3. Set child[next_v][start_v] to infinity to prevent premature subtour
                child_mat = [row[:] for row in curr.reduced_matrix]
                for j in range(n):
                    child_mat[curr_v][j] = float("inf")
                for i in range(n):
                    child_mat[i][next_v] = float("inf")

                if curr.level < n - 1:
                    child_mat[next_v][0] = float("inf")

                # Reduce child matrix to determine incremental bound
                reduced_child, child_red_cost = reduce_matrix(child_mat)
                child_bound = curr.cost + edge_cost + child_red_cost

                # Branch and Bound Pruning Test
                if child_bound < best_cost:
                    counter += 1
                    child_node = TSPNode(
                        path=curr.path + [next_v],
                        reduced_matrix=reduced_child,
                        cost=child_bound,
                        vertex=next_v,
                        level=curr.level + 1
                    )
                    heapq.heappush(
                        pq,
                        (child_bound, child_node.level, counter, child_node)
                    )
                else:
                    branches_pruned += 1

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    best_path_names = [node_names[i] for i in best_path_indices]

    # Calculate individual leg transit costs
    route_legs = []
    if best_path_indices:
        for i in range(len(best_path_indices) - 1):
            u_idx = best_path_indices[i]
            v_idx = best_path_indices[i + 1]
            leg_cost = cost_matrix[u_idx][v_idx]
            route_legs.append({
                "from": node_names[u_idx],
                "to": node_names[v_idx],
                "cost": leg_cost
            })

    return {
        "best_cost": best_cost,
        "best_path_indices": best_path_indices,
        "best_path_names": best_path_names,
        "route_legs": route_legs,
        "nodes_explored": nodes_explored,
        "branches_pruned": branches_pruned,
        "initial_lower_bound": initial_lower_bound,
        "runtime_ms": elapsed_ms,
        "tree_trace": tree_trace
    }


def solve_logistics_tsp(
    selected_hubs: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Applies TSP Branch and Bound route optimization to the real-world logistics network.
    Uses Floyd-Warshall all-pairs shortest path matrix as the underlying distance metric.

    Args:
        selected_hubs: Subset of hub locations to visit. Defaults to 5 core distribution centers.

    Returns:
        Optimized tour itinerary, individual legs, total transit cost, and bounding statistics.
    """
    if selected_hubs is None:
        selected_hubs = [
            "North_Hub",
            "Airport_Logistics_Center",
            "Tech_Park",
            "Central_Square",
            "East_District"
        ]

    # Compute APSP distance matrix over regional network
    dist_mat, _, node_index_map = floyd_warshall(
        LOGISTICS_NODES,
        LOGISTICS_EDGES,
        directed=False
    )

    k = len(selected_hubs)
    inf = float("inf")
    sub_matrix: List[List[float]] = [[inf] * k for _ in range(k)]

    for i, u in enumerate(selected_hubs):
        u_idx = node_index_map[u]
        for j, v in enumerate(selected_hubs):
            if i != j:
                v_idx = node_index_map[v]
                sub_matrix[i][j] = float(dist_mat[u_idx][v_idx])

    result = solve_tsp_branch_and_bound(sub_matrix, node_names=selected_hubs)
    result["selected_locations"] = selected_hubs
    return result


def run_phase7_demo():
    """Demonstration runner for Phase 7 (Unit 4: TSP Branch and Bound)."""
    print("================================================================================")
    print("PHASE 7 DEMO: Unit 4 - Travelling Salesman Problem using Branch & Bound (LCBB)")
    print("================================================================================")

    # Verification 1: Standard 4-City Benchmark Graph with known optimal cost = 80
    print("\n--- 1. Verification on Standard 4-City Benchmark Graph ---")
    inf = float("inf")
    benchmark_4 = [
        [inf, 10.0, 15.0, 20.0],
        [10.0, inf, 35.0, 25.0],
        [15.0, 35.0, inf, 30.0],
        [20.0, 25.0, 30.0, inf]
    ]
    b4_names = ["City_A", "City_B", "City_C", "City_D"]
    res4 = solve_tsp_branch_and_bound(benchmark_4, node_names=b4_names)
    print(f"  Benchmark 4-City Locations: {', '.join(b4_names)}")
    print(f"  Initial Lower Bound:        ${res4['initial_lower_bound']:.2f}")
    print(f"  Optimal Tour:               {' -> '.join(res4['best_path_names'])}")
    print(f"  Optimal Route Cost:         ${res4['best_cost']:.2f}")
    print(f"  State Space Nodes Explored: {res4['nodes_explored']}")
    print(f"  Sub-optimal Branches Pruned:{res4['branches_pruned']}")
    print(f"  Runtime:                    {res4['runtime_ms']:.4f} ms")
    assert res4["best_cost"] == 80.0, f"Expected 80.0, got {res4['best_cost']}"
    print("  [PASS] Mathematical verification: 80.0 == known optimal solution.")

    # Verification 2: Standard 5-City Textbook Instance with known optimal cost = 28
    print("\n--- 2. Verification on Standard 5-City Textbook Instance ---")
    benchmark_5 = [
        [inf, 20.0, 30.0, 10.0, 11.0],
        [15.0, inf, 16.0, 4.0, 2.0],
        [3.0, 5.0, inf, 2.0, 4.0],
        [19.0, 6.0, 18.0, inf, 3.0],
        [16.0, 4.0, 7.0, 16.0, inf]
    ]
    b5_names = ["Depot_1", "Depot_2", "Depot_3", "Depot_4", "Depot_5"]
    res5 = solve_tsp_branch_and_bound(benchmark_5, node_names=b5_names)
    print(f"  Benchmark 5-City Locations: {', '.join(b5_names)}")
    print(f"  Initial Lower Bound:        ${res5['initial_lower_bound']:.2f}")
    print(f"  Optimal Tour:               {' -> '.join(res5['best_path_names'])}")
    print(f"  Optimal Route Cost:         ${res5['best_cost']:.2f}")
    print(f"  State Space Nodes Explored: {res5['nodes_explored']}")
    print(f"  Sub-optimal Branches Pruned:{res5['branches_pruned']}")
    print(f"  Runtime:                    {res5['runtime_ms']:.4f} ms")
    assert res5["best_cost"] == 28.0, f"Expected 28.0, got {res5['best_cost']}"
    print("  [PASS] Mathematical verification: 28.0 == known textbook solution.")

    # Production Application: Regional Logistics Multi-Stop Dispatch
    print("\n--- 3. Production Application: Multi-Stop Logistics Route Optimization ---")
    hubs = [
        "North_Hub",
        "Airport_Logistics_Center",
        "Central_Square",
        "Tech_Park",
        "East_District"
    ]
    logistics_res = solve_logistics_tsp(hubs)
    print(f"  Selected Delivery Locations ({len(hubs)} hubs):")
    for i, h in enumerate(hubs, 1):
        print(f"    {i}. {h}")
    print(f"\n  Initial Lower Bound:         ${logistics_res['initial_lower_bound']:.2f}")
    print(f"  Optimal Delivery Route:      {' -> '.join(logistics_res['best_path_names'])}")
    print(f"  Total Closed-Tour Cost:      ${logistics_res['best_cost']:.2f}")
    print("\n  Segment-by-Segment Transit Leg Breakdown:")
    for leg in logistics_res["route_legs"]:
        print(f"    [{leg['from']:24}] ---> [{leg['to']:24}] : ${leg['cost']:.2f}")
    print(f"\n  Search Space Nodes Explored: {logistics_res['nodes_explored']}")
    print(f"  Branches Pruned by B&B:      {logistics_res['branches_pruned']}")
    print(f"  Optimization Runtime:        {logistics_res['runtime_ms']:.4f} ms")


if __name__ == "__main__":
    run_phase7_demo()
