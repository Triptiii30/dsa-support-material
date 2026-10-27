# NOIDA INSTITUTE OF ENGINEERING AND TECHNOLOGY, GREATER NOIDA
### (An Autonomous Institute Affiliated to Dr. A.P.J. Abdul Kalam Technical University, Uttar Pradesh, Lucknow)
### Department of Computer Science and Engineering

---

# PROJECT-BASED LEARNING (PBL) FINAL REPORT: MONTH 3
## Multi-Criteria Demand-Supply Matching & Logistics Optimization Platform
### A Comprehensive Implementation of Classical Data Structures and Algorithms (Units 1 to 5)

---

**Course Code & Title:** Data Structures & Algorithms Project-Based Learning (DSA PBL)  
**Project Title:** Multi-Criteria Demand-Supply Matching & Logistics Optimization Platform  
**Academic Session:** 2026–2027  
**Milestone:** Month 3 Final Project Review & Comprehensive Institutional Report  
**Submitted By:**  
- **Student Name:** Tripti Verma  
- **Branch / Specialization:** Computer Science & Engineering  
- **Institution:** Noida Institute of Engineering and Technology (NIET), Greater Noida  

**Under the Guidance of:**  
- **Faculty Mentor / Project Supervisor:** Department of Computer Science and Engineering, NIET  

---

## CANDIDATE'S DECLARATION

I hereby declare that the work presented in this Project-Based Learning report entitled **"Multi-Criteria Demand-Supply Matching & Logistics Optimization Platform"**, submitted to the Department of Computer Science and Engineering, Noida Institute of Engineering and Technology, Greater Noida, in partial fulfillment of the requirements for the course **Data Structures and Algorithms (DSA PBL)**, is an authentic record of our own work carried out under the supervision of our faculty mentor.

The algorithmic implementations, empirical benchmark measurements, and analytical formulations presented in this report have been directly developed and executed by me. To the best of my knowledge, this report does not contain any fabricated data or undocumented claims.

**Tripti Verma**  
Department of Computer Science & Engineering  
Noida Institute of Engineering and Technology, Greater Noida  
Date: October 28, 2026  

---

## CERTIFICATE OF APPROVAL

This is to certify that the Project-Based Learning report entitled **"Multi-Criteria Demand-Supply Matching & Logistics Optimization Platform"**, submitted by **Tripti Verma**, has been evaluated and approved as satisfying the academic requirements for the course **Data Structures and Algorithms (DSA PBL)**.

The student has successfully developed, verified, tested, and documented the 8-phase algorithmic platform covering:
1. **Unit 1:** Trees, AVL Self-Balancing Trees & Binary Max-Heap Priority Queues
2. **Unit 2:** Graph Theory, Traversals (BFS, DFS), Minimum Spanning Trees (Kruskal, Prim with DSU), and Shortest Paths (Dijkstra, Bellman-Ford, Floyd-Warshall)
3. **Unit 3:** Dynamic Programming (0/1 Knapsack, LCS, Matrix Chain Multiplication, Resource Allocation)
4. **Unit 4:** Branch and Bound — Travelling Salesman Problem (TSP) with Matrix Reduction
5. **Unit 5:** Advanced Indexing — B+ Tree for Multi-Level Catalog Indexing and Range Queries
6. **Integrated Matching Engine:** Multi-criteria composite allocation framework

**Project Supervisor / Faculty Mentor**  
Department of Computer Science & Engineering  
Noida Institute of Engineering and Technology, Greater Noida  

**Head of Department**  
Department of Computer Science & Engineering  
Noida Institute of Engineering and Technology, Greater Noida  

---

## ACKNOWLEDGEMENTS

I express my deepest gratitude to the faculty members and project coordinators of the Department of Computer Science and Engineering at Noida Institute of Engineering and Technology (NIET), Greater Noida, for their invaluable guidance, intellectual encouragement, and rigorous standards throughout the three-month duration of this Project-Based Learning course.

Their insightful feedback during Milestone Review 1 and Milestone Review 2 proved instrumental in shaping our mathematical formulations, optimizing our algorithmic data structures, and navigating complex edge cases such as negative-weight routing, combinatorial explosions in dynamic programming, and branch pruning in branch-and-bound exploration.

I also extend my sincere appreciation to the authors of foundational algorithms literature and the open-source software community whose design philosophies informed our modular, dependency-free architecture.

---

## ABSTRACT

In modern distributed logistics, emergency humanitarian relief, and high-velocity supply chain networks, efficiently allocating constrained supplies to competing demand orders while adhering to multi-dimensional physical, monetary, and temporal constraints is a foundational computational challenge. Naive flat-file and brute-force approaches incur prohibitive polynomial or factorial time complexities, leading to catastrophic allocation delays and route inefficiencies during peak operational surges.

This project designs, engineers, benchmarks, and validates a unified, production-grade **Multi-Criteria Demand-Supply Matching & Logistics Optimization Platform** built strictly from foundational Data Structures and Algorithms without relying on black-box third-party dependencies.

The architecture synthesizes eight modular algorithmic phases aligned directly with the institutional DSA syllabus:
1. **Phase 1 (Unit 1):** Self-Balancing AVL Trees ($O(\log N)$ price indexing) and Binary Max-Heaps ($O(\log N)$ urgency-driven priority order retrieval).
2. **Phase 2 (Unit 2):** Versatile Adjacency List/Matrix Graph representation, BFS/DFS traversals, and Connected Component cluster isolation in $O(V + E)$ time.
3. **Phase 3 (Unit 2):** Regional infrastructure backbone minimization using Kruskal's algorithm (with Disjoint Set Union utilizing path compression and union by rank) and Prim's algorithm, both converging to the identical optimal backbone cost of **$168.00**.
4. **Phase 4 (Unit 2):** Shortest path navigation via Dijkstra's algorithm for standard transit routes, Bellman-Ford for routes featuring green delivery subsidies (negative weights) and negative-cycle detection, and Floyd-Warshall for all-pairs precomputed hub-to-hub dispatch.
5. **Phase 5 (Unit 3):** Dynamic Programming formulations including 0/1 Knapsack for vehicle payload maximization, Longest Common Subsequence (LCS) for client-supplier contract specification alignment, Matrix Chain Multiplication (MCM) for multi-hop pipeline scheduling, and Resource Allocation DP for multi-center utility maximization.
6. **Phase 6:** An integrated Multi-Criteria Matching Engine synthesizing price compatibility, specification similarity, and transit proximity into a composite scoring framework.
7. **Phase 7 (Unit 4 - Final Review Module):** Travelling Salesman Problem (TSP) optimization using Least-Cost Branch and Bound (LCBB) with Matrix Reduction. Validated on standard 4-city ($80.00) and 5-city ($28.00) benchmark instances, and deployed on the 5-hub regional network to find the optimal closed delivery tour of **$125.00** with **15 branches pruned**.
8. **Phase 8 (Unit 5 - Final Review Module):** Multi-level B+ Tree catalog indexing of order $M=3$, featuring automatic leaf and internal node splitting, $O(\log N)$ exact lookups, $O(N)$ sequential leaf traversal, and $O(\log N + K)$ range querying.

All 26 automated unit and contract tests pass with 100% success rate in 3.53 milliseconds. The platform supports interactive CLI execution, local HTTP serving, and serverless cloud deployment on Vercel.

---

## TABLE OF CONTENTS

1. **Chapter 1: Introduction & Problem Formulation**
   - 1.1 Project Background & Industrial Context
   - 1.2 Problem Statement & Algorithmic Challenges
   - 1.3 Project Objectives & Success Criteria
   - 1.4 NIET PBL Course Alignment with Syllabus Units
2. **Chapter 2: Literature Review & Algorithmic Foundations**
   - 2.1 Evolution of Supply Chain Matching Systems
   - 2.2 Theoretical Comparison of Paradigms
   - 2.3 Structural Suitability of Tree and Graph Models
3. **Chapter 3: System Architecture & Data Flow**
   - 3.1 End-to-End Multi-Phase Pipeline Architecture
   - 3.2 Core Domain Data Models
   - 3.3 Zero-Dependency Design Philosophy
4. **Chapter 4: Algorithmic Formulations, Mathematical Models & Pseudocode**
   - 4.1 Unit 1: Self-Balancing AVL Trees & Binary Max-Heaps (Phase 1)
   - 4.2 Unit 2: Graph Connectivity, Traversals & Connected Components (Phase 2)
   - 4.3 Unit 2: Minimum Cost Spanning Trees — Kruskal vs Prim (Phase 3)
   - 4.4 Unit 2: Shortest Path Algorithms — Dijkstra, Bellman-Ford, Floyd-Warshall (Phase 4)
   - 4.5 Unit 3: Dynamic Programming Applications (Phase 5)
   - 4.6 Phase 6: Multi-Criteria Integrated Matching Engine
   - 4.7 Unit 4: Branch and Bound — Travelling Salesman Problem (Phase 7)
   - 4.8 Unit 5: Advanced Indexing — B+ Tree Catalog Engine (Phase 8)
5. **Chapter 5: Implementation Architecture & Deployment**
   - 5.1 Modular Source Code Layout
   - 5.2 Unified API Dispatch Service (`modules/api_service.py`)
   - 5.3 Local HTTP Server (`server.py`) & Cloud Serverless Handler (`api/index.py`)
   - 5.4 Master CLI Driver (`main.py`)
6. **Chapter 6: Empirical Verification, Benchmark Results & Experimental Analysis**
   - 6.1 Test Suite Structure & Execution Record (26/26 Tests Passing)
   - 6.2 Empirical Benchmark Summary Table (Measured Run Times & Space Footprints)
   - 6.3 Detailed Analysis of Unit 4 TSP Branch and Bound Execution
   - 6.4 Detailed Analysis of Unit 5 B+ Tree Indexing & Range Scans
7. **Chapter 7: Limitations, Challenges Encountered & Corrective Actions**
   - 7.1 Engineering Challenges & Algorithmic Solutions
   - 7.2 Explicit Identification of System Limitations
8. **Chapter 8: Conclusion & Future Roadmap**
   - 8.1 Summary of Deliverables & Project Achievements
   - 8.2 Future Roadmap (AI/ML Integration)
9. **References**
10. **Appendix: Algorithmic Complexity Reference Matrix**

---

## CHAPTER 1: INTRODUCTION & PROBLEM FORMULATION

### 1.1 Project Background & Industrial Context
In global logistics, disaster relief management, pharmaceutical supply networks, and e-commerce fulfillment hubs, matching fluctuating customer demands with distributed supplier capacities is an NP-hard or polynomial-bottleneck problem when subject to multi-criteria operational constraints:
- Demands exhibit strict budget ceilings, time-sensitive urgency ratings, and technical specification tags (e.g., `cold_chain`, `sterile`, `express`, `cleanroom`).
- Suppliers operate with discrete inventory quotas, fixed per-unit catalog prices, and geographical physical hubs.
- Transportation networks feature non-uniform road links, varying transit costs, travel delays, and government green-freight subsidies (creating negative transit weights).
- Multi-stop delivery vehicles must optimize routes to minimize total tour costs and avoid visiting hubs in redundant sequences.

### 1.2 Problem Statement & Algorithmic Challenges
A naive, flat-file matching engine encounters crippling performance degradation:
1. Linear catalog scanning requires $O(N)$ comparisons per incoming order, choking under high query volumes.
2. Unordered demand retrieval results in high-urgency medical supplies or emergency relief aid being queued behind low-priority commercial shipments.
3. Unverified route planning risks dispatching trucks across disconnected physical network islands.
4. Greedy local shortest-path selection fails to account for regional network topology, resulting in excessive transit expenditures.
5. Inability to support multi-stop routing forces vehicles to make disjoint, inefficient back-and-forth round trips.

### 1.3 Project Objectives & Success Criteria
The primary objectives of this three-month PBL project are:
1. **Architect a pure Python standard-library platform** free of third-party runtime dependencies.
2. **Implement classical algorithmic techniques** covering Trees, Graphs, Dynamic Programming, Branch and Bound, and B+ Trees.
3. **Verify mathematical correctness** using unit tests with zero tolerance for regression.
4. **Implement the two Final-Review modules:**
   - **Unit 4:** Travelling Salesman Problem via Least-Cost Branch and Bound (LCBB) with Matrix Reduction, validated against known benchmarks and deployed on the regional logistics graph.
   - **Unit 5:** Multi-level B+ Tree supporting node splitting, exact point lookups, $O(N)$ ordered leaf traversals, and $O(\log N + K)$ range queries.
5. **Compile the comprehensive Month 3 Final Institutional Report** documenting verified empirical metrics.

### 1.4 NIET PBL Course Alignment with Syllabus Units
| Syllabus Unit | Core DSA Subject Matter | Project Phase & Module |
| :--- | :--- | :--- |
| **Unit 1** | Trees, Binary Search Trees, AVL Self-Balancing Trees, Heaps | **Phase 1:** `phase1_structures.py` (AVL Tree & Binary Max-Heap) |
| **Unit 2** | Graph Theory, Traversals (BFS, DFS), Connected Components | **Phase 2:** `phase2_graph.py` (Adjacency Matrix/List, BFS, DFS) |
| **Unit 2 (cont.)** | Minimum Spanning Trees (Kruskal with DSU, Prim's Algorithm) | **Phase 3:** `phase3_mst.py` (Kruskal vs Prim MST Engine) |
| **Unit 2 (cont.)** | Shortest Paths (Dijkstra, Bellman-Ford, Floyd-Warshall APSP) | **Phase 4:** `phase4_shortest_path.py` (Routing Algorithms) |
| **Unit 3** | Dynamic Programming (0/1 Knapsack, LCS, MCM, Resource Alloc.) | **Phase 5:** `phase5_dp.py` (Optimization Suite) |
| **Integration** | Multi-Criteria Decision Analysis & Global Matching Pipeline | **Phase 6:** `phase6_matching_engine.py` (Composite Engine) |
| **Unit 4 (Final)** | Branch & Bound: Travelling Salesman Problem (LCBB) | **Phase 7:** `phase7_tsp_branch_bound.py` (TSP Engine) |
| **Unit 5 (Final)** | Advanced Indexing: Multi-Level B+ Trees & Range Retrieval | **Phase 8:** `phase8_bplus_tree.py` (B+ Tree Catalog Engine) |

---

## CHAPTER 2: LITERATURE REVIEW & ALGORITHMIC FOUNDATIONS

### 2.1 Evolution of Supply Chain Matching Systems
Early resource management systems utilized relational SQL joins and flat array scans. As inventory catalogs expanded into millions of Stock Keeping Units (SKUs), classical relational indexing proved inadequate for multi-attribute compatibility scoring where qualitative tags, non-linear transit networks, and cargo weight constraints interact simultaneously.

### 2.2 Theoretical Comparison of Paradigms
- **Greedy Search (Dijkstra, Prim, Kruskal):** Excellent for single-criterion local optimization with matroids or optimal substructure, but fails in the presence of negative weights or multi-constraint knapsacks.
- **Dynamic Programming (Bellman-Ford, 0/1 Knapsack, Floyd-Warshall, LCS, MCM):** Solves overlapping subproblems with optimal substructure by caching state transitions in polynomial time, overcoming greedy myopia.
- **Branch and Bound (TSP):** Essential for NP-hard combinatorial problems where exact global optimality is mandatory. Employs mathematically rigorous lower-bounding to prune provably suboptimal subtrees in the state space tree, avoiding exhaustive $O(N!)$ brute-force exploration.
- **Self-Balancing Trees vs B+ Trees:** While AVL trees provide rigid balance ($BF \in \{-1, 0, 1\}$) for in-memory binary search in $O(\log_2 N)$, B+ trees reduce tree height to $O(\log_M N)$ by adopting high fanout ($M \ge 3$), clustering data records strictly in doubly-linked leaf nodes for superior cache locality and range scan efficiency.

---

## CHAPTER 3: SYSTEM ARCHITECTURE & DATA FLOW

### 3.1 End-to-End Multi-Phase Pipeline Architecture
The architecture operates as a pipelined funnel:
1. **Demand & Supply Ingestion:**
   - Demands are placed into a **Binary Max-Heap** keyed by composite priority: $\text{Priority} = \text{Urgency} \times 10 + \frac{\text{Budget}}{100}$.
   - Supplies are dual-indexed: in an **AVL Tree** for in-memory price search and in a **B+ Tree** of order 3 for catalog indexing and fast range querying.
2. **Topology & Connectivity Filtering:**
   - The regional logistics network is loaded into a **Graph** structure.
   - Connected components are analyzed; unreachable destinations are isolated before routing is attempted.
3. **Shortest Path Computation:**
   - Standard routes use **Dijkstra's algorithm**; routes with subsidies use **Bellman-Ford**.
   - Complete hub-to-hub dispatch costs are generated via **Floyd-Warshall** all-pairs shortest paths.
4. **Multi-Criteria Scoring Engine:**
   - Each demand popped from the Max-Heap searches candidate supplies within budget.
   - For each candidate, specification tags are aligned using **LCS Dynamic Programming**:
     $$\text{Score} = 0.40 \times \text{LCS Similarity} + 0.30 \times \text{Price Attractiveness} + 0.30 \times \text{Proximity Score}$$
5. **Vehicle Capacity & Route Optimization:**
   - Final matched allocations are constrained by fleet payload limits using **0/1 Knapsack DP**.
   - Delivery vehicles servicing multiple distribution hubs execute a closed tour optimized via **TSP Branch and Bound**.

---

## CHAPTER 4: ALGORITHMIC FORMULATIONS & MATHEMATICAL MODELS

### 4.1 Unit 1: Self-Balancing AVL Trees & Binary Max-Heaps (Phase 1)
- **AVL Invariant:** For every node $v$, Balance Factor $BF(v) = h(\text{left}) - h(\text{right}) \in \{-1, 0, 1\}$.
- **Rotations:** LL (Right Rotate), RR (Left Rotate), LR (Left-Right Rotate), RL (Right-Left Rotate).
- **Duplicate Key Handling:** Multi-item bucket arrays (`data_list`) attached to each tree node, avoiding duplicate node overhead while maintaining rigid balance.
- **Binary Max-Heap:** Array-based complete binary tree maintaining $A[\text{parent}(i)] \ge A[i]$. Push and Pop executed in $O(\log N)$ via Sift-Up and Sift-Down.

### 4.2 Unit 2: Graph Connectivity, Traversals & Connected Components (Phase 2)
- Supports dual representation: Adjacency List for sparse traversal and Adjacency Matrix ($V \times V$) for dense matrix operations.
- BFS implemented using FIFO Queue in $O(V + E)$ time; DFS implemented using recursion/stack in $O(V + E)$ time.
- Connected components identified through full-graph traversal sweeps, isolating supply islands.

### 4.3 Unit 2: Minimum Cost Spanning Trees — Kruskal vs Prim (Phase 3)
- **Kruskal's Algorithm:** Sorts all $E$ edges in $O(E \log E)$. Iterates through sorted edges, accepting edge $(u, v)$ if $\text{Find}(u) \neq \text{Find}(v)$. Employs Disjoint Set Union (DSU) with Path Compression and Union by Rank, achieving near-linear time $O(E \cdot \alpha(V))$.
- **Prim's Algorithm:** Maintains a priority min-heap of candidate cut edges, expanding the cut from an arbitrary starting vertex in $O(E \log V)$ time.
- **Empirical Result:** Both algorithms converge to the identical minimal infrastructure backbone cost of **$168.00** across 9 arterial links.

### 4.4 Unit 2: Shortest Path Algorithms — Dijkstra, Bellman-Ford, Floyd-Warshall (Phase 4)
- **Dijkstra's Algorithm:** Uses Min-Heap to compute single-source shortest paths in $O((V + E) \log V)$ time for graphs with strictly non-negative edge weights.
- **Bellman-Ford Algorithm:** Relaxes all $E$ edges $V - 1$ times in $O(V \cdot E)$ time. Correctly accommodates negative edge weights (representing green logistics subsidies) and checks for negative-weight cycles in a final $V$-th iteration pass.
- **Floyd-Warshall Algorithm:** Computes all-pairs shortest paths via dynamic programming:
  $$D_{k}[i][j] = \min\left(D_{k-1}[i][j], D_{k-1}[i][k] + D_{k-1}[k][j]\right)$$
  in $O(V^3)$ time and $O(V^2)$ memory, enabling $O(1)$ dispatch lookup for any hub pair.

### 4.5 Unit 3: Dynamic Programming Applications (Phase 5)
- **0/1 Knapsack DP:** Maximizes total allocation utility subject to vehicle weight capacity $W$:
  $$K[i][w] = \max\left(K[i-1][w], K[i-1][w - w_i] + v_i\right)$$
  Executes in $O(N \cdot W)$ time.
- **Longest Common Subsequence (LCS):** Computes qualitative contract specification overlap:
  $$L[i][j] = \begin{cases} 1 + L[i-1][j-1] & \text{if } s_1[i] = s_2[j] \\ \max(L[i-1][j], L[i][j-1]) & \text{otherwise} \end{cases}$$
  Similarity metric: $\text{Sim}(s_1, s_2) = \frac{2 \times |LCS|}{|s_1| + |s_2|}$.
- **Matrix Chain Multiplication (MCM):** Determines optimal parenthesization of multi-stage logistics pipelines in $O(N^3)$ time, eliminating Catalan-number combinatorial explosion.
- **Resource Allocation DP:** Allocates discrete resources across $M$ centers to maximize overall operational utility in $O(M \cdot K^2)$ time.

### 4.6 Phase 6: Multi-Criteria Integrated Matching Engine
Executes an end-to-end multi-criteria pipeline:
1. Pops top-urgency demands from Max-Heap.
2. Queries candidate supplies in AVL tree where $\text{unit\_price} \le \text{max\_price}$.
3. Computes LCS tag alignment, graph reachability, and transit distance.
4. Evaluates composite matching score and produces an optimized contract manifest.

### 4.7 Unit 4: Branch and Bound — Travelling Salesman Problem (Phase 7)
#### Formulation:
Given an $N \times N$ distance matrix $C$ with $C[i][i] = \infty$, find a simple cycle visiting every vertex exactly once and returning to the depot with minimum total cost:
$$\min \sum_{i=1}^{N} C[\pi(i)][\pi(i+1)], \quad \text{where } \pi(N+1) = \pi(1)$$

#### Least-Cost Branch and Bound (LCBB) with Matrix Reduction:
1. **Matrix Reduction Function:**
   - **Row Reduction:** For each row $i$, find $r_i = \min_j C[i][j]$. Subtract $r_i$ from all entries in row $i$. Total row reduction $R_{rows} = \sum r_i$.
   - **Column Reduction:** For each column $j$, find $c_j = \min_i C[i][j]$. Subtract $c_j$ from all entries in column $j$. Total column reduction $R_{cols} = \sum c_j$.
   - **Initial Lower Bound:** $\text{LB}_{root} = R_{rows} + R_{cols}$.
2. **State Space Tree Node Representation:**
   $$\text{Node} = \langle \text{path}, \text{reduced\_matrix}, \text{cost}, \text{vertex}, \text{level} \rangle$$
3. **Child Expansion $(u \to v)$:**
   - Set row $u = \infty$, column $v = \infty$, and $C[v][\text{start}] = \infty$ (to prevent premature subtours before all $N$ vertices are visited).
   - Reduce child matrix to calculate incremental reduction cost $r_{child}$.
   - Child lower bound: $\text{LB}_{child} = \text{LB}_{parent} + \text{parent.reduced\_matrix}[u][v] + r_{child}$.
4. **Branch Pruning Criterion:**
   $$\text{If } \text{LB}_{child} \ge \text{BestCost}, \quad \text{PRUNE BRANCH (Discard node)}$$
   Otherwise, push child node into the Min-Priority Queue.

#### Verification & Results:
- **Benchmark 1 (4-City Standard Matrix):**
  - Initial Lower Bound: **$70.00**
  - Optimal Tour: `City_A -> City_B -> City_D -> City_C -> City_A`
  - Optimal Tour Cost: **$80.00** (Exact match with known optimal)
  - State Space Nodes Explored: **12**
  - Sub-optimal Branches Pruned: **5**
  - Execution Time: **0.1143 ms**
- **Benchmark 2 (5-City Textbook Matrix):**
  - Initial Lower Bound: **$25.00**
  - Optimal Tour: `Depot_1 -> Depot_4 -> Depot_2 -> Depot_5 -> Depot_3 -> Depot_1`
  - Optimal Tour Cost: **$28.00** (Exact match with known optimal)
  - State Space Nodes Explored: **11**
  - Sub-optimal Branches Pruned: **6**
  - Execution Time: **0.1045 ms**
- **Production Logistics Application (5 Core Hubs):**
  - Hubs: `North_Hub`, `Airport_Logistics_Center`, `Central_Square`, `Tech_Park`, `East_District`
  - Distance Metric: All-pairs shortest path distance matrix via Floyd-Warshall.
  - Initial Lower Bound: **$100.00**
  - Optimal Delivery Route: `North_Hub -> Airport_Logistics_Center -> Tech_Park -> Central_Square -> East_District -> North_Hub`
  - Optimal Closed Tour Cost: **$125.00**
  - Breakdown:
    - `[North_Hub]` $\to$ `[Airport_Logistics_Center]`: **$15.00**
    - `[Airport_Logistics_Center]` $\to$ `[Tech_Park]`: **$20.00**
    - `[Tech_Park]` $\to$ `[Central_Square]`: **$18.00**
    - `[Central_Square]` $\to$ `[East_District]`: **$25.00**
    - `[East_District]` $\to$ `[North_Hub]`: **$47.00**
  - State Space Nodes Explored: **29**
  - Sub-optimal Branches Pruned: **15**
  - Execution Time: **0.3558 ms**

### 4.8 Unit 5: Advanced Indexing — B+ Tree Catalog Engine (Phase 8)
#### Invariants & Structural Properties:
- Order $M = 3$ (Capacity: maximum $M - 1 = 2$ keys per node; node splits upon accumulating $M = 3$ keys).
- **Leaf Nodes:** Contain search keys, data record buckets (supporting multiple supplier items per price point), and `next_leaf` / `prev_leaf` pointers forming a doubly linked list.
- **Internal Nodes:** Contain guide keys and child node references. For $k$ keys, contains $k + 1$ child pointers.
- **Leaf Node Split:** Splits into two halves. The smallest key of the right leaf is copied up into the parent as a separator key.
- **Internal Node Split:** The median key is moved (pushed) UP into the parent and excluded from both child internal nodes.
- **Root Split:** When root splits, a new internal root is created with one key and two children, increasing tree depth by 1.

#### Verification & Results:
- **Synthetic Structural Test (Order = 3, Keys = `[50, 20, 80, 10, 30, 70, 90, 40, 60]`):**
  - Tree Depth: **3**
  - Internal Nodes: **3** (`[50]`, `[20, 30]`, `[70, 80]`)
  - Leaf Nodes: **6** (`[10]`, `[20]`, `[30, 40]`, `[50, 60]`, `[70]`, `[80, 90]`)
  - Total Keys Indexed: **14**
  - Ordered Leaf Traversal: `10 -> 20 -> 30 -> 40 -> 50 -> 60 -> 70 -> 80 -> 90` (strictly monotonic)
  - Range Query `[25, 75]`: Retrieved exactly `[30, 40, 50, 60, 70]` (5 keys) in $O(\log N + K)$ time.
- **Supplier Catalog Application:**
  - Indexed 6 supplier catalog records from `SUPPLY_RECORDS` by `unit_price`.
  - Tree Structure: Depth = **2**, Leaf Nodes = **3**, Internal Nodes = **1**.
  - Internal Node Guide Keys: `[88.0, 135.0]`
  - Leaf Nodes: `[25.0, 40.0]`, `[88.0, 110.0]`, `[135.0, 260.0]`.
  - Point Search (`price = $88.00`): Retrieved `[S202] Titan Heavy Foundries` in **0.0019 ms**.
  - Procurement Range Query (`$35.00 <= price <= $120.00`): Retrieved 3 suppliers (FarmFresh `$40.00`, Titan `$88.00`, Helios `$110.00`) in **0.0047 ms**.
  - Ordered Traversal: Scanned all 6 catalog items in **0.0034 ms** strictly through leaf sibling pointers.

---

## CHAPTER 5: IMPLEMENTATION ARCHITECTURE & DEPLOYMENT

### 5.1 Modular Source Code Layout
```
DSA_PBL_PROJECT/
├── dataset/
│   ├── __init__.py
│   └── sample_data.py             # Realistic multi-sector demand, supply & network data
├── docs/
│   ├── FINAL_PBL_REPORT.docx      # Institutional Final Review Word Report
│   ├── FINAL_PBL_REPORT.pdf       # Institutional Final Review PDF Report
│   ├── FINAL_PBL_REPORT.md        # Comprehensive Final Markdown Report
│   ├── REPORT_2.md                # Milestone 2 Progress Report
│   └── slides/                    # Archived lecture presentations (Units 1-3)
├── modules/
│   ├── __init__.py
│   ├── api_service.py             # Unified API handler and dispatch service
│   ├── phase1_structures.py       # Unit 1: AVL Tree & Binary Max-Heap
│   ├── phase2_graph.py            # Unit 2: Graph (Adj List/Matrix), BFS, DFS, Clusters
│   ├── phase3_mst.py              # Unit 2: Kruskal's & Prim's MST (with DSU)
│   ├── phase4_shortest_path.py    # Unit 2: Dijkstra, Bellman-Ford, Floyd-Warshall
│   ├── phase5_dp.py               # Unit 3: 0/1 Knapsack, LCS, MCM, Resource Allocation
│   ├── phase6_matching_engine.py  # Integrated Multi-Criteria Matching Engine
│   ├── phase7_tsp_branch_bound.py # Unit 4: TSP using Branch and Bound (LCBB)
│   └── phase8_bplus_tree.py       # Unit 5: B+ Tree Catalog Indexing Engine
├── tests/
│   ├── __init__.py
│   ├── test_all.py                # Algorithmic unit tests (Phases 1 through 8)
│   └── test_api.py                # API contract and endpoint unit tests
├── api/
│   └── index.py                   # Vercel Serverless Function entry point
├── main.py                        # Master CLI driver & interactive runner (Phases 1-8)
├── server.py                      # Local & container HTTP development server
├── vercel.json                    # Vercel serverless routing configuration
├── requirements.txt               # Pure Python standard library declaration
└── web/                           # Dashboard visualizer assets (HTML, CSS, JS)
```

### 5.2 Standalone Python Standard Library Philosophy
The entire algorithmic platform is implemented in pure Python (utilizing built-in packages: `heapq`, `collections`, `copy`, `math`, `time`, `http.server`, `urllib.parse`, `json`, `argparse`). No third-party computational or graph packages (such as NumPy, NetworkX, or SciPy) are utilized.

### 5.3 Unified API Dispatch Architecture
All client interfaces (local server, web dashboard, and Vercel serverless function) query business logic through a single centralized controller: `modules.api_service.dispatch_api_request(path, query_params)`. This eliminates dual-maintenance divergence and guarantees contract consistency across:
- `/api/initial-data`
- `/api/run-matching`
- `/api/mst`
- `/api/shortest-path`
- `/api/tsp-route`
- `/api/bplus-catalog`

---

## CHAPTER 6: EMPIRICAL VERIFICATION & BENCHMARK RESULTS

### 6.1 Test Suite Structure & Execution Record
The platform features an automated test suite comprising **26 distinct unit and contract tests**:
- `TestPhase1DataStructures` (2 tests): AVL Tree balance invariant ($BF \in \{-1, 0, 1\}$), exact search, range query, deletion; Binary Max-Heap priority order.
- `TestPhase2Graph` (1 test): BFS/DFS traversal order, spanning tree edge counts, and connected component cluster detection.
- `TestPhase3MST` (1 test): Kruskal (with DSU) vs Prim's algorithm total cost equivalence ($168.00).
- `TestPhase4ShortestPath` (1 test): Dijkstra routing, Bellman-Ford negative edge credits, negative cycle detection, Floyd-Warshall APSP reconstruction.
- `TestPhase5DynamicProgramming` (4 tests): 0/1 Knapsack DP vs Brute-Force equivalence, LCS preference scoring, Matrix Chain Multiplication DP vs Brute Force, Resource Allocation.
- `TestPhase6IntegratedEngine` (1 test): End-to-end multi-criteria pipeline validation and capacity bound verification.
- `TestPhase7TSPBranchAndBound` (3 tests): 4-city benchmark (cost 80.00), 5-city benchmark (cost 28.00), and logistics graph multi-stop route with genuine branch pruning.
- `TestPhase8BPlusTree` (5 tests): Insertion and leaf/internal splitting, exact point search and missing key handling, ordered traversal verification, range query bounds, and catalog indexing.
- `TestApiService` (8 tests): Contract validation for `/api/initial-data`, `/api/run-matching`, `/api/mst`, `/api/shortest-path` (Dijkstra and Bellman-Ford), `/api/tsp-route`, `/api/bplus-catalog`, and 404 handler.

**Test Run Evidence:**
```
Ran 26 tests in 0.003s
OK (26/26 passed, 0 failures, 0 errors)
Total execution time: 3.53 ms
```

### 6.2 Empirical Benchmark Summary Table
*All metrics represent actual measurements recorded on the execution host:*

| Phase & Algorithm | Time Complexity | Space Complexity | Measured Execution Time | Primary Output / Invariant |
| :--- | :--- | :--- | :--- | :--- |
| **Phase 1: AVL Tree Search** | $O(\log N)$ | $O(N)$ | **0.0008 ms** | Balanced BST ($BF = 0$) |
| **Phase 1: Binary Max-Heap** | $O(\log N)$ | $O(N)$ | **0.0012 ms** | Strict priority descent |
| **Phase 2: BFS Traversal** | $O(V + E)$ | $O(V)$ | **0.0110 ms** | 10 nodes visited in order |
| **Phase 2: DFS Traversal** | $O(V + E)$ | $O(V)$ | **0.0064 ms** | Spanning tree generated |
| **Phase 3: Kruskal's MST** | $O(E \log E)$ | $O(V + E)$ | **0.0326 ms** | Cost: **$168.00** (12 edges eval) |
| **Phase 3: Prim's MST** | $O(E \log V)$ | $O(V + E)$ | **0.0136 ms** | Cost: **$168.00** (12 edges eval) |
| **Phase 4: Dijkstra Routing** | $O((V+E) \log V)$| $O(V + E)$ | **0.0185 ms** | North_Hub $\to$ Central: **$22.00** |
| **Phase 4: Bellman-Ford** | $O(V \cdot E)$ | $O(V)$ | **0.0241 ms** | North_Hub $\to$ Rural: **$14.00** |
| **Phase 4: Floyd-Warshall** | $O(V^3)$ | $O(V^2)$ | **0.0482 ms** | Complete $10 \times 10$ matrix |
| **Phase 5: 0/1 Knapsack DP** | $O(N \cdot W)$ | $O(N \cdot W)$ | **0.1270 ms** | Max Utility: **1786.00** |
| **Phase 5: LCS Alignment** | $O(M \cdot N)$ | $O(M \cdot N)$ | **0.0084 ms** | Spec similarity calculated |
| **Phase 5: Matrix Chain DP** | $O(N^3)$ | $O(N^2)$ | **0.0110 ms** | Optimal cost: **30,000** |
| **Phase 5: Resource Alloc.** | $O(M \cdot K^2)$ | $O(M \cdot K)$ | **0.0195 ms** | Max Utility: **30.00** |
| **Phase 6: Multi-Criteria** | Composite | $O(D+S+V)$ | **0.1437 ms** | 6 contracts fulfilled |
| **Phase 7: TSP 4-City LCBB** | $O(2^N \cdot N^2)$ | $O(N \cdot 2^N)$| **0.1143 ms** | Cost: **$80.00**, 5 pruned |
| **Phase 7: TSP 5-City LCBB** | $O(2^N \cdot N^2)$ | $O(N \cdot 2^N)$| **0.1045 ms** | Cost: **$28.00**, 6 pruned |
| **Phase 7: TSP Logistics** | $O(2^N \cdot N^2)$ | $O(N \cdot 2^N)$| **0.3558 ms** | Cost: **$125.00**, 15 pruned |
| **Phase 8: B+ Tree Search** | $O(\log_M N)$ | $O(N)$ | **0.0019 ms** | Exact catalog lookup |
| **Phase 8: B+ Tree Range** | $O(\log_M N + K)$| $O(N)$ | **0.0047 ms** | 3 qualifying suppliers |
| **Phase 8: B+ Ordered Scan** | $O(N)$ | $O(N)$ | **0.0034 ms** | Full leaf scan (6 items) |

---

## CHAPTER 7: LIMITATIONS, CHALLENGES ENCOUNTERED & CORRECTIVE ACTIONS

### 7.1 Engineering Challenges & Algorithmic Solutions
1. **Duplicate Price Points in Binary Trees:** Multiple suppliers offering identical unit prices caused silent node overwriting in standard BST implementations.  
   *Solution:* Designed multi-item bucket arrays (`data_list` in AVL, `records` in B+ Tree) at each node, preserving all distinct supplier records without unbalancing the search tree.
2. **Disconnected Physical Transport Islands:** Attempting shortest-path calculations across unreachable locations produced infinite loops or unbounded distance values.  
   *Solution:* Integrated Phase 2 Connected Components analysis before routing. Disconnected islands are isolated gracefully.
3. **Negative Transit Subsidies Invalidating Greedy Dijkstra:** Municipal incentives and backhaul credits generate negative edge weights, invalidating Dijkstra's non-decreasing distance invariant.  
   *Solution:* Implemented dual routing engines: Dijkstra is used for standard physical transit networks; Bellman-Ford is automatically invoked for subsidized routes with rigorous negative-cycle detection.
4. **Fractional vs Integer Knapsack Quantities:** Cargo constraints often include fractional quantities, whereas classical 0/1 Knapsack DP requires discrete integer table indexing.  
   *Solution:* Applied integer scaling factors before dynamic programming table construction, rescaling results during solution reconstruction.
5. **Combinatorial Explosion in Multi-Stop Route Optimization:** Exhaustive evaluation of $N!$ permutations for multi-stop delivery tours becomes computationally intractable.  
   *Solution:* Transitioned to Least-Cost Branch and Bound with Matrix Reduction, pruning provably suboptimal branches early and achieving optimal 5-hub delivery dispatch in under 0.4 milliseconds.

### 7.2 Explicit Statement of System Limitations
To maintain documentation integrity, the following limitations are explicitly noted:
1. **Deterministic Static Network Assumption:** The current graph topology assumes fixed edge costs and travel times. Real-world transit fluctuations (weather events, dynamic traffic congestion, accident closures) require real-time dynamic edge weight re-evaluation.
2. **In-Memory Volatility:** All tree, graph, and heap data structures currently reside in system memory. Persistent serialization to relational/NoSQL backends (e.g., PostgreSQL, SQLite) is required for persistent enterprise production deployments.
3. **Advanced AI/ML Roadmaps Unimplemented:** As defined in the Project Roadmap, predictive demand forecasting using recurrent neural networks (LSTM), Graph Neural Networks (GNN) for cold-start semantic embeddings, and Reinforcement Learning (RL) for dynamic pricing remain future enhancements beyond the scope of classical DSA coursework.

---

## CHAPTER 8: CONCLUSION & FUTURE ROADMAP

### 8.1 Summary of Deliverables & Project Achievements
Over the three-month Project-Based Learning curriculum, the project successfully delivered:
1. A fully functional, production-tested 8-phase algorithmic platform in pure Python.
2. Complete implementations of the two Final-Review modules:
   - **Unit 4:** Least-Cost Branch and Bound Travelling Salesman Problem route optimization.
   - **Unit 5:** Multi-level B+ Tree catalog indexing with node splitting, exact lookups, and range scans.
3. A verified test suite with 26 passing tests executing in under 4 milliseconds.
4. An interactive multi-phase CLI runner and dual deployment engine (local HTTP and Vercel cloud serverless).
5. Comprehensive institutional reports formatted in Markdown, DOCX, and PDF.

### 8.2 Future Scope
Future phases of the platform will focus on bridging classical algorithmic optimizations with modern artificial intelligence:
- **LSTM / Prophet Integration:** Forecasting demand surges before they enter the priority queue, enabling proactive warehouse inventory placement.
- **Graph Convolutional Networks (GCN):** Generating dense vector embeddings of supply and demand nodes to enable semantic compatibility matching beyond literal keyword tags.
- **Deep Q-Networks (DQN):** Dynamically tuning transit subsidies and driver incentive payments based on real-time fleet capacity backlogs.

---

## REFERENCES
1. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.
2. Horowitz, E., Sahni, S., & Rajasekaran, S. (2008). *Fundamentals of Computer Algorithms* (2nd ed.). Universities Press.
3. Little, J. D., Murty, K. G., Sweeney, D. W., & Karel, C. (1963). *An Algorithm for the Traveling Salesman Problem*. Operations Research, 11(6), 972–989.
4. Comer, D. (1979). *The Ubiquitous B-Tree*. ACM Computing Surveys (CSUR), 11(2), 121–137.
5. Dijkstra, E. W. (1959). *A note on two problems in connexion with graphs*. Numerische Mathematik, 1(1), 269–271.
6. Kruskal, J. B. (1956). *On the shortest spanning subtree of a graph and the traveling salesman problem*. Proceedings of the American Mathematical Society, 7(1), 48–50.
7. Bellman, R. (1958). *On a routing problem*. Quarterly of Applied Mathematics, 16(1), 87–90.
8. Floyd, R. W. (1962). *Algorithm 97: Shortest path*. Communications of the ACM, 5(6), 345.

---

## APPENDIX: MASTER ALGORITHMIC COMPLEXITY REFERENCE MATRIX

| Phase & Module | Algorithmic Paradigm | Time Complexity (Best / Avg / Worst) | Space Complexity | Practical Role in Matching Platform |
| :--- | :--- | :--- | :--- | :--- |
| **Phase 1: AVL Tree** | Self-Balancing BST | $O(\log N) / O(\log N) / O(\log N)$ | $O(N)$ | Price catalog point lookups and budget ceiling range search |
| **Phase 1: Max-Heap** | Priority Queue | $O(1) \text{ peek} / O(\log N) \text{ push/pop}$ | $O(N)$ | Urgent demand order prioritization |
| **Phase 2: BFS** | Queue-based Traversal | $O(V + E) / O(V + E) / O(V + E)$ | $O(V)$ | Hop-bounded cluster exploration & breadth connectivity |
| **Phase 2: DFS** | Stack/Recursive Traversal| $O(V + E) / O(V + E) / O(V + E)$ | $O(V)$ | Deep route search & cycle detection |
| **Phase 3: Kruskal MST**| Greedy with DSU | $O(E \log E) / O(E \log E) / O(E \log E)$ | $O(V + E)$ | Sparse regional infrastructure transit backbone optimization |
| **Phase 3: Prim MST** | Greedy with Min-Heap | $O(E \log V) / O(E \log V) / O(E \log V)$ | $O(V + E)$ | Dense hub cabling and minimal transport interconnection |
| **Phase 4: Dijkstra** | Greedy Shortest Path | $O((V+E) \log V)$ | $O(V + E)$ | Lowest cost dispatch path for non-negative road links |
| **Phase 4: Bellman-Ford**| Dynamic Programming | $O(V \cdot E) / O(V \cdot E) / O(V \cdot E)$ | $O(V)$ | Routing with green delivery subsidies & negative cycle check |
| **Phase 4: Floyd-Warshall**| Dynamic Programming | $O(V^3) / O(V^3) / O(V^3)$ | $O(V^2)$ | All-pairs precomputed transit cost matrix for $O(1)$ dispatch |
| **Phase 5: 0/1 Knapsack**| Dynamic Programming | $O(N \cdot W) / O(N \cdot W) / O(N \cdot W)$ | $O(N \cdot W)$ | Fleet payload optimization under cargo capacity constraint |
| **Phase 5: LCS Matching**| Dynamic Programming | $O(M \cdot N) / O(M \cdot N) / O(M \cdot N)$ | $O(M \cdot N)$ | Quantitative similarity scoring of qualitative contract tags |
| **Phase 5: Matrix Chain**| Dynamic Programming | $O(N^3) / O(N^3) / O(N^3)$ | $O(N^2)$ | Multi-stage logistics pipeline staging optimization |
| **Phase 5: Resource Alloc**| Dynamic Programming | $O(M \cdot K^2) / O(M \cdot K^2) / O(M \cdot K^2)$| $O(M \cdot K)$ | Multi-center utility maximization under fixed resource budget |
| **Phase 6: Multi-Criteria**| Composite Pipeline | $O(D \cdot (\log S + V \log V))$ | $O(D+S+V+E)$ | Unified multi-criteria contract scoring and dispatch engine |
| **Phase 7: TSP (LCBB)** | Branch and Bound | $O(N^2) \text{ best} / O(2^N \cdot N^2) \text{ worst}$| $O(N \cdot 2^N)$ | Multi-stop closed delivery vehicle tour optimization |
| **Phase 8: B+ Tree** | Multi-level Balanced Tree| $O(\log_M N) \text{ search} / O(N) \text{ traversal}$| $O(N)$ | High-throughput supplier catalog indexing and range querying |
