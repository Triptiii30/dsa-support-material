"""
Automated Unit Tests for API Service endpoints.
Verifies contract integrity, schema compliance, and status codes.
"""

import os
import sys
import unittest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from modules.api_service import (
    dispatch_api_request,
    get_initial_data,
    run_matching,
    get_mst,
    get_shortest_path
)


class TestApiService(unittest.TestCase):
    def test_initial_data_contract(self):
        code, data = dispatch_api_request("/api/initial-data", {})
        self.assertEqual(code, 200)
        self.assertIn("demands", data)
        self.assertIn("supplies", data)
        self.assertIn("nodes", data)
        self.assertIn("edges", data)
        self.assertIn("directed_edges", data)
        self.assertGreater(len(data["demands"]), 0)
        self.assertGreater(len(data["supplies"]), 0)

    def test_run_matching_endpoint(self):
        code, data = dispatch_api_request("/api/run-matching", {"capacity": ["250"]})
        self.assertEqual(code, 200)
        self.assertIn("matches", data)
        self.assertIn("mst_cost", data)
        self.assertIn("knapsack_selected", data)
        self.assertEqual(data["knapsack_capacity"], 250)
        self.assertGreater(len(data["matches"]), 0)

    def test_mst_endpoint(self):
        code, data = dispatch_api_request("/api/mst", {})
        self.assertEqual(code, 200)
        self.assertIn("kruskal", data)
        self.assertIn("prim", data)
        self.assertAlmostEqual(data["kruskal"]["cost"], data["prim"]["cost"], places=2)
        self.assertGreater(len(data["kruskal"]["edges"]), 0)

    def test_shortest_path_dijkstra(self):
        code, data = dispatch_api_request(
            "/api/shortest-path",
            {"source": ["North_Hub"], "algo": ["dijkstra"]}
        )
        self.assertEqual(code, 200)
        self.assertEqual(data["algorithm"], "Dijkstra")
        self.assertIn("results", data)
        self.assertIn("Airport_Logistics_Center", data["results"])
        self.assertEqual(data["results"]["Airport_Logistics_Center"]["cost"], 15.0)

    def test_shortest_path_bellman_ford(self):
        code, data = dispatch_api_request(
            "/api/shortest-path",
            {"source": ["North_Hub"], "algo": ["bellman"]}
        )
        self.assertEqual(code, 200)
        self.assertEqual(data["algorithm"], "Bellman-Ford")
        self.assertFalse(data["has_negative_cycle"])
        self.assertIn("results", data)

    def test_tsp_route_endpoint(self):
        code, data = dispatch_api_request("/api/tsp-route", {})
        self.assertEqual(code, 200)
        self.assertIn("best_cost", data)
        self.assertIn("best_path_names", data)
        self.assertIn("selected_locations", data)
        self.assertIn("branches_pruned", data)
        self.assertGreater(data["best_cost"], 0.0)

    def test_bplus_catalog_endpoint(self):
        # 1. Ordered traversal
        code, data = dispatch_api_request("/api/bplus-catalog", {})
        self.assertEqual(code, 200)
        self.assertEqual(data["query_type"], "ordered_traversal")
        self.assertGreater(len(data["matches"]), 0)

        # 2. Range query
        code, data = dispatch_api_request(
            "/api/bplus-catalog",
            {"min_price": ["35.0"], "max_price": ["120.0"]}
        )
        self.assertEqual(code, 200)
        self.assertEqual(data["query_type"], "range_query")
        for m in data["matches"]:
            self.assertTrue(35.0 <= m["price"] <= 120.0)

        # 3. Exact search
        code, data = dispatch_api_request(
            "/api/bplus-catalog",
            {"search_price": ["88.0"]}
        )
        self.assertEqual(code, 200)
        self.assertEqual(data["query_type"], "exact_search")
        self.assertEqual(len(data["matches"]), 1)
        self.assertEqual(data["matches"][0]["supplier"], "Titan Heavy Foundries")

    def test_not_found_endpoint(self):
        code, data = dispatch_api_request("/api/unknown-endpoint", {})
        self.assertEqual(code, 404)
        self.assertIn("error", data)


if __name__ == "__main__":
    unittest.main()
