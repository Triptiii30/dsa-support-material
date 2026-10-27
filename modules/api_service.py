"""
Unified API Service & Business Logic Handler for Demand-Supply Matching Prototype.
Eliminates duplication across local development servers (server.py) and cloud
serverless entry points (api/index.py).
"""

import os
import sys
from typing import Dict, Any, Tuple, List

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from dataset.sample_data import (
    DEMAND_RECORDS,
    SUPPLY_RECORDS,
    LOGISTICS_NODES,
    LOGISTICS_EDGES,
    DIRECTED_LOGISTICS_WITH_DISCOUNTS
)
from modules.phase2_graph import Graph
from modules.phase3_mst import kruskal_mst, prim_mst
from modules.phase4_shortest_path import dijkstra, bellman_ford
from modules.phase6_matching_engine import DemandSupplyMatchingEngine


def get_initial_data() -> Dict[str, Any]:
    """Returns baseline data for initial frontend rendering."""
    return {
        "demands": DEMAND_RECORDS,
        "supplies": SUPPLY_RECORDS,
        "nodes": LOGISTICS_NODES,
        "edges": LOGISTICS_EDGES,
        "directed_edges": DIRECTED_LOGISTICS_WITH_DISCOUNTS
    }


def run_matching(capacity: int = 250) -> Dict[str, Any]:
    """Executes Phase 6 matching engine pipeline and fleet capacity knapsack."""
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

    return {
        "matches": serialized_matches,
        "mst_cost": mst_cost,
        "mst_edges": [{"u": u, "v": v, "w": w} for u, v, w in mst_edges],
        "knapsack_capacity": capacity,
        "knapsack_utility": round(max_util, 2),
        "knapsack_selected": serialized_knapsack
    }


def get_mst() -> Dict[str, Any]:
    """Computes and compares Kruskal and Prim Minimum Spanning Trees."""
    network = Graph(directed=False)
    for n in LOGISTICS_NODES:
        network.add_node(n)
    for u, v, cost, _ in LOGISTICS_EDGES:
        network.add_edge(u, v, cost)

    k_edges, k_cost, k_stats = kruskal_mst(network)
    p_edges, p_cost, p_stats = prim_mst(network, "North_Hub")

    return {
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
    }


def get_shortest_path(source: str = "North_Hub", algo: str = "dijkstra") -> Dict[str, Any]:
    """Calculates single-source shortest paths using Dijkstra or Bellman-Ford."""
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
        return {
            "source": source,
            "algorithm": "Bellman-Ford",
            "has_negative_cycle": has_neg,
            "results": {
                dest: {"cost": dists[dest], "path": paths[dest]}
                for dest in LOGISTICS_NODES
            }
        }
    else:
        dijk_res = dijkstra(network, source)
        return {
            "source": source,
            "algorithm": "Dijkstra",
            "results": {
                dest: {"cost": dijk_res[dest][0], "path": dijk_res[dest][1]}
                for dest in LOGISTICS_NODES
            }
        }


def dispatch_api_request(path: str, query_params: Dict[str, List[str]]) -> Tuple[int, Dict[str, Any]]:
    """
    Unified router for /api endpoints.
    Returns: (http_status_code, response_dict)
    """
    clean_path = path.rstrip("/")
    if not clean_path:
        clean_path = "/"

    if clean_path == "/api/initial-data":
        return 200, get_initial_data()

    if clean_path == "/api/run-matching":
        try:
            capacity = int(query_params.get("capacity", [250])[0])
        except (ValueError, IndexError):
            capacity = 250
        return 200, run_matching(capacity)

    if clean_path == "/api/mst":
        return 200, get_mst()

    if clean_path == "/api/shortest-path":
        source = query_params.get("source", ["North_Hub"])[0]
        algo = query_params.get("algo", ["dijkstra"])[0]
        return 200, get_shortest_path(source=source, algo=algo)

    return 404, {"error": f"API endpoint '{clean_path}' not found"}
