# Demand-Supply Matching Prototype | DSA PBL Project

> A high-performance, modular algorithmic framework for multi-criteria demand-supply matching, fleet capacity optimization, and logistics network routing.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-26%20Passed-brightgreen.svg)](#6-testing--verification)
[![Vercel Deployment](https://img.shields.io/badge/Deploy-Vercel-black.svg)](https://vercel.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](#4-docker-deployment)

---

## Overview

This repository contains the complete production-grade implementation for the **Data Structures and Algorithms Project-Based Learning (DSA PBL)**. The system addresses the complex problem of matching multi-attribute demand orders with supplier catalogs, identifying connected regional logistics networks, computing lowest-cost dispatch paths, creating minimum infrastructure spanning trees, optimizing vehicle cargo capacity through dynamic programming, solving multi-stop delivery tours via Branch & Bound (TSP), and indexing high-throughput product catalogs using B+ Trees.

The application features:
1. **Interactive Visual Dashboard (Web UI)**: Canvas-based visualizers for Network Graphs, Minimum Spanning Trees (MST), AVL Trees, Binary Heaps, and Dynamic Programming matrices.
2. **Modular Algorithmic Engine (Python Core)**: 8 discrete phases covering self-balancing trees, priority queues, graph algorithms, shortest paths, dynamic programming, unified multi-criteria matching, TSP branch and bound, and B+ tree indexing.
3. **Dual-Mode Deployment**:
   - **Local & Docker Server**: Built-in HTTP server (`server.py`) serving both static assets and API routes.
   - **Cloud Serverless (Vercel)**: Configured with `vercel.json` and `api/index.py` serverless function handler.

---

## Architecture & Directory Structure

```
DSA_PBL_PROJECT/
├── .dockerignore                  # Docker build exclusions
├── .env.example                   # Environment configuration template
├── .gitignore                     # Production Git ignore rules
├── Dockerfile                     # Lightweight container image definition
├── docker-compose.yml             # Single-command local orchestration
├── README.md                      # Primary project documentation
├── requirements.txt               # Pure Python standard library declaration
├── vercel.json                    # Vercel serverless routing configuration
├── api/
│   └── index.py                   # Vercel Serverless Function entry point
├── dataset/
│   ├── __init__.py
│   └── sample_data.py             # Realistic multi-sector demand, supply & network datasets
├── docs/
│   ├── FINAL_PBL_REPORT.docx      # Institutional Final Review Word Report
│   ├── FINAL_PBL_REPORT.pdf       # Institutional Final Review PDF Report
│   ├── FINAL_PBL_REPORT.md        # Comprehensive Final Markdown Report
│   ├── REPORT_2.md                # Milestone 2 Progress Report
│   └── slides/                    # Archived lecture presentations
│       ├── README.md              # Slide deck catalog
│       ├── Unit-1_Trees.pptx      # Unit 1: Trees & AVL Trees
│       ├── Unit-2_DSA.pptx        # Unit 2: Graphs, Spanning Trees & Routing
│       └── Unit-3_DSA.pptx        # Unit 3: Dynamic Programming
├── main.py                        # Master CLI driver & interactive runner (Phases 1-8)
├── modules/
│   ├── __init__.py
│   ├── api_service.py             # Unified API handler and dispatch service
│   ├── phase1_structures.py       # AVL Tree & Binary Max-Heap (Priority Queue)
│   ├── phase2_graph.py            # Graph (Adj List/Matrix), BFS, DFS, Connected Components
│   ├── phase3_mst.py              # Kruskal's & Prim's Minimum Spanning Trees (with DSU)
│   ├── phase4_shortest_path.py    # Dijkstra, Bellman-Ford (negative subsidies), Floyd-Warshall
│   ├── phase5_dp.py               # 0/1 Knapsack, LCS Preference Matching, MCM, Resource Allocation
│   ├── phase6_matching_engine.py  # End-to-end Multi-Criteria Matching Engine
│   ├── phase7_tsp_branch_bound.py # Unit 4: TSP using Branch and Bound (LCBB)
│   └── phase8_bplus_tree.py       # Unit 5: B+ Tree Catalog Indexing Engine
├── server.py                      # Local & container HTTP development server
├── tests/
│   ├── __init__.py
│   ├── test_all.py                # Algorithmic unit tests for Phases 1 through 8
│   └── test_api.py                # API contract and endpoint unit tests
└── web/
    ├── app.js                     # Vanilla modern JavaScript (ES6+) visualization engine
    ├── index.html                 # Responsive dashboard interface
    └── style.css                  # Modern CSS design system & visual styling
```

---

## Quickstart & Execution

### Prerequisites
- **Python 3.8+** (Uses 100% standard libraries; no external pip dependencies required).
- Any modern web browser (Chrome, Firefox, Safari, Edge).

### 1. Launch Interactive Web Frontend
Start the local server:
```bash
python server.py
```
Or specify a custom port:
```bash
python server.py 8080
```
Then navigate to: **`http://localhost:8000/`** (or open [`web/index.html`](web/index.html) directly in any web browser).

### 2. Interactive Console CLI
To launch the interactive command-line interface:
```bash
python main.py
```

### 3. Automated Pipeline Execution
Run all 6 phases sequentially with detailed output logs and complexity matrices:
```bash
python main.py --all
```

Run specific algorithmic phases:
```bash
python main.py --phase 1    # Phase 1: Core Data Structures (AVL & Heap)
python main.py --phase 2    # Phase 2: Graph Traversal & Connectivity (BFS/DFS/Clusters)
python main.py --phase 3    # Phase 3: Minimum Cost Spanning Trees (Prim vs Kruskal)
python main.py --phase 4    # Phase 4: Shortest Path Routing (Dijkstra/Bellman-Ford/Floyd-Warshall)
python main.py --phase 5    # Phase 5: Dynamic Programming Applications (Knapsack, LCS, MCM, RAP)
python main.py --phase 6    # Phase 6: Prototype Integration (Integrated Matching Engine)
python main.py --summary    # Display complexity & benchmark reference matrix
```

---

## Deployment Configuration

### 1. Deploying to Vercel (Recommended Cloud Option)
This repository is pre-configured with [`vercel.json`](vercel.json) and [`api/index.py`](api/index.py):
1. Push your repository to GitHub.
2. Import the repository into **[Vercel](https://vercel.com/)**.
3. Keep the **Root Directory** as `./` (default) and Framework Preset as **Other**.
4. Click **Deploy**.
   - The frontend is served automatically from `/web`.
   - All `/api/*` endpoints are dynamically handled by Vercel Serverless Functions (`api/index.py`).

### 2. Docker & Container Deployment
Run with Docker:
```bash
# Build Docker image
docker build -t dsa-matchgrid:latest .

# Run container on port 8000
docker run -p 8000:8000 --name dsa_server dsa-matchgrid:latest
```

Or using Docker Compose:
```bash
docker compose up -d
```

### 3. Container Platforms (Render, Railway, Heroku, Fly.io)
The `server.py` entry point respects standard environment variables:
- `PORT`: Network port (defaults to `8000`).
- `HOST`: Bind address (defaults to `0.0.0.0` or `""`).

See [`.env.example`](.env.example) for configuration options.

---

## Testing & Verification

The repository includes an automated test suite verifying both algorithmic correctness and API schema contracts:

```bash
# Run all discovered tests
python -m unittest discover tests -v

# Or via CLI flag
python main.py --test
```

### Test Coverage Highlights:
- **Phase 1**: AVL height-balancing invariant ($BF \in \{-1, 0, 1\}$), exact lookups, range queries, deletions; Binary Max-Heap priority ordering.
- **Phase 2**: BFS/DFS traversal order, spanning tree edge counts, and connected component cluster detection.
- **Phase 3**: Kruskal (with DSU path compression and union by rank) vs Prim's algorithm total cost equivalence ($168.00 cost).
- **Phase 4**: Dijkstra non-negative routing, Bellman-Ford negative edge credits and negative cycle detection, Floyd-Warshall APSP reconstruction.
- **Phase 5**: 0/1 Knapsack DP vs Brute-Force equivalence, LCS preference score calculation, Matrix Chain Multiplication DP, and Resource Allocation.
- **Phase 6**: End-to-end multi-criteria pipeline validation and capacity bound verification.
- **API Endpoints**: Contract verification for `/api/initial-data`, `/api/run-matching`, `/api/mst`, `/api/shortest-path`, and 404 handler.

---

## Algorithmic Complexity Reference Matrix

| Phase & Algorithm | Time Complexity | Space Complexity | Primary Use Case in Matching System |
| :--- | :--- | :--- | :--- |
| **Phase 1: AVL Tree Search** | $O(\log N)$ | $O(N)$ | Self-balancing price catalog indexing & range queries |
| **Phase 1: Binary Max-Heap** | $O(\log N)$ push/pop, $O(1)$ peek | $O(N)$ | High-urgency demand order priority retrieval |
| **Phase 2: BFS Traversal** | $O(V + E)$ | $O(V)$ | Hub reachability & hop-bounded supply clusters |
| **Phase 2: DFS Traversal** | $O(V + E)$ | $O(V)$ | Deep route exploration & cycle identification |
| **Phase 3: Kruskal's MST** | $O(E \log E)$ or $O(E \log V)$ | $O(V + E)$ | Sparse regional infrastructure transit backbone |
| **Phase 3: Prim's MST (Heap)** | $O(E \log V)$ | $O(V + E)$ | Dense network minimal cabling & hub connection |
| **Phase 4: Dijkstra Routing** | $O((V + E) \log V)$ | $O(V + E)$ | Single-source lowest transit cost pathfinding |
| **Phase 4: Bellman-Ford** | $O(V \cdot E)$ | $O(V)$ | Routing with green subsidies & backhaul discounts |
| **Phase 4: Floyd-Warshall** | $O(V^3)$ | $O(V^2)$ | Complete all-pairs hub dispatch matrix ($O(1)$ query) |
| **Phase 5: 0/1 Knapsack DP** | $O(N \cdot W)$ | $O(N \cdot W)$ | Fleet vehicle capacity & warehouse quota allocation |
| **Phase 5: LCS Preference DP**| $O(M \cdot N)$ | $O(M \cdot N)$ | Client specification tag compatibility scoring |
| **Phase 5: Matrix Chain DP** | $O(N^3)$ | $O(N^2)$ | Optimal multi-stage supply chain pipeline ordering |
| **Phase 5: Resource Allocation**| $O(M \cdot K^2)$ | $O(M \cdot K)$ | Multi-center utility maximization under fixed quota |
| **Phase 6: Multi-Criteria Match**| Composite Pipeline | $O(V + E + N)$ | Composite scoring (40% LCS + 30% Price + 30% Proximity) |

For comprehensive theoretical proofs, pseudocode, output logs, comparative tables, and the ~65% progress milestone report, see [`docs/REPORT_2.md`](docs/REPORT_2.md).
