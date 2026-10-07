"""
Demand-Supply Matching Prototype
Master CLI Driver and Demonstration Suite

Usage:
    python main.py             # Interactive Menu
    python main.py --all       # Run all phases sequentially
    python main.py --phase 1   # Run specific phase (1 to 6)
    python main.py --test      # Run unit test suite
"""

import sys
import os
import argparse

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from modules.phase1_structures import run_phase1_demo
from modules.phase2_graph import run_phase2_demo
from modules.phase3_mst import run_phase3_demo
from modules.phase4_shortest_path import run_phase4_demo
from modules.phase5_dp import run_phase5_demo
from modules.phase6_matching_engine import run_phase6_integrated_demo


def print_header():
    print("""
========================================================================================
   ____                                   __     ____                       __         
  / __ \\___  ____ ___  ____ _____  ____  / /    / __/_  ______  ____  / /_  __       
 / / / / _ \\/ __ `__ \\/ __ `/ __ \\/ __ \\/ /    / /_/ / / / __ \\/ __ \\/ / / / /       
/ /_/ /  __/ / / / / / /_/ / / / / /_/ / /    / __/ /_/ / /_/ / /_/ / / /_/ /        
\\____/\\___/_/ /_/ /_/\\__,_/_/ /_/\\____/_/    /_/  \\__,_/ .___/ .___/_/\\__, /         
                                                       /_/   /_/      /____/          
  DEMAND-SUPPLY MATCHING PROTOTYPE | DSA PBL PROJECT
  Self-Balancing Trees * Priority Queues * Graphs * Shortest Paths * Dynamic Programming
========================================================================================
""")


def print_complexity_summary():
    print("""
========================================================================================
                    MASTER ALGORITHM COMPLEXITY REFERENCE MATRIX
========================================================================================
Phase & Algorithm             | Time Complexity            | Space Complexity | Primary Use Case
------------------------------+----------------------------+------------------+--------------------------------------
Phase 1: AVL Tree Search      | O(log N)                   | O(N)             | Price & urgency index lookups
Phase 1: Binary Max-Heap      | O(log N) push/pop, O(1) pk | O(N)             | Priority retrieval for urgent demand
Phase 2: BFS Traversal        | O(V + E)                   | O(V)             | Breadth search & hop-based clusters
Phase 2: DFS Traversal        | O(V + E)                   | O(V)             | Deep route traversal & cycles
Phase 3: Kruskal's MST        | O(E log E) or O(E log V)   | O(V + E)         | Sparse network infrastructure link
Phase 3: Prim's MST (Heap)    | O(E log V)                 | O(V + E)         | Dense network infrastructure link
Phase 4: Dijkstra Routing     | O((V + E) log V)           | O(V + E)         | Nearest supplier lowest transit cost
Phase 4: Bellman-Ford Routing | O(V * E)                   | O(V)             | Routing with subsidies/credits
Phase 4: Floyd-Warshall APSP  | O(V^3)                     | O(V^2)           | Complete all-pairs hub dispatch table
Phase 5: 0/1 Knapsack DP      | O(N * W)                   | O(N * W)         | Vehicle & warehouse quota allocation
Phase 5: LCS Preference DP    | O(M * N)                   | O(M * N)         | Specification tag contract alignment
Phase 5: Matrix Chain DP      | O(N^3)                     | O(N^2)           | Multi-stage logistics pipeline order
Phase 5: Resource Allocation  | O(M * K^2)                 | O(M * K)         | Multi-center utility maximization
========================================================================================
""")


def run_all_phases():
    print_header()
    print("\n[>>>] Running Phase 1: Core Data Structures (AVL Tree & Binary Heap)")
    run_phase1_demo()

    print("\n[>>>] Running Phase 2: Graph Traversal & Connectivity (BFS/DFS/Clusters)")
    run_phase2_demo()

    print("\n[>>>] Running Phase 3: Minimum Cost Spanning Trees (Prim vs Kruskal)")
    run_phase3_demo()

    print("\n[>>>] Running Phase 4: Shortest Path Routing (Dijkstra, Bellman-Ford, Floyd-Warshall)")
    run_phase4_demo()

    print("\n[>>>] Running Phase 5: Dynamic Programming Applications")
    run_phase5_demo()

    print("\n[>>>] Running Phase 6: Prototype Integration")
    run_phase6_integrated_demo()

    print_complexity_summary()


def interactive_menu():
    print_header()
    while True:
        print("\nSelect a Demonstration Module to Execute:")
        print("  [1] Phase 1: Core Data Structures (AVL Tree & Binary Max-Heap)")
        print("  [2] Phase 2: Graph Traversal & Connectivity (BFS, DFS, Clusters, Spanning Trees)")
        print("  [3] Phase 3: Minimum Cost Spanning Trees (Kruskal vs Prim with DSU)")
        print("  [4] Phase 4: Shortest Path Algorithms (Dijkstra, Bellman-Ford, Floyd-Warshall)")
        print("  [5] Phase 5: Dynamic Programming (0/1 Knapsack, LCS, MCM, Resource Allocation)")
        print("  [6] Phase 6: Prototype Integration (End-to-End Demand-Supply Matching Engine)")
        print("  [7] Run All Phases Sequentially (1 to 6)")
        print("  [8] Run Complete Automated Test Suite (Unit & Integration Tests)")
        print("  [9] Display Complexity & Performance Benchmark Summary")
        print("  [0] Exit")

        choice = input("\nEnter your choice [0-9]: ").strip()
        print()

        if choice == "1":
            run_phase1_demo()
        elif choice == "2":
            run_phase2_demo()
        elif choice == "3":
            run_phase3_demo()
        elif choice == "4":
            run_phase4_demo()
        elif choice == "5":
            run_phase5_demo()
        elif choice == "6":
            run_phase6_integrated_demo()
        elif choice == "7":
            run_all_phases()
        elif choice == "8":
            import unittest
            from tests.test_all import (
                TestPhase1DataStructures,
                TestPhase2Graph,
                TestPhase3MST,
                TestPhase4ShortestPath,
                TestPhase5DynamicProgramming,
                TestPhase6IntegratedEngine
            )
            suite = unittest.TestLoader().loadTestsFromNames([
                'tests.test_all.TestPhase1DataStructures',
                'tests.test_all.TestPhase2Graph',
                'tests.test_all.TestPhase3MST',
                'tests.test_all.TestPhase4ShortestPath',
                'tests.test_all.TestPhase5DynamicProgramming',
                'tests.test_all.TestPhase6IntegratedEngine'
            ])
            runner = unittest.TextTestRunner(verbosity=2)
            runner.run(suite)
        elif choice == "9":
            print_complexity_summary()
        elif choice == "0":
            print("Exiting Demand-Supply Matching Prototype. Goodbye!")
            break
        else:
            print("[!] Invalid option. Please enter a number between 0 and 9.")


def main():
    parser = argparse.ArgumentParser(description="Demand-Supply Matching Prototype CLI")
    parser.add_argument("--all", action="store_true", help="Run all phases sequentially")
    parser.add_argument("--phase", type=int, choices=[1, 2, 3, 4, 5, 6], help="Run a specific phase")
    parser.add_argument("--test", action="store_true", help="Run automated test suite")
    parser.add_argument("--summary", action="store_true", help="Print complexity summary")

    args = parser.parse_args()

    if args.all:
        run_all_phases()
    elif args.phase == 1:
        run_phase1_demo()
    elif args.phase == 2:
        run_phase2_demo()
    elif args.phase == 3:
        run_phase3_demo()
    elif args.phase == 4:
        run_phase4_demo()
    elif args.phase == 5:
        run_phase5_demo()
    elif args.phase == 6:
        run_phase6_integrated_demo()
    elif args.test:
        import unittest
        suite = unittest.defaultTestLoader.discover('tests', pattern='test_*.py')
        unittest.TextTestRunner(verbosity=2).run(suite)
    elif args.summary:
        print_complexity_summary()
    else:
        # Default to interactive if no CLI flags provided
        interactive_menu()


if __name__ == "__main__":
    main()
