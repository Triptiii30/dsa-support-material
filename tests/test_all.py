"""
Comprehensive Unit & Integration Test Suite for Demand-Supply Matching Prototype.
Covers Phases 1 through 6.
"""

import os
import sys
import unittest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from modules.phase1_structures import AVLTree, MaxBinaryHeap
from modules.phase2_graph import Graph
from modules.phase3_mst import kruskal_mst, prim_mst
from modules.phase4_shortest_path import dijkstra, bellman_ford, floyd_warshall, reconstruct_floyd_path
from modules.phase5_dp import (
    knapsack_01_dp,
    knapsack_01_brute_force,
    lcs_preference_matching,
    matrix_chain_order_dp,
    matrix_chain_brute_force,
    resource_allocation_dp
)
from modules.phase6_matching_engine import DemandSupplyMatchingEngine
from dataset.sample_data import DEMAND_RECORDS, SUPPLY_RECORDS, LOGISTICS_NODES, LOGISTICS_EDGES


class TestPhase1DataStructures(unittest.TestCase):
    def test_avl_tree_balance_and_operations(self):
        avl = AVLTree(key_attribute_name="price")
        values = [50, 20, 80, 10, 30, 70, 90, 5, 15, 25, 35]
        for val in values:
            avl.insert(val, {"id": f"item_{val}", "price": val})

        # Check balance factor of root
        bf = avl._get_balance(avl.root)
        self.assertIn(bf, [-1, 0, 1])

        # Exact search
        res = avl.search(30)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["price"], 30)

        # Range query [20, 70]
        rq = avl.range_query(20, 70)
        keys = [k for k, _ in rq]
        self.assertTrue(all(20 <= k <= 70 for k in keys))
        self.assertIn(20, keys)
        self.assertIn(70, keys)

        # Deletion
        deleted = avl.delete(20)
        self.assertTrue(deleted)
        self.assertEqual(len(avl.search(20)), 0)
        self.assertIn(avl._get_balance(avl.root), [-1, 0, 1])

    def test_binary_max_heap(self):
        heap = MaxBinaryHeap()
        heap.push(10.0, "D1")
        heap.push(50.0, "D2")
        heap.push(30.0, "D3")
        heap.push(100.0, "D4")

        self.assertEqual(heap.peek().priority, 100.0)
        self.assertEqual(heap.pop_max().data, "D4")
        self.assertEqual(heap.pop_max().data, "D2")
        self.assertEqual(heap.pop_max().data, "D3")
        self.assertEqual(heap.pop_max().data, "D1")
        self.assertTrue(heap.is_empty())


class TestPhase2Graph(unittest.TestCase):
    def test_bfs_dfs_and_connectivity(self):
        g = Graph(directed=False)
        g.add_edge("A", "B", 1.0)
        g.add_edge("B", "C", 2.0)
        g.add_edge("C", "A", 3.0)
        # Separate island
        g.add_edge("X", "Y", 4.0)

        components = g.find_connected_components()
        self.assertEqual(len(components), 2)

        bfs_order, bfs_tree = g.bfs("A")
        self.assertEqual(set(bfs_order), {"A", "B", "C"})
        self.assertEqual(len(bfs_tree), 2)

        dfs_order, dfs_tree = g.dfs("A")
        self.assertEqual(set(dfs_order), {"A", "B", "C"})
        self.assertEqual(len(dfs_tree), 2)


class TestPhase3MST(unittest.TestCase):
    def test_kruskal_and_prim_equivalence(self):
        g = Graph(directed=False)
        for n in LOGISTICS_NODES:
            g.add_node(n)
        for u, v, cost, _ in LOGISTICS_EDGES:
            g.add_edge(u, v, cost)

        k_edges, k_cost, _ = kruskal_mst(g)
        p_edges, p_cost, _ = prim_mst(g, "North_Hub")

        self.assertAlmostEqual(k_cost, p_cost, places=4)
        self.assertEqual(len(k_edges), len(g.nodes) - 1)
        self.assertEqual(len(p_edges), len(g.nodes) - 1)


class TestPhase4ShortestPath(unittest.TestCase):
    def test_dijkstra_bellman_floyd(self):
        g = Graph(directed=False)
        for n in LOGISTICS_NODES:
            g.add_node(n)
        for u, v, cost, _ in LOGISTICS_EDGES:
            g.add_edge(u, v, cost)

        # Dijkstra
        dijk = dijkstra(g, "North_Hub")
        self.assertEqual(dijk["North_Hub"][0], 0.0)
        self.assertEqual(dijk["Airport_Logistics_Center"][0], 15.0)

        # Bellman-Ford with negative edge
        edges = [
            ("A", "B", 4.0),
            ("B", "C", -2.0),
            ("A", "C", 5.0)
        ]
        dists, paths, has_neg = bellman_ford(["A", "B", "C"], edges, "A")
        self.assertFalse(has_neg)
        self.assertEqual(dists["C"], 2.0)  # A -> B (4) -> C (-2) = 2.0 < 5.0

        # Floyd-Warshall
        dist_mat, next_mat, idx_map = floyd_warshall(LOGISTICS_NODES, LOGISTICS_EDGES)
        c, path = reconstruct_floyd_path("North_Hub", "Airport_Logistics_Center", LOGISTICS_NODES, dist_mat, next_mat, idx_map)
        self.assertEqual(c, 15.0)
        self.assertEqual(path, ["North_Hub", "Airport_Logistics_Center"])


class TestPhase5DynamicProgramming(unittest.TestCase):
    def test_knapsack_01(self):
        weights = [10, 20, 30]
        values = [60.0, 100.0, 120.0]
        cap = 50
        dp_val, sel_idx, _ = knapsack_01_dp(weights, values, cap)
        bf_val = knapsack_01_brute_force(weights, values, cap)
        self.assertEqual(dp_val, 220.0)
        self.assertEqual(dp_val, bf_val)
        self.assertEqual(sel_idx, [1, 2])

    def test_lcs(self):
        s1 = ["sterile", "cold_chain", "express"]
        s2 = ["standard", "cold_chain", "express", "certified"]
        lcs_len, lcs_seq, sim = lcs_preference_matching(s1, s2)
        self.assertEqual(lcs_len, 2)
        self.assertEqual(lcs_seq, ["cold_chain", "express"])
        self.assertAlmostEqual(sim, (2 * 2) / (3 + 4), places=4)

    def test_matrix_chain_multiplication(self):
        dims = [10, 20, 30, 40, 30]
        dp_cost, opt_paren = matrix_chain_order_dp(dims)
        bf_cost = matrix_chain_brute_force(dims)
        self.assertEqual(dp_cost, 30000)
        self.assertEqual(dp_cost, bf_cost)

    def test_resource_allocation(self):
        # 2 centers, 3 resources
        util = [
            [0.0, 10.0, 18.0, 24.0],
            [0.0, 12.0, 20.0, 26.0]
        ]
        max_u, alloc = resource_allocation_dp(3, util)
        self.assertEqual(sum(alloc), 3)
        self.assertEqual(max_u, 30.0)  # Center 0 gets 1 (10) + Center 1 gets 2 (20) = 30


from modules.phase7_tsp_branch_bound import (
    solve_tsp_branch_and_bound,
    solve_logistics_tsp,
    reduce_matrix
)
from modules.phase8_bplus_tree import (
    BPlusTree,
    build_catalog_bplus_tree
)


class TestPhase6IntegratedEngine(unittest.TestCase):
    def test_engine_end_to_end(self):
        engine = DemandSupplyMatchingEngine()
        engine.load_dataset(DEMAND_RECORDS, SUPPLY_RECORDS)
        matches = engine.execute_matching_pipeline()
        self.assertGreater(len(matches), 0)

        # Ensure all matches respect price bound
        for m in matches:
            self.assertLessEqual(m.supplier["unit_price"], m.demand["max_price"])
            self.assertEqual(m.supplier["category"], m.demand["category"])
            self.assertGreater(len(m.transit_path), 0)

        # Test Knapsack optimization
        max_util, sel = engine.optimize_dispatch_knapsack(150)
        self.assertGreater(max_util, 0)
        self.assertLessEqual(sum(m.allocated_qty for m in sel), 150)


class TestPhase7TSPBranchAndBound(unittest.TestCase):
    def test_4_city_known_optimal(self):
        inf = float("inf")
        matrix_4 = [
            [inf, 10.0, 15.0, 20.0],
            [10.0, inf, 35.0, 25.0],
            [15.0, 35.0, inf, 30.0],
            [20.0, 25.0, 30.0, inf]
        ]
        res = solve_tsp_branch_and_bound(matrix_4)
        self.assertEqual(res["best_cost"], 80.0)
        self.assertEqual(len(res["best_path_indices"]), 5)  # 4 cities + return to start
        self.assertEqual(res["best_path_indices"][0], res["best_path_indices"][-1])
        self.assertLessEqual(res["initial_lower_bound"], 80.0)
        self.assertGreater(res["branches_pruned"], 0)

    def test_5_city_textbook_optimal(self):
        inf = float("inf")
        matrix_5 = [
            [inf, 20.0, 30.0, 10.0, 11.0],
            [15.0, inf, 16.0, 4.0, 2.0],
            [3.0, 5.0, inf, 2.0, 4.0],
            [19.0, 6.0, 18.0, inf, 3.0],
            [16.0, 4.0, 7.0, 16.0, inf]
        ]
        res = solve_tsp_branch_and_bound(matrix_5)
        self.assertEqual(res["best_cost"], 28.0)
        self.assertEqual(len(res["best_path_indices"]), 6)  # 5 cities + return to start
        self.assertEqual(res["best_path_indices"][0], res["best_path_indices"][-1])
        self.assertLessEqual(res["initial_lower_bound"], 28.0)
        self.assertGreater(res["branches_pruned"], 0)

    def test_logistics_tsp_route(self):
        hubs = ["North_Hub", "Airport_Logistics_Center", "Central_Square", "Tech_Park", "East_District"]
        res = solve_logistics_tsp(hubs)
        self.assertGreater(res["best_cost"], 0.0)
        self.assertEqual(len(res["best_path_names"]), len(hubs) + 1)
        self.assertEqual(res["best_path_names"][0], res["best_path_names"][-1])
        self.assertEqual(len(res["route_legs"]), len(hubs))
        self.assertLessEqual(res["initial_lower_bound"], res["best_cost"])
        self.assertGreater(res["branches_pruned"], 0)


class TestPhase8BPlusTree(unittest.TestCase):
    def test_bplus_insert_and_node_splits(self):
        tree = BPlusTree(order=3)
        keys = [50, 20, 80, 10, 30, 70, 90, 40, 60]
        for k in keys:
            tree.insert(k, f"Val_{k}")

        summary = tree.get_structure_summary()
        self.assertGreater(summary["depth"], 1)
        self.assertGreater(summary["internal_nodes"], 0)
        self.assertGreater(summary["leaf_nodes"], 1)

    def test_bplus_search_exact_and_missing(self):
        tree = BPlusTree(order=3)
        tree.insert(100, {"name": "Product_100"})
        tree.insert(200, {"name": "Product_200"})

        found = tree.search(100)
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0]["name"], "Product_100")

        missing = tree.search(999)
        self.assertEqual(len(missing), 0)

    def test_bplus_ordered_traversal(self):
        tree = BPlusTree(order=3)
        keys = [45, 12, 89, 34, 7, 65, 23, 90, 56]
        for k in keys:
            tree.insert(k, k)

        traversal = tree.ordered_traversal()
        extracted_keys = [k for k, _ in traversal]
        self.assertEqual(extracted_keys, sorted(keys))

    def test_bplus_range_query(self):
        tree = BPlusTree(order=3)
        for val in range(10, 101, 10):
            tree.insert(val, f"Item_{val}")

        # Range query [25, 75] -> expected [30, 40, 50, 60, 70]
        res = tree.range_query(25, 75)
        res_keys = [k for k, _ in res]
        self.assertEqual(res_keys, [30, 40, 50, 60, 70])

    def test_bplus_catalog_indexing(self):
        tree = build_catalog_bplus_tree(SUPPLY_RECORDS, key_field="unit_price", order=3)
        summary = tree.get_structure_summary()
        self.assertEqual(summary["total_records"], len(SUPPLY_RECORDS))

        # Search for known price 88.0 (Titan Heavy Foundries)
        found = tree.search(88.0)
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0]["supplier"], "Titan Heavy Foundries")


if __name__ == "__main__":
    unittest.main()

