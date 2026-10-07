"""
Phase 4: Shortest Path Algorithms
- Dijkstra's Algorithm: Nearest supplier retrieval and lowest-cost logistics routing.
- Bellman-Ford Algorithm: Handling negative edge weights (discounts, green subsidies, route rebates) and detecting negative cycles.
- Floyd-Warshall Algorithm: All-pairs shortest path matrix across entire logistics network.
"""

import os
import sys
import heapq
from typing import Dict, List, Tuple, Optional, Any

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from modules.phase2_graph import Graph


# ==============================================================================
# 1. Dijkstra's Algorithm
# ==============================================================================

def dijkstra(graph: Graph, source: str, target: Optional[str] = None) -> Dict[str, Tuple[float, List[str]]]:
    """
    Dijkstra's Algorithm using Binary Min-Heap Priority Queue.
    Requires non-negative edge weights.
    Returns: Dict mapping destination_node -> (shortest_distance, [path_nodes])
    Time Complexity: O((V + E) log V)
    """
    if source not in graph.nodes:
        raise ValueError(f"Source node '{source}' not found in graph.")

    distances: Dict[str, float] = {node: float('inf') for node in graph.nodes}
    predecessors: Dict[str, Optional[str]] = {node: None for node in graph.nodes}
    distances[source] = 0.0

    # Min-heap stores (current_distance, node)
    pq: List[Tuple[float, str]] = [(0.0, source)]
    visited = set()

    while pq:
        curr_dist, curr_node = heapq.heappop(pq)

        if curr_node in visited:
            continue
        visited.add(curr_node)

        if target and curr_node == target:
            break

        for neighbor, weight in graph.adj_list.get(curr_node, []):
            if weight < 0:
                raise ValueError("Dijkstra does not support negative weights. Use Bellman-Ford instead.")

            new_dist = curr_dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                predecessors[neighbor] = curr_node
                heapq.heappush(pq, (new_dist, neighbor))

    # Reconstruct paths
    results: Dict[str, Tuple[float, List[str]]] = {}
    for dest in graph.nodes:
        if distances[dest] == float('inf'):
            results[dest] = (float('inf'), [])
            continue

        path = []
        curr: Optional[str] = dest
        while curr is not None:
            path.append(curr)
            curr = predecessors[curr]
        path.reverse()
        results[dest] = (distances[dest], path)

    return results


# ==============================================================================
# 2. Bellman-Ford Algorithm
# ==============================================================================

def bellman_ford(
    nodes: List[str],
    edges: List[Tuple[str, str, float]],
    source: str
) -> Tuple[Dict[str, float], Dict[str, List[str]], bool]:
    """
    Bellman-Ford Algorithm.
    Supports negative edge weights (such as green incentives, backhaul credits, bulk volume rebates).
    Detects negative weight cycles.
    Returns:
        - distances: Dict[node -> distance]
        - paths: Dict[node -> list of nodes in path]
        - has_negative_cycle: bool
    Time Complexity: O(V * E)
    """
    distances: Dict[str, float] = {node: float('inf') for node in nodes}
    predecessors: Dict[str, Optional[str]] = {node: None for node in nodes}
    distances[source] = 0.0

    # Relax all edges |V| - 1 times
    v_count = len(nodes)
    for _ in range(v_count - 1):
        relaxed_any = False
        for u, v, w in edges:
            if distances[u] != float('inf') and distances[u] + w < distances[v]:
                distances[v] = distances[u] + w
                predecessors[v] = u
                relaxed_any = True
        if not relaxed_any:
            break  # Early convergence optimization

    # Check for negative weight cycles (|V|-th relaxation iteration)
    has_negative_cycle = False
    for u, v, w in edges:
        if distances[u] != float('inf') and distances[u] + w < distances[v]:
            has_negative_cycle = True
            break

    # Reconstruct paths
    paths: Dict[str, List[str]] = {}
    for dest in nodes:
        if distances[dest] == float('inf'):
            paths[dest] = []
            continue

        path = []
        curr: Optional[str] = dest
        loop_guard = 0
        while curr is not None and loop_guard <= v_count:
            path.append(curr)
            curr = predecessors[curr]
            loop_guard += 1

        if loop_guard > v_count:
            # Trapped in negative cycle loop
            paths[dest] = ["[Negative Cycle Detected]"]
        else:
            path.reverse()
            paths[dest] = path

    return distances, paths, has_negative_cycle


# ==============================================================================
# 3. Floyd-Warshall Algorithm
# ==============================================================================

def floyd_warshall(
    nodes: List[str],
    edges: List[Tuple[str, str, float]],
    directed: bool = False
) -> Tuple[List[List[float]], List[List[Optional[int]]], Dict[str, int]]:
    """
    Floyd-Warshall Algorithm for All-Pairs Shortest Paths.
    Returns:
        - dist_matrix: N x N distance table
        - next_node: N x N predecessor/next intermediate matrix for full path reconstruction
        - node_idx: Dict mapping node_name -> index
    Time Complexity: O(V^3)
    Space Complexity: O(V^2)
    """
    n = len(nodes)
    node_idx = {name: i for i, name in enumerate(nodes)}
    inf = float('inf')

    # Initialize matrices
    dist = [[inf] * n for _ in range(n)]
    next_node = [[None] * n for _ in range(n)]

    for i in range(n):
        dist[i][i] = 0.0
        next_node[i][i] = i

    for edge in edges:
        u, v, w = edge[0], edge[1], edge[2]
        if u in node_idx and v in node_idx:
            i, j = node_idx[u], node_idx[v]
            if w < dist[i][j]:
                dist[i][j] = w
                next_node[i][j] = j
            if not directed:
                if w < dist[j][i]:
                    dist[j][i] = w
                    next_node[j][i] = i

    # DP all-pairs relaxation
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] != inf and dist[k][j] != inf:
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        next_node[i][j] = next_node[i][k]

    return dist, next_node, node_idx


def reconstruct_floyd_path(
    u: str,
    v: str,
    nodes: List[str],
    dist: List[List[float]],
    next_node: List[List[Optional[int]]],
    node_idx: Dict[str, int]
) -> Tuple[float, List[str]]:
    """Reconstructs shortest path between u and v from Floyd-Warshall next matrix."""
    i, j = node_idx[u], node_idx[v]
    if dist[i][j] == float('inf'):
        return float('inf'), []

    path = [u]
    curr = i
    while curr != j:
        curr = next_node[curr][j]
        if curr is None:
            return float('inf'), []
        path.append(nodes[curr])

    return dist[i][j], path


# ==============================================================================
# Demonstration & Nearest Supplier Retrieval
# ==============================================================================

def run_phase4_demo():
    from dataset.sample_data import (
        LOGISTICS_NODES,
        LOGISTICS_EDGES,
        DIRECTED_LOGISTICS_WITH_DISCOUNTS,
        SUPPLY_RECORDS
    )

    print("================================================================================")
    print("PHASE 4 DEMO: Shortest Path Algorithms (Dijkstra, Bellman-Ford, Floyd-Warshall)")
    print("================================================================================")

    # 1. Dijkstra on Undirected Logistics Network
    network = Graph(directed=False)
    for n in LOGISTICS_NODES:
        network.add_node(n)
    for u, v, cost, _ in LOGISTICS_EDGES:
        network.add_edge(u, v, cost)

    demand_hub = "North_Hub"
    print(f"\n--- 1. Dijkstra's Algorithm: Nearest Supplier Retrieval for Demand Hub [{demand_hub}] ---")
    dijkstra_results = dijkstra(network, source=demand_hub)

    # Find closest supplier facilities
    supplier_locations = {s["location"]: s for s in SUPPLY_RECORDS}
    print(f"{'Target Supplier Location':<28} | {'Min Transit Cost':<18} | {'Optimal Route'}")
    print("-" * 80)
    for loc, s_record in supplier_locations.items():
        cost, path = dijkstra_results[loc]
        path_str = " -> ".join(path)
        print(f"{loc:<28} | ${cost:<17.2f} | {path_str}")

    # 2. Bellman-Ford with Negative Weight Discounts & Green Subsidies
    print(f"\n--- 2. Bellman-Ford Algorithm: Handling Route Subsidies & Negative Edge Credits ---")
    bf_source = "Airport_Logistics_Center"
    print(f"Source Hub: [{bf_source}]")
    print("Included Subsidies: Central_Square -> Rural_Depot (-$8.00 green credit), Airport -> Central (-$5.00 backhaul)")

    bf_dists, bf_paths, has_neg_cycle = bellman_ford(
        nodes=LOGISTICS_NODES,
        edges=DIRECTED_LOGISTICS_WITH_DISCOUNTS,
        source=bf_source
    )

    print(f"Negative Cycle Detected: {has_neg_cycle}")
    print(f"{'Destination Hub':<26} | {'Effective Cost (with credits)':<30} | {'Subsidized Route'}")
    print("-" * 86)
    for dest in LOGISTICS_NODES:
        cost = bf_dists[dest]
        path_str = " -> ".join(bf_paths[dest]) if bf_paths[dest] else "No path"
        cost_str = f"${cost:.2f}" if cost != float('inf') else "Unreachable"
        print(f"{dest:<26} | {cost_str:<30} | {path_str}")

    # 3. Floyd-Warshall All-Pairs Transit Matrix
    print(f"\n--- 3. Floyd-Warshall Algorithm: All-Pairs Shortest Path Matrix ---")
    fw_dist, fw_next, fw_idx = floyd_warshall(LOGISTICS_NODES, LOGISTICS_EDGES, directed=False)

    sample_hubs = ["North_Hub", "Central_Square", "Tech_Park", "South_Port", "Rural_Depot"]
    print(f"{'Origin \\ Dest':<16} | " + " | ".join(f"{h[:8]:8}" for h in sample_hubs))
    print("-" * 65)
    for orig in sample_hubs:
        row_vals = []
        for dest in sample_hubs:
            c = fw_dist[fw_idx[orig]][fw_idx[dest]]
            row_vals.append(f"${c:6.1f}" if c != float('inf') else "  INF  ")
        print(f"{orig[:16]:<16} | " + " | ".join(row_vals))

    # Path reconstruction example from Floyd-Warshall
    orig, dest = "Rural_Depot", "Harbor_Terminal"
    c, path = reconstruct_floyd_path(orig, dest, LOGISTICS_NODES, fw_dist, fw_next, fw_idx)
    print(f"\nFloyd-Warshall Reconstructed Multi-Hop Route from [{orig}] to [{dest}]:")
    print(f"  Cost: ${c:.2f} | Path: {' -> '.join(path)}")


if __name__ == "__main__":
    run_phase4_demo()
