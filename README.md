# Demand-Supply Matching Prototype | DSA PBL Project

> A high-performance, modular algorithmic framework for multi-criteria demand-supply matching and logistics network optimization.

## Overview
This repository contains the complete implementation for the **Data Structures and Algorithms Project-Based Learning (DSA PBL)**. The system addresses the complex problem of matching multi-attribute demand orders with supplier catalogs, identifying connected regional logistics networks, computing lowest-cost dispatch paths, creating minimum infrastructure spanning trees, and optimizing vehicle cargo capacity through dynamic programming.

---

## Architecture & Module Directory

```
DSA_PBL_PROJECT/
├── README.md                      # Project documentation and quickstart
├── main.py                        # Master CLI driver & interactive runner
├── dataset/
│   ├── __init__.py
│   └── sample_data.py             # Realistic multi-sector demand, supply & network datasets
├── modules/
│   ├── __init__.py
│   ├── phase1_structures.py       # AVL Tree & Binary Max-Heap (Priority Queue)
│   ├── phase2_graph.py            # Graph (Adj List/Matrix), BFS, DFS, Connected Components
│   ├── phase3_mst.py              # Kruskal's & Prim's Minimum Spanning Trees (with DSU)
│   ├── phase4_shortest_path.py    # Dijkstra, Bellman-Ford (negative subsidies), Floyd-Warshall
│   ├── phase5_dp.py               # 0/1 Knapsack, LCS Preference Matching, MCM, Resource Allocation
│   └── phase6_matching_engine.py  # End-to-end Multi-Criteria Matching Engine
├── tests/
│   └── test_all.py                # Comprehensive automated unit & integration test suite
└── docs/
    └── REPORT_2.md                # Comprehensive Report 2 with pseudocode, benchmarks & reflection
```

---

## Quickstart & Execution

### 1. Launch Interactive Web Frontend (HTML / CSS / JS)
Start the local server and open the web dashboard:
```bash
python server.py 8000
```
Then navigate to: **`http://localhost:8000/`** (or open [`web/index.html`](file:///c:/Users/Tripati%20Verma/OneDrive%20-%20Noida%20Institute%20of%20Engineering%20and%20Technology/Documents/DSA_PBL_PROJECT/web/index.html) directly in any web browser).

### 2. Interactive Console CLI
To launch the interactive command-line interface:
```bash
python main.py
```

### 3. Run All Phases Sequentially (Console)
To execute the automated pipeline from Phase 1 through Phase 6 with full logs:
```bash
python main.py --all
```

### 3. Run Specific Phases
```bash
python main.py --phase 1    # Core Data Structures (AVL & Heap)
python main.py --phase 2    # Graph Traversal & Connectivity (BFS/DFS/Clusters)
python main.py --phase 3    # Minimum Cost Spanning Trees (Prim vs Kruskal)
python main.py --phase 4    # Shortest Path Routing (Dijkstra/Bellman-Ford/Floyd-Warshall)
python main.py --phase 5    # Dynamic Programming Applications (Knapsack, LCS, MCM, RAP)
python main.py --phase 6    # Prototype Integration (Integrated Matching Engine)
```

### 4. Run Automated Test Suite
To execute all 10 unit and integration tests:
```bash
python -m unittest tests/test_all.py
# or
python main.py --test
```

---

## Algorithmic Summary

| Phase | Algorithms & Structures | Primary Role in System |
| :--- | :--- | :--- |
| **Phase 1** | AVL Tree, Binary Max-Heap | $O(\log N)$ self-balancing catalog indexing and $O(1)$ priority extraction |
| **Phase 2** | BFS, DFS, Connected Components | Cluster identification & unreachable transport node filtering |
| **Phase 3** | Kruskal (DSU) & Prim's (Heap) | Minimal infrastructure transit network backbone ($168.00 cost) |
| **Phase 4** | Dijkstra, Bellman-Ford, Floyd-Warshall | Lowest-cost routing, subsidized green credits, and APSP matrix |
| **Phase 5** | 0/1 Knapsack, LCS, MCM, RAP | Specification alignment, fleet capacity bounds, and pipeline optimization |
| **Phase 6** | Multi-Criteria Matching Engine | Composite scoring (40% Spec LCS + 30% Price + 30% Proximity) |

For comprehensive theoretical proofs, pseudocode, output logs, comparative tables, and the ~65% progress milestone report, see [`docs/REPORT_2.md`](docs/REPORT_2.md).
