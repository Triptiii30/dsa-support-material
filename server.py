"""
Lightweight Python Backend & Web Server for Demand-Supply Matching Prototype.
Serves static frontend (HTML/CSS/JS) and provides JSON API endpoints
connecting the UI to the actual Python DSA modules.
"""

import os
import sys
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from dataset.sample_data import (
    DEMAND_RECORDS,
    SUPPLY_RECORDS,
    LOGISTICS_NODES,
    LOGISTICS_EDGES,
    DIRECTED_LOGISTICS_WITH_DISCOUNTS
)
from modules.phase1_structures import AVLTree, MaxBinaryHeap
from modules.phase2_graph import Graph
from modules.phase3_mst import kruskal_mst, prim_mst
from modules.phase4_shortest_path import dijkstra, bellman_ford, floyd_warshall, reconstruct_floyd_path
from modules.phase5_dp import (
    knapsack_01_dp,
    lcs_preference_matching,
    matrix_chain_order_dp,
    resource_allocation_dp
)
from modules.phase6_matching_engine import DemandSupplyMatchingEngine


WEB_DIR = os.path.join(PROJECT_ROOT, "web")


class DSAApiHandler(SimpleHTTPRequestHandler):
    """Custom request handler serving static files and handling /api requests."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)

        if parsed_path.path == "/api/initial-data":
            self._send_json({
                "demands": DEMAND_RECORDS,
                "supplies": SUPPLY_RECORDS,
                "nodes": LOGISTICS_NODES,
                "edges": LOGISTICS_EDGES,
                "directed_edges": DIRECTED_LOGISTICS_WITH_DISCOUNTS
            })
        elif parsed_path.path == "/api/run-matching":
            query = urllib.parse.parse_qs(parsed_path.query)
            capacity = int(query.get("capacity", [250])[0])

            engine = DemandSupplyMatchingEngine()
            engine.load_dataset(DEMAND_RECORDS, SUPPLY_RECORDS)
            matches = engine.execute_matching_pipeline()
            mst_edges, mst_cost = engine.compute_network_mst()
            max_util, knapsack_sel = engine.optimize_dispatch_knapsack(capacity)

            serialized_matches = []
            for m in matches:
                serialized_matches.append({
                    "demand_id": m.demand["id"],
                    "client": m.demand["client"],
                    "demand_loc": m.demand["location"],
                    "category": m.demand["category"],
                    "quantity": m.demand["quantity"],
                    "budget": m.demand["max_price"],
                    "urgency": m.demand["urgency"],
                    "supplier_id": m.supplier["id"],
                    "supplier_name": m.supplier["supplier"],
                    "supplier_loc": m.supplier["location"],
                    "unit_price": m.supplier["unit_price"],
                    "match_score": round(m.match_score * 100, 2),
                    "lcs_tags": m.lcs_matched_tags,
                    "spec_similarity": round(m.spec_similarity * 100, 1),
                    "transit_cost": m.transit_cost,
                    "transit_path": m.transit_path,
                    "allocated_qty": m.allocated_qty,
                    "total_contract_cost": m.total_contract_cost
                })

            serialized_knapsack = [
                {
                    "demand_id": m.demand["id"],
                    "client": m.demand["client"],
                    "allocated_qty": m.allocated_qty,
                    "urgency": m.demand["urgency"],
                    "total_cost": m.total_contract_cost
                }
                for m in knapsack_sel
            ]

            self._send_json({
                "matches": serialized_matches,
                "mst_cost": mst_cost,
                "mst_edges": [{"u": u, "v": v, "w": w} for u, v, w in mst_edges],
                "knapsack_capacity": capacity,
                "knapsack_utility": round(max_util, 2),
                "knapsack_selected": serialized_knapsack
            })
        elif parsed_path.path == "/api/mst":
            network = Graph(directed=False)
            for n in LOGISTICS_NODES:
                network.add_node(n)
            for u, v, cost, _ in LOGISTICS_EDGES:
                network.add_edge(u, v, cost)

            k_edges, k_cost, k_stats = kruskal_mst(network)
            p_edges, p_cost, p_stats = prim_mst(network, "North_Hub")

            self._send_json({
                "kruskal": {
                    "cost": k_cost,
                    "edges": [{"u": u, "v": v, "w": w} for u, v, w in k_edges],
                    "runtime_ms": round(k_stats["runtime_ms"], 4),
                    "edges_evaluated": k_stats["edges_considered"]
                },
                "prim": {
                    "cost": p_cost,
                    "edges": [{"u": u, "v": v, "w": w} for u, v, w in p_edges],
                    "runtime_ms": round(p_stats["runtime_ms"], 4),
                    "edges_evaluated": p_stats["edges_considered"]
                }
            })
        elif parsed_path.path == "/api/shortest-path":
            query = urllib.parse.parse_qs(parsed_path.query)
            source = query.get("source", ["North_Hub"])[0]
            algo = query.get("algo", ["dijkstra"])[0]

            network = Graph(directed=False)
            for n in LOGISTICS_NODES:
                network.add_node(n)
            for u, v, cost, _ in LOGISTICS_EDGES:
                network.add_edge(u, v, cost)

            if algo == "bellman":
                dists, paths, has_neg = bellman_ford(
                    LOGISTICS_NODES,
                    DIRECTED_LOGISTICS_WITH_DISCOUNTS,
                    source
                )
                self._send_json({
                    "source": source,
                    "algorithm": "Bellman-Ford",
                    "has_negative_cycle": has_neg,
                    "results": {
                        dest: {"cost": dists[dest], "path": paths[dest]}
                        for dest in LOGISTICS_NODES
                    }
                })
            else:
                dijk_res = dijkstra(network, source)
                self._send_json({
                    "source": source,
                    "algorithm": "Dijkstra",
                    "results": {
                        dest: {"cost": dijk_res[dest][0], "path": dijk_res[dest][1]}
                        for dest in LOGISTICS_NODES
                    }
                })
        else:
            # Fallback to static file serving
            super().do_GET()

    def _send_json(self, data: dict):
        response_bytes = json.dumps(data).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(response_bytes)


def run_server(port: int = 8000):
    server_address = ("", port)
    httpd = HTTPServer(server_address, DSAApiHandler)
    print(f"================================================================================")
    print(f" Demand-Supply Matching Web Server Running at: http://localhost:{port}/")
    print(f" Press Ctrl+C to stop the server.")
    print(f"================================================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
        httpd.server_close()


if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    run_server(port)
