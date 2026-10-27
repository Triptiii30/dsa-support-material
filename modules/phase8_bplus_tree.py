"""
Phase 8: Unit 5 - B+ Tree for Supplier & Product Catalog Indexing
- Multi-level self-balancing indexing structure optimized for block storage and range scans.
- Internal nodes contain guide keys and child references.
- Leaf nodes contain search keys, record payloads, and sequential doubly-linked sibling pointers.
- Supports O(log N) insertion with proactive/reactive leaf and internal node splits.
- Supports O(log N) exact point lookups, O(N) ordered full traversals, and O(log N + K) range queries.
"""

import os
import sys
import time
from typing import List, Tuple, Dict, Any, Optional

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from dataset.sample_data import SUPPLY_RECORDS, DEMAND_RECORDS


class BPlusNode:
    """Base class for B+ Tree nodes."""
    def __init__(self, is_leaf: bool = False):
        self.is_leaf: bool = is_leaf
        self.keys: List[Any] = []
        self.parent: Optional["BPlusInternalNode"] = None


class BPlusLeafNode(BPlusNode):
    """
    Leaf node storing key-to-record buckets and sequential sibling pointers.
    """
    def __init__(self):
        super().__init__(is_leaf=True)
        # Each entry in records is a list (bucket) of records matching keys[i]
        self.records: List[List[Any]] = []
        self.next_leaf: Optional["BPlusLeafNode"] = None
        self.prev_leaf: Optional["BPlusLeafNode"] = None


class BPlusInternalNode(BPlusNode):
    """
    Internal node containing routing/index keys and child node references.
    An internal node with k keys has k + 1 children.
    """
    def __init__(self):
        super().__init__(is_leaf=False)
        self.children: List[BPlusNode] = []


class BPlusTree:
    """
    B+ Tree data structure of order M.
    - Max keys per node: M - 1.
    - Max children per internal node: M.
    - When a node accumulates M keys, it splits.
    """
    def __init__(self, order: int = 4):
        if order < 3:
            raise ValueError("B+ Tree order must be at least 3")
        self.order: int = order
        self.root: BPlusNode = BPlusLeafNode()
        self.depth: int = 1
        self.total_records: int = 0

    def _find_leaf(self, key: Any) -> BPlusLeafNode:
        """Navigates from root to the appropriate leaf node for key."""
        curr = self.root
        while not curr.is_leaf:
            assert isinstance(curr, BPlusInternalNode)
            idx = 0
            while idx < len(curr.keys) and key >= curr.keys[idx]:
                idx += 1
            curr = curr.children[idx]
        assert isinstance(curr, BPlusLeafNode)
        return curr

    def search(self, key: Any) -> List[Any]:
        """
        Exact point search for key.
        Returns list of all records associated with key, or empty list if not present.
        Time Complexity: O(log_M N)
        """
        leaf = self._find_leaf(key)
        for i, k in enumerate(leaf.keys):
            if k == key:
                return list(leaf.records[i])
        return []

    def insert(self, key: Any, record: Any) -> None:
        """
        Inserts a key-record pair into the B+ Tree.
        Handles leaf and internal node splits automatically.
        Time Complexity: O(log_M N)
        """
        leaf = self._find_leaf(key)

        # Check if key already exists in leaf bucket
        for i, k in enumerate(leaf.keys):
            if k == key:
                leaf.records[i].append(record)
                self.total_records += 1
                return

        # Insert key and new record bucket in sorted order
        idx = 0
        while idx < len(leaf.keys) and leaf.keys[idx] < key:
            idx += 1
        leaf.keys.insert(idx, key)
        leaf.records.insert(idx, [record])
        self.total_records += 1

        # Check capacity overflow: leaf splits when count reaches order
        if len(leaf.keys) >= self.order:
            self._split_leaf(leaf)

    def _split_leaf(self, leaf: BPlusLeafNode) -> None:
        """
        Splits an overflowing leaf node into two halves.
        The smallest key of the right leaf is copied up into the parent as separator.
        """
        mid = len(leaf.keys) // 2
        new_leaf = BPlusLeafNode()
        new_leaf.keys = leaf.keys[mid:]
        new_leaf.records = leaf.records[mid:]
        new_leaf.parent = leaf.parent

        leaf.keys = leaf.keys[:mid]
        leaf.records = leaf.records[:mid]

        # Update sibling pointers (doubly linked list among leaves)
        new_leaf.next_leaf = leaf.next_leaf
        if new_leaf.next_leaf:
            new_leaf.next_leaf.prev_leaf = new_leaf
        leaf.next_leaf = new_leaf
        new_leaf.prev_leaf = leaf

        # Separator key copied up to parent
        pushed_key = new_leaf.keys[0]

        if leaf.parent is None:
            # Root split: create a new root internal node
            new_root = BPlusInternalNode()
            new_root.keys = [pushed_key]
            new_root.children = [leaf, new_leaf]
            leaf.parent = new_root
            new_leaf.parent = new_root
            self.root = new_root
            self.depth += 1
        else:
            self._insert_into_parent(leaf.parent, pushed_key, new_leaf)

    def _insert_into_parent(
        self,
        parent: BPlusInternalNode,
        key: Any,
        right_child: BPlusNode
    ) -> None:
        """Inserts separator key and right child reference into internal parent node."""
        idx = 0
        while idx < len(parent.keys) and parent.keys[idx] < key:
            idx += 1
        parent.keys.insert(idx, key)
        parent.children.insert(idx + 1, right_child)
        right_child.parent = parent

        # Check internal node overflow
        if len(parent.keys) >= self.order:
            self._split_internal(parent)

    def _split_internal(self, node: BPlusInternalNode) -> None:
        """
        Splits an overflowing internal node.
        The median key is moved (pushed) UP into the parent and excluded from children.
        """
        mid = len(node.keys) // 2
        pushed_key = node.keys[mid]

        new_internal = BPlusInternalNode()
        new_internal.keys = node.keys[mid + 1:]
        new_internal.children = node.children[mid + 1:]
        new_internal.parent = node.parent

        # Re-assign parent reference for all migrated children
        for child in new_internal.children:
            child.parent = new_internal

        node.keys = node.keys[:mid]
        node.children = node.children[:mid + 1]

        if node.parent is None:
            # Root split: create new root internal node
            new_root = BPlusInternalNode()
            new_root.keys = [pushed_key]
            new_root.children = [node, new_internal]
            node.parent = new_root
            new_internal.parent = new_root
            self.root = new_root
            self.depth += 1
        else:
            self._insert_into_parent(node.parent, pushed_key, new_internal)

    def ordered_traversal(self) -> List[Tuple[Any, List[Any]]]:
        """
        Sequentially traverses all records in sorted key order using leaf sibling pointers.
        Time Complexity: O(N) linear time.
        """
        curr = self.root
        while not curr.is_leaf:
            assert isinstance(curr, BPlusInternalNode)
            curr = curr.children[0]

        result: List[Tuple[Any, List[Any]]] = []
        leaf_ptr = curr
        while leaf_ptr is not None:
            assert isinstance(leaf_ptr, BPlusLeafNode)
            for k, bucket in zip(leaf_ptr.keys, leaf_ptr.records):
                result.append((k, list(bucket)))
            leaf_ptr = leaf_ptr.next_leaf
        return result

    def range_query(self, min_key: Any, max_key: Any) -> List[Tuple[Any, List[Any]]]:
        """
        Retrieves all key-record pairs satisfying min_key <= key <= max_key.
        Finds the initial leaf via O(log_M N) tree descent, then scans sequential
        leaf sibling pointers until key exceeds max_key.
        Time Complexity: O(log_M N + K), where K is number of items in range.
        """
        leaf = self._find_leaf(min_key)
        result: List[Tuple[Any, List[Any]]] = []
        curr = leaf
        done = False

        while curr is not None and not done:
            for k, bucket in zip(curr.keys, curr.records):
                if k > max_key:
                    done = True
                    break
                if k >= min_key:
                    result.append((k, list(bucket)))
            curr = curr.next_leaf

        return result

    def get_structure_summary(self) -> Dict[str, Any]:
        """Computes statistical summary of the B+ Tree hierarchy."""
        leaves = 0
        internals = 0
        total_keys = 0

        # Level-order traversal
        queue = [self.root]
        while queue:
            curr = queue.pop(0)
            total_keys += len(curr.keys)
            if curr.is_leaf:
                leaves += 1
            else:
                internals += 1
                assert isinstance(curr, BPlusInternalNode)
                queue.extend(curr.children)

        return {
            "order": self.order,
            "depth": self.depth,
            "total_records": self.total_records,
            "total_keys": total_keys,
            "internal_nodes": internals,
            "leaf_nodes": leaves
        }

    def display_tree(self) -> str:
        """Returns string visualization of tree levels and keys."""
        lines = []
        queue = [(self.root, 0)]
        current_level = 0
        level_nodes = []

        while queue:
            node, level = queue.pop(0)
            if level != current_level:
                lines.append(f"Level {current_level} ({'Leaves' if level_nodes[0].is_leaf else 'Internal'}): " +
                             " | ".join(f"[{','.join(str(k) for k in n.keys)}]" for n in level_nodes))
                current_level = level
                level_nodes = []

            level_nodes.append(node)
            if not node.is_leaf:
                assert isinstance(node, BPlusInternalNode)
                for child in node.children:
                    queue.append((child, level + 1))

        if level_nodes:
            lines.append(f"Level {current_level} ({'Leaves' if level_nodes[0].is_leaf else 'Internal'}): " +
                         " | ".join(f"[{','.join(str(k) for k in n.keys)}]" for n in level_nodes))

        return "\n".join(lines)


def build_catalog_bplus_tree(
    records: Optional[List[Dict[str, Any]]] = None,
    key_field: str = "unit_price",
    order: int = 3
) -> BPlusTree:
    """
    Constructs and populates a B+ Tree index over supplier or product catalog records.
    Default order is 3 to demonstrate frequent splits, balancing, and multi-tier hierarchy.
    """
    if records is None:
        records = SUPPLY_RECORDS

    tree = BPlusTree(order=order)
    for rec in records:
        key_val = rec.get(key_field)
        if key_val is not None:
            tree.insert(key_val, rec)
    return tree


def run_phase8_demo():
    """Demonstration runner for Phase 8 (Unit 5: B+ Tree Catalog Indexing)."""
    print("================================================================================")
    print("PHASE 8 DEMO: Unit 5 - B+ Tree for Supplier & Product Catalog Indexing")
    print("================================================================================")

    # 1. Structural Verification: Small synthetic dataset to demonstrate node splitting
    print("\n--- 1. Structural Verification: Node Splitting & Rebalancing (Order = 3) ---")
    synthetic_tree = BPlusTree(order=3)
    keys_to_insert = [50, 20, 80, 10, 30, 70, 90, 40, 60]
    print(f"  Inserting keys sequentially into Order-3 B+ Tree: {keys_to_insert}")
    for k in keys_to_insert:
        synthetic_tree.insert(k, f"Payload_{k}")

    print("\n  Hierarchical Tree Layout:")
    print(synthetic_tree.display_tree())

    summary = synthetic_tree.get_structure_summary()
    print(f"\n  Tree Depth:          {summary['depth']}")
    print(f"  Internal Nodes:      {summary['internal_nodes']}")
    print(f"  Leaf Nodes:          {summary['leaf_nodes']}")
    print(f"  Total Keys Indexed:  {summary['total_keys']}")

    # Ordered Traversal
    ordered = synthetic_tree.ordered_traversal()
    print(f"\n  Ordered Traversal (Sequential Leaf Scan):")
    print("    " + " -> ".join(f"Key({k})" for k, _ in ordered))
    assert [k for k, _ in ordered] == sorted(keys_to_insert), "Ordered traversal must be sorted!"
    print("  [PASS] Ordered leaf traversal strictly monotonically increasing.")

    # Range Query
    rq_min, rq_max = 25, 75
    rq_res = synthetic_tree.range_query(rq_min, rq_max)
    print(f"\n  Range Query [{rq_min} <= key <= {rq_max}]:")
    print("    " + ", ".join(f"Key({k})" for k, _ in rq_res))
    assert [k for k, _ in rq_res] == [30, 40, 50, 60, 70], "Range query results mismatch!"
    print(f"  [PASS] Range query retrieved exactly 5 items in O(log N + K) time.")

    # 2. Production Application: Supplier Catalog Indexing
    print("\n--- 2. Production Application: Supplier Catalog Price Indexing ---")
    catalog_tree = build_catalog_bplus_tree(SUPPLY_RECORDS, key_field="unit_price", order=3)
    cat_summary = catalog_tree.get_structure_summary()
    print(f"  Loaded {len(SUPPLY_RECORDS)} Supplier Records into B+ Tree (Order=3).")
    print(f"  Tree Structure: Depth={cat_summary['depth']}, Leaves={cat_summary['leaf_nodes']}, Internals={cat_summary['internal_nodes']}")
    print("\n  B+ Tree Index Hierarchy:")
    print(catalog_tree.display_tree())

    # Point Search
    target_price = 88.0
    print(f"\n  Exact Price Search: ${target_price:.2f}")
    t0 = time.perf_counter()
    matches = catalog_tree.search(target_price)
    t_search = (time.perf_counter() - t0) * 1000.0
    for m in matches:
        print(f"    -> Found: [{m['id']}] {m['supplier']} | Category: {m['category']} | Qty: {m['available_qty']} units")
    print(f"    Lookup Time: {t_search:.4f} ms")

    # Catalog Price Range Query
    min_budget, max_budget = 35.0, 120.0
    print(f"\n  Procurement Price Window Query: [${min_budget:.2f} to ${max_budget:.2f}]")
    t0 = time.perf_counter()
    price_range = catalog_tree.range_query(min_budget, max_budget)
    t_range = (time.perf_counter() - t0) * 1000.0
    for price, recs in price_range:
        for r in recs:
            print(f"    -> ${price:6.2f} | [{r['id']}] {r['supplier']:28} | Loc: {r['location']}")
    print(f"    Retrieved {sum(len(recs) for _, recs in price_range)} qualifying catalog items in {t_range:.4f} ms via leaf pointers.")


if __name__ == "__main__":
    run_phase8_demo()
