"""
Phase 3: Minimum Cost Spanning Trees (MST)
- Kruskal's Algorithm with Disjoint Set Union (Path Compression + Union by Rank) - optimal for sparse graphs.
- Prim's Algorithm using Min-Priority Queue - optimal for dense graphs.
- Minimum-cost allocation network generation.
- Performance and complexity comparison.
"""

import os
import sys
import time
import heapq
from typing import Dict, List, Set, Tuple, Optional, Any

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from modules.phase2_graph import Graph


# ==============================================================================
# 1. Disjoint Set Union (DSU / Union-Find) with Path Compression & Union by Rank
# ==============================================================================

class DisjointSetUnion:
    """Disjoint Set Union (Union-Find) data structure."""
    def __init__(self, elements: List[str]):
        self.parent: Dict[str, str] = {x: x for x in elements}
        self.rank: Dict[str, int] = {x: 0 for x in elements}

    def find(self, i: str) -> str:
        """Find representative with path compression (nearly O(1) amortized, alpha(N))."""
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, root_x: str, root_y: str) -> bool:
        """Union two sets by rank. Returns True if united, False if already in same set."""
        rx = self.find(root_x)
        ry = self.find(root_y)

        if rx == ry:
            return False

        # Union by rank heuristic
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1

        return True


# ==============================================================================
# 2. Kruskal's Algorithm
# ==============================================================================

def kruskal_mst(graph: Graph) -> Tuple[List[Tuple[str, str, float]], float, Dict[str, Any]]:
    """
    Kruskal's MST algorithm.
    Time Complexity: O(E log E) or O(E log V).
    Space Complexity: O(V + E).
    Ideal for sparse graphs where E << V^2.
    """
    start_time = time.perf_counter()

    # Collect unique undirected edges
    seen_edges = set()
    unique_edges = []
    for u, v, w in graph.edges:
        edge_key = tuple(sorted([u, v]))
        if edge_key not in seen_edges:
            seen_edges.add(edge_key)
            unique_edges.append((w, u, v))

    # Sort edges non-decreasingly by weight
    unique_edges.sort(key=lambda x: x[0])

    dsu = DisjointSetUnion(graph.nodes)
    mst_edges: List[Tuple[str, str, float]] = []
    total_cost: float = 0.0
    edges_considered = 0

    for weight, u, v in unique_edges:
        edges_considered += 1
        if dsu.union(u, v):
            mst_edges.append((u, v, weight))
            total_cost += weight
            if len(mst_edges) == len(graph.nodes) - 1:
                break

    elapsed = (time.perf_counter() - start_time) * 1000  # ms
    stats = {
        "algorithm": "Kruskal",
        "edges_considered": edges_considered,
        "total_edges": len(unique_edges),
        "mst_edge_count": len(mst_edges),
        "runtime_ms": elapsed
    }
    return mst_edges, total_cost, stats


# ==============================================================================
# 3. Prim's Algorithm
# ==============================================================================

def prim_mst(graph: Graph, start_node: Optional[str] = None) -> Tuple[List[Tuple[str, str, float]], float, Dict[str, Any]]:
    """
    Prim's MST algorithm using Min-Priority Queue (Binary Min-Heap).
    Time Complexity: O((V + E) log V) = O(E log V).
    Space Complexity: O(V + E).
    Ideal for dense graphs where E is close to V^2.
    """
    start_time = time.perf_counter()

    if not graph.nodes:
        return [], 0.0, {"runtime_ms": 0.0}

    start = start_node if start_node and start_node in graph.nodes else graph.nodes[0]

    visited: Set[str] = set()
    mst_edges: List[Tuple[str, str, float]] = []
    total_cost: float = 0.0
    edges_considered = 0

    # Min-Heap stores tuples of (weight, u, v) where u is in MST and v is prospective
    min_heap: List[Tuple[float, str, str]] = []

    def _add_edges_from(node: str):
        visited.add(node)
        for neighbor, weight in graph.adj_list.get(node, []):
            if neighbor not in visited:
                heapq.heappush(min_heap, (weight, node, neighbor))

    _add_edges_from(start)

    while min_heap and len(visited) < len(graph.nodes):
        weight, u, v = heapq.heappop(min_heap)
        edges_considered += 1

        if v in visited:
            continue

        # Add edge to MST
        mst_edges.append((u, v, weight))
        total_cost += weight
        _add_edges_from(v)

    elapsed = (time.perf_counter() - start_time) * 1000  # ms
    stats = {
        "algorithm": "Prim",
        "edges_considered": edges_considered,
        "mst_edge_count": len(mst_edges),
        "runtime_ms": elapsed
    }
    return mst_edges, total_cost, stats


# ==============================================================================
# Demonstration & Performance Comparison
# ==============================================================================

def run_phase3_demo():
    from dataset.sample_data import LOGISTICS_NODES, LOGISTICS_EDGES

    print("================================================================================")
    print("PHASE 3 DEMO: Minimum Cost Spanning Trees (Prim vs Kruskal)")
    print("================================================================================")

    network = Graph(directed=False)
    for n in LOGISTICS_NODES:
        network.add_node(n)
    for u, v, cost, _ in LOGISTICS_EDGES:
        network.add_edge(u, v, cost)

    print(f"Logistics Network: {len(network.nodes)} Nodes, {len(LOGISTICS_EDGES)} Available Edges")

    # Run Kruskal's
    k_edges, k_cost, k_stats = kruskal_mst(network)
    print(f"\n--- 1. Kruskal's Algorithm Result ---")
    print(f"Total Minimum Infrastructure/Transit Cost: ${k_cost:.2f}")
    print(f"Edges Selected ({len(k_edges)} edges):")
    for u, v, w in k_edges:
        print(f"  [{u}] <====== ${w:.1f} ======> [{v}]")
    print(f"Stats: Edges Evaluated={k_stats['edges_considered']}, Time={k_stats['runtime_ms']:.4f} ms")

    # Run Prim's
    p_edges, p_cost, p_stats = prim_mst(network, start_node="North_Hub")
    print(f"\n--- 2. Prim's Algorithm Result ---")
    print(f"Total Minimum Infrastructure/Transit Cost: ${p_cost:.2f}")
    print(f"Edges Selected ({len(p_edges)} edges):")
    for u, v, w in p_edges:
        print(f"  [{u}] <====== ${w:.1f} ======> [{v}]")
    print(f"Stats: Edges Evaluated={p_stats['edges_considered']}, Time={p_stats['runtime_ms']:.4f} ms")

    # Verification of MST Equivalence
    assert abs(k_cost - p_cost) < 1e-6, "Kruskal and Prim MST costs must match!"
    print(f"\nVerification Passed: Both Kruskal and Prim produced identical MST cost (${k_cost:.2f})!")

    # Performance & Complexity Comparison Table
    print("\n--- 3. Performance & Theoretical Complexity Comparison ---")
    print(f"{'Feature / Metric':<28} | {'Kruskal’s Algorithm':<26} | {'Prim’s Algorithm (Heap)':<26}")
    print("-" * 86)
    print(f"{'Time Complexity':<28} | {'O(E log E) or O(E log V)':<26} | {'O(E log V)':<26}")
    print(f"{'Space Complexity':<28} | {'O(V + E) for DSU & Edges':<26} | {'O(V + E) for Heap/Adjacency':<26}")
    print(f"{'Optimal Graph Type':<28} | {'Sparse Graphs (E << V^2)':<26} | {'Dense Graphs (E ~ V^2)':<26}")
    print(f"{'Core Data Structure':<28} | {'Disjoint Set Union (Rank+PC)':<26} | {'Binary Min-Heap Priority Queue':<26}")
    k_time_str = f"{k_stats['runtime_ms']:.4f} ms"
    p_time_str = f"{p_stats['runtime_ms']:.4f} ms"
    k_eval_str = f"{k_stats['edges_considered']}/{k_stats['total_edges']} edges"
    p_eval_str = f"{p_stats['edges_considered']} extractions"
    print(f"{'Network Sample Runtime':<28} | {k_time_str:<26} | {p_time_str:<26}")
    print(f"{'Edges Evaluated':<28} | {k_eval_str:<26} | {p_eval_str:<26}")


if __name__ == "__main__":
    run_phase3_demo()
