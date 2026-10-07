"""
Phase 2: Graph Traversal & Connectivity
- Adjacency List & Adjacency Matrix representations.
- Breadth-First Search (BFS) and Depth-First Search (DFS).
- Connected Components (clusters of demand-supply nodes).
- Spanning Tree generation (BFS and DFS Spanning Trees).
"""

import os
import sys
from collections import deque
from typing import Dict, List, Set, Tuple, Optional, Any

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


class Graph:
    """
    Versatile Graph class supporting both Adjacency List and Adjacency Matrix.
    Used for modeling regional logistics networks, demand clusters, and supply routes.
    """
    def __init__(self, directed: bool = False):
        self.directed: bool = directed
        self.nodes: List[str] = []
        self.node_index_map: Dict[str, int] = {}
        self.adj_list: Dict[str, List[Tuple[str, float]]] = {}
        self.edges: List[Tuple[str, str, float]] = []

    def add_node(self, node: str) -> None:
        """Add a node (location / hub / cluster) to the graph."""
        if node not in self.node_index_map:
            self.node_index_map[node] = len(self.nodes)
            self.nodes.append(node)
            self.adj_list[node] = []

    def add_edge(self, u: str, v: str, weight: float = 1.0) -> None:
        """Add a weighted edge between u and v."""
        self.add_node(u)
        self.add_node(v)

        self.adj_list[u].append((v, weight))
        self.edges.append((u, v, weight))

        if not self.directed:
            self.adj_list[v].append((u, weight))
            self.edges.append((v, u, weight))

    def get_adjacency_matrix(self) -> Tuple[List[str], List[List[float]]]:
        """
        Generates and returns (node_list, matrix).
        Inf or 0 indicates absence of edge.
        """
        n = len(self.nodes)
        inf = float('inf')
        matrix = [[inf] * n for _ in range(n)]

        for i in range(n):
            matrix[i][i] = 0.0

        for u, neighbors in self.adj_list.items():
            u_idx = self.node_index_map[u]
            for v, w in neighbors:
                v_idx = self.node_index_map[v]
                matrix[u_idx][v_idx] = min(matrix[u_idx][v_idx], w)

        return self.nodes, matrix

    def print_adjacency_matrix(self) -> str:
        """Returns formatted string of the adjacency matrix."""
        headers, mat = self.get_adjacency_matrix()
        short_headers = [h[:8] for h in headers]
        lines = []
        header_row = f"{'':10} | " + " | ".join(f"{h:8}" for h in short_headers)
        lines.append(header_row)
        lines.append("-" * len(header_row))
        for i, row in enumerate(mat):
            row_str = f"{headers[i][:10]:10} | " + " | ".join(
                f"{val:8.1f}" if val != float('inf') else f"{'INF':>8}" for val in row
            )
            lines.append(row_str)
        return "\n".join(lines)

    # --------------------------------------------------------------------------
    # BFS Traversal
    # --------------------------------------------------------------------------
    def bfs(self, start_node: str) -> Tuple[List[str], List[Tuple[str, str, float]]]:
        """
        Breadth-First Search traversal starting from start_node.
        Returns:
            - traversal_order: list of nodes visited in order
            - tree_edges: edges included in the BFS spanning tree (u, v, weight)
        """
        if start_node not in self.adj_list:
            return [], []

        visited: Set[str] = set([start_node])
        queue: deque[str] = deque([start_node])
        traversal_order: List[str] = []
        tree_edges: List[Tuple[str, str, float]] = []

        while queue:
            curr = queue.popleft()
            traversal_order.append(curr)

            for neighbor, weight in self.adj_list[curr]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    tree_edges.append((curr, neighbor, weight))
                    queue.append(neighbor)

        return traversal_order, tree_edges

    # --------------------------------------------------------------------------
    # DFS Traversal
    # --------------------------------------------------------------------------
    def dfs(self, start_node: str) -> Tuple[List[str], List[Tuple[str, str, float]]]:
        """
        Depth-First Search traversal starting from start_node.
        Returns:
            - traversal_order: list of nodes visited in order
            - tree_edges: edges included in the DFS spanning tree (u, v, weight)
        """
        if start_node not in self.adj_list:
            return [], []

        visited: Set[str] = set()
        traversal_order: List[str] = []
        tree_edges: List[Tuple[str, str, float]] = []

        def _dfs_util(curr: str):
            visited.add(curr)
            traversal_order.append(curr)

            for neighbor, weight in self.adj_list[curr]:
                if neighbor not in visited:
                    tree_edges.append((curr, neighbor, weight))
                    _dfs_util(neighbor)

        _dfs_util(start_node)
        return traversal_order, tree_edges

    # --------------------------------------------------------------------------
    # Connected Components (Clusters)
    # --------------------------------------------------------------------------
    def find_connected_components(self) -> List[List[str]]:
        """
        Finds all connected components (isolated clusters or regional subnetworks).
        Returns a list of components, where each component is a list of node names.
        """
        visited: Set[str] = set()
        components: List[List[str]] = []

        for node in self.nodes:
            if node not in visited:
                comp_nodes, _ = self.bfs(node)
                visited.update(comp_nodes)
                components.append(comp_nodes)

        return components

    # --------------------------------------------------------------------------
    # Spanning Tree Generation
    # --------------------------------------------------------------------------
    def generate_spanning_tree(self, start_node: str, method: str = "bfs") -> List[Tuple[str, str, float]]:
        """
        Generates a spanning tree starting from start_node using BFS or DFS.
        """
        if method.lower() == "dfs":
            _, edges = self.dfs(start_node)
        else:
            _, edges = self.bfs(start_node)
        return edges


def run_phase2_demo():
    from dataset.sample_data import LOGISTICS_NODES, LOGISTICS_EDGES

    print("================================================================================")
    print("PHASE 2 DEMO: Graph Traversal & Connectivity (BFS, DFS, Clusters, Spanning Trees)")
    print("================================================================================")

    # Initialize Logistics Network Graph
    network = Graph(directed=False)
    for n in LOGISTICS_NODES:
        network.add_node(n)

    for u, v, cost, _ in LOGISTICS_EDGES:
        network.add_edge(u, v, cost)

    # Also add an isolated regional sub-cluster to demonstrate multi-cluster detection
    isolated_nodes = ["Offshore_Island_Port", "Island_Medical_Post"]
    for n in isolated_nodes:
        network.add_node(n)
    network.add_edge("Offshore_Island_Port", "Island_Medical_Post", 8.0)

    print(f"\n1. Graph Topology Loaded: {len(network.nodes)} Nodes, {len(network.edges)//2} Undirected Edges")
    print("\nAdjacency Matrix Sample (First 6 Nodes):")
    nodes, mat = network.get_adjacency_matrix()
    sub_headers = nodes[:6]
    print(f"{'':25} | " + " | ".join(f"{h[:7]:7}" for h in sub_headers))
    print("-" * 75)
    for i in range(6):
        row_str = f"{nodes[i][:25]:25} | " + " | ".join(
            f"{mat[i][j]:7.1f}" if mat[i][j] != float('inf') else f"{'INF':>7}" for j in range(6)
        )
        print(row_str)

    # Connected Components
    print("\n--- 2. Connected Components (Supply & Demand Network Clusters) ---")
    components = network.find_connected_components()
    for idx, comp in enumerate(components, 1):
        print(f"  Cluster {idx} ({len(comp)} nodes):")
        print(f"    Nodes: {', '.join(comp)}")

    # BFS Traversal
    start_hub = "North_Hub"
    print(f"\n--- 3. Breadth-First Search (BFS) Traversal from [{start_hub}] ---")
    bfs_order, bfs_tree = network.bfs(start_hub)
    print(f"  BFS Visit Order: {' -> '.join(bfs_order)}")
    print(f"  BFS Spanning Tree Edges ({len(bfs_tree)} edges):")
    bfs_total_cost = 0.0
    for u, v, w in bfs_tree:
        bfs_total_cost += w
        print(f"    ({u}) <--- ${w:.1f} ---> ({v})")
    print(f"  BFS Spanning Tree Total Weight: ${bfs_total_cost:.1f}")

    # DFS Traversal
    print(f"\n--- 4. Depth-First Search (DFS) Traversal from [{start_hub}] ---")
    dfs_order, dfs_tree = network.dfs(start_hub)
    print(f"  DFS Visit Order: {' -> '.join(dfs_order)}")
    print(f"  DFS Spanning Tree Edges ({len(dfs_tree)} edges):")
    dfs_total_cost = 0.0
    for u, v, w in dfs_tree:
        dfs_total_cost += w
        print(f"    ({u}) <--- ${w:.1f} ---> ({v})")
    print(f"  DFS Spanning Tree Total Weight: ${dfs_total_cost:.1f}")


if __name__ == "__main__":
    run_phase2_demo()
