"""
Phase 6: Prototype Integration
Demand-Supply Matching Engine integrating:
- AVL Tree (Price/Urgency Indexing)
- Binary Max-Heap (Priority Queue for Demands)
- Graph Connectivity & Clustering (BFS/DFS)
- Minimum Spanning Tree (Kruskal/Prim Logistics Backbone)
- Shortest Path Routing (Dijkstra & Bellman-Ford)
- Dynamic Programming (LCS Spec Matching, 0/1 Knapsack Fleet Allocation, Resource Allocation)
"""

import os
import sys
import time
from typing import Dict, List, Tuple, Any, Optional

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from modules.phase1_structures import AVLTree, MaxBinaryHeap
from modules.phase2_graph import Graph
from modules.phase3_mst import kruskal_mst, prim_mst
from modules.phase4_shortest_path import dijkstra, bellman_ford, floyd_warshall
from modules.phase5_dp import (
    lcs_preference_matching,
    knapsack_01_dp,
    matrix_chain_order_dp,
    resource_allocation_dp
)
from dataset.sample_data import (
    DEMAND_RECORDS,
    SUPPLY_RECORDS,
    LOGISTICS_NODES,
    LOGISTICS_EDGES,
    DIRECTED_LOGISTICS_WITH_DISCOUNTS
)


class MatchResult:
    """Represents a matched pair between a demand and a supplier."""
    def __init__(
        self,
        demand: Dict[str, Any],
        supplier: Dict[str, Any],
        match_score: float,
        lcs_matched_tags: List[str],
        spec_similarity: float,
        transit_cost: float,
        transit_path: List[str],
        allocated_qty: int,
        total_contract_cost: float
    ):
        self.demand = demand
        self.supplier = supplier
        self.match_score = match_score
        self.lcs_matched_tags = lcs_matched_tags
        self.spec_similarity = spec_similarity
        self.transit_cost = transit_cost
        self.transit_path = transit_path
        self.allocated_qty = allocated_qty
        self.total_contract_cost = total_contract_cost


class DemandSupplyMatchingEngine:
    """
    Unified end-to-end Demand-Supply Matching Engine.
    Combines AVL Indexing, Priority Queues, Graph Algorithms, and Dynamic Programming.
    """
    def __init__(self):
        # Phase 1: Core Data Structures
        self.supply_price_avl = AVLTree(key_attribute_name="unit_price")
        self.demand_priority_heap = MaxBinaryHeap()

        # Phase 2: Logistics Graph
        self.network = Graph(directed=False)
        self._init_network()

        # Catalog state
        self.demands: List[Dict[str, Any]] = []
        self.supplies: List[Dict[str, Any]] = []
        self.matches: List[MatchResult] = []

    def _init_network(self):
        """Builds regional logistics graph from dataset."""
        for node in LOGISTICS_NODES:
            self.network.add_node(node)
        for u, v, cost, _ in LOGISTICS_EDGES:
            self.network.add_edge(u, v, cost)

    def load_dataset(self, demands: List[Dict[str, Any]], supplies: List[Dict[str, Any]]):
        """Loads dataset and builds data structures."""
        self.demands = [dict(d) for d in demands]
        self.supplies = [dict(s) for s in supplies]

        # Index supplies in AVL Tree by price
        for s in self.supplies:
            self.supply_price_avl.insert(s["unit_price"], s)

        # Enqueue demands in Binary Max-Heap by composite priority score
        # Priority Score = Urgency * 10 + (max_price * 0.1)
        for d in self.demands:
            score = d["urgency"] * 10.0 + (d["max_price"] * 0.1)
            self.demand_priority_heap.push(score, d)

    def execute_matching_pipeline(self) -> List[MatchResult]:
        """
        Executes end-to-end matching:
        1. Extract demands in priority order from Heap.
        2. Query AVL tree for price-compatible suppliers.
        3. Validate graph reachability via connected components / BFS.
        4. Calculate lowest-cost logistics routing via Dijkstra.
        5. Evaluate specification compatibility using LCS DP.
        6. Compute composite score and allocate available quantities.
        """
        self.matches = []
        # Precompute all-pairs shortest paths
        supplier_inventory = {s["id"]: s["available_qty"] for s in self.supplies}
        supplier_by_id = {s["id"]: s for s in self.supplies}

        # Work on a copy of priority heap
        temp_heap = MaxBinaryHeap()
        for item in self.demand_priority_heap.heap:
            temp_heap.push(item.priority, item.data)

        # Process demands in priority order
        while not temp_heap.is_empty():
            heap_item = temp_heap.pop_max()
            demand = heap_item.data
            req_qty = demand["quantity"]
            client_loc = demand["location"]

            # Compute shortest paths from demand location to all hubs
            dijkstra_paths = dijkstra(self.network, source=client_loc)

            # Step 1: Query AVL tree for suppliers with price <= demand.max_price
            price_candidates = self.supply_price_avl.range_query(min_key=0.0, max_key=demand["max_price"])

            best_match: Optional[MatchResult] = None
            highest_score: float = -1.0

            for _, sup_list in price_candidates:
                for s in sup_list:
                    # Category filter
                    if s["category"] != demand["category"]:
                        continue

                    # Stock availability check
                    if supplier_inventory[s["id"]] <= 0:
                        continue

                    sup_loc = s["location"]
                    # Reachability & Shortest Route via Dijkstra
                    if sup_loc not in dijkstra_paths or dijkstra_paths[sup_loc][0] == float('inf'):
                        continue  # Not physically reachable in network

                    transit_cost, transit_path = dijkstra_paths[sup_loc]

                    # Specification matching via LCS DP
                    lcs_len, lcs_seq, spec_similarity = lcs_preference_matching(
                        demand["tags"], s["tags"]
                    )

                    # Multi-attribute scoring:
                    # Price savings ratio
                    price_saving = (demand["max_price"] - s["unit_price"]) / demand["max_price"]
                    # Proximity score (cheaper transit is better; normalizer = $100)
                    proximity_score = max(0.0, 1.0 - (transit_cost / 100.0))

                    # Composite Match Score: 40% Spec LCS + 30% Price Advantage + 30% Logistics Proximity
                    composite_score = (
                        0.40 * spec_similarity +
                        0.30 * price_saving +
                        0.30 * proximity_score
                    )

                    if composite_score > highest_score:
                        highest_score = composite_score
                        alloc_qty = min(req_qty, supplier_inventory[s["id"]])
                        total_cost = (alloc_qty * s["unit_price"]) + transit_cost

                        best_match = MatchResult(
                            demand=demand,
                            supplier=s,
                            match_score=composite_score,
                            lcs_matched_tags=lcs_seq,
                            spec_similarity=spec_similarity,
                            transit_cost=transit_cost,
                            transit_path=transit_path,
                            allocated_qty=alloc_qty,
                            total_contract_cost=total_cost
                        )

            if best_match:
                # Deduct inventory
                supplier_inventory[best_match.supplier["id"]] -= best_match.allocated_qty
                self.matches.append(best_match)

        return self.matches

    def compute_network_mst(self) -> Tuple[List[Tuple[str, str, float]], float]:
        """Calculates global minimum cost infrastructure spanning tree for logistics."""
        mst_edges, total_cost, _ = kruskal_mst(self.network)
        return mst_edges, total_cost

    def optimize_dispatch_knapsack(self, vehicle_capacity: int) -> Tuple[float, List[MatchResult]]:
        """
        Applies 0/1 Knapsack DP to select the optimal set of matched orders
        that maximizes fulfilled urgency utility under limited vehicle/depot cargo capacity.
        """
        if not self.matches:
            return 0.0, []

        weights = [m.allocated_qty for m in self.matches]
        # Value = urgency * allocated_qty * (1 + match_score)
        values = [
            round(m.demand["urgency"] * m.allocated_qty * (1.0 + m.match_score), 1)
            for m in self.matches
        ]
        names = [f"{m.demand['id']}->{m.supplier['id']}" for m in self.matches]

        max_val, sel_indices, _ = knapsack_01_dp(weights, values, vehicle_capacity, names)
        selected_matches = [self.matches[i] for i in sel_indices]
        return max_val, selected_matches


def print_banner(title: str):
    width = 90
    print("\n" + "=" * width)
    print(f" {title.upper()} ".center(width, "="))
    print("=" * width)


def run_phase6_integrated_demo():
    print_banner("Phase 6 Prototype Integration: Demand-Supply Matching Engine")

    engine = DemandSupplyMatchingEngine()
    engine.load_dataset(DEMAND_RECORDS, SUPPLY_RECORDS)

    print(f"\n[+] Loaded {len(DEMAND_RECORDS)} Demand Contracts and {len(SUPPLY_RECORDS)} Supplier Catalogs.")
    print(f"[+] AVL Price Index & Binary Urgency Heap constructed.")

    # 1. Connected Clusters
    print("\n" + "-" * 90)
    print("STEP 1: LOGISTICS NETWORK CONNECTIVITY & CLUSTERS (PHASE 2)")
    print("-" * 90)
    clusters = engine.network.find_connected_components()
    for idx, c in enumerate(clusters, 1):
        print(f"  Cluster {idx} ({len(c)} nodes): {', '.join(c)}")

    # 2. End-to-End Matching Pipeline
    print("\n" + "-" * 90)
    print("STEP 2: MULTI-ATTRIBUTE MATCHING PIPELINE (AVL + HEAP + LCS + DIJKSTRA)")
    print("-" * 90)
    t0 = time.perf_counter()
    matches = engine.execute_matching_pipeline()
    match_time = (time.perf_counter() - t0) * 1000

    print(f"Successfully matched {len(matches)}/{len(DEMAND_RECORDS)} demand requests in {match_time:.3f} ms:\n")

    print(f"{'Demand ID':<10} | {'Client':<22} | {'Supplier':<22} | {'Score':<6} | {'Route':<22} | {'Cost':<10}")
    print("-" * 105)
    for m in matches:
        d = m.demand
        s = m.supplier
        route_str = f"{d['location'][:8]}->{s['location'][:8]}"
        print(
            f"{d['id']:<10} | {d['client'][:22]:<22} | {s['supplier'][:22]:<22} | "
            f"{m.match_score*100:>5.1f}% | {route_str:<22} | ${m.total_contract_cost:>8.2f}"
        )

    print("\nDetailed Match Specifications & Routing Breakdown:")
    for idx, m in enumerate(matches, 1):
        d = m.demand
        s = m.supplier
        print(f"\n  Match #{idx}: [{d['id']}] {d['client']}  <===>  [{s['id']}] {s['supplier']}")
        print(f"    Category:        {d['category']}")
        print(f"    Quantity:        {m.allocated_qty} units (Demand: {d['quantity']} | Stock: {s['available_qty']})")
        print(f"    Pricing:         Offered ${s['unit_price']:.2f} <= Budget ${d['max_price']:.2f}")
        print(f"    Spec LCS Tags:   {m.lcs_matched_tags} (Compatibility: {m.spec_similarity*100:.1f}%)")
        print(f"    Dijkstra Route:  {' -> '.join(m.transit_path)} (Transit Cost: ${m.transit_cost:.2f})")
        print(f"    Total Cost:      ${m.total_contract_cost:.2f} | Match Quality Score: {m.match_score*100:.2f}/100")

    # 3. Minimum Cost Backbone (MST)
    print("\n" + "-" * 90)
    print("STEP 3: REGIONAL LOGISTICS BACKBONE VIA MINIMUM SPANNING TREE (PHASE 3)")
    print("-" * 90)
    mst_edges, mst_cost = engine.compute_network_mst()
    print(f"Total Minimum Infrastructure Cost: ${mst_cost:.2f}")
    print(f"Selected MST Arteries ({len(mst_edges)} links):")
    for u, v, w in mst_edges:
        print(f"  [{u}] <--- ${w:.1f} ---> [{v}]")

    # 4. Constrained Vehicle Fleet Allocation (0/1 Knapsack DP)
    print("\n" + "-" * 90)
    print("STEP 4: FLEET CAPACITY OPTIMIZATION VIA 0/1 KNAPSACK (PHASE 5)")
    print("-" * 90)
    truck_cap = 250  # Available vehicle load limit
    total_requested_units = sum(m.allocated_qty for m in matches)
    print(f"Total Requested Allocation: {total_requested_units} units")
    print(f"Dispatch Cargo Constraint:   {truck_cap} units")

    max_util, sel_matches = engine.optimize_dispatch_knapsack(truck_cap)
    allocated_units = sum(m.allocated_qty for m in sel_matches)
    print(f"\nOptimization Result:")
    print(f"  Selected Demands: {len(sel_matches)}/{len(matches)} fulfilled within capacity")
    print(f"  Capacity Utilized: {allocated_units}/{truck_cap} units ({(allocated_units/truck_cap)*100:.1f}%)")
    print(f"  Total Urgency Utility Index: {max_util:.2f}")
    for m in sel_matches:
        print(f"    -> [{m.demand['id']}] {m.demand['client']} ({m.allocated_qty} units | Urgency: {m.demand['urgency']}/10)")


if __name__ == "__main__":
    run_phase6_integrated_demo()
