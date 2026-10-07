"""
Phase 1: Core Data Structures
- AVL Tree (Self-balancing Binary Search Tree) for indexing records by price/urgency.
- Binary Heap (Priority Queue) for priority-based match retrieval.
"""

import os
import sys
from typing import Any, List, Optional, Tuple, Callable

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ==============================================================================
# 1. AVL Tree Implementation
# ==============================================================================

class AVLNode:
    """Represents a node in an AVL tree."""
    def __init__(self, key: float, data: Any):
        self.key: float = key
        # Using a list to accommodate duplicate keys (e.g. multiple items at same price/urgency)
        self.data_list: List[Any] = [data]
        self.left: Optional['AVLNode'] = None
        self.right: Optional['AVLNode'] = None
        self.height: int = 1

    def __repr__(self) -> str:
        return f"AVLNode(key={self.key}, count={len(self.data_list)}, height={self.height})"


class AVLTree:
    """
    Self-balancing Binary Search Tree (AVL Tree) for indexing demand/supply records.
    Guarantees O(log N) worst-case time complexity for insertion, deletion, and search.
    """
    def __init__(self, key_attribute_name: str = "key"):
        self.root: Optional[AVLNode] = None
        self.attribute_name: str = key_attribute_name
        self.size: int = 0

    def _get_height(self, node: Optional[AVLNode]) -> int:
        return node.height if node else 0

    def _get_balance(self, node: Optional[AVLNode]) -> int:
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _right_rotate(self, y: AVLNode) -> AVLNode:
        r"""
            y                              x
           / \                            / \
          x   T3   -- Right Rotate ->    T1  y
         / \                                / \
        T1  T2                             T2 T3
        """
        x = y.left
        assert x is not None
        T2 = x.right

        # Perform rotation
        x.right = y
        y.left = T2

        # Update heights
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))

        return x

    def _left_rotate(self, x: AVLNode) -> AVLNode:
        r"""
          x                                y
         / \                              / \
        T1  y    -- Left Rotate ->       x   T3
           / \                          / \
          T2 T3                        T1 T2
        """
        y = x.right
        assert y is not None
        T2 = y.left

        # Perform rotation
        y.left = x
        x.right = T2

        # Update heights
        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def insert(self, key: float, data: Any) -> None:
        """Public method to insert a key-data pair."""
        self.root = self._insert_node(self.root, key, data)
        self.size += 1

    def _insert_node(self, node: Optional[AVLNode], key: float, data: Any) -> AVLNode:
        # 1. Normal BST insertion
        if not node:
            return AVLNode(key, data)

        if abs(key - node.key) < 1e-9:
            # Handle duplicate keys by grouping into data_list
            node.data_list.append(data)
            return node
        elif key < node.key:
            node.left = self._insert_node(node.left, key, data)
        else:
            node.right = self._insert_node(node.right, key, data)

        # 2. Update height of ancestor node
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        # 3. Get the balance factor
        balance = self._get_balance(node)

        # 4. If unbalanced, handle the 4 rotation cases:
        # Case 1 - Left Left
        if balance > 1 and node.left and key < node.left.key:
            return self._right_rotate(node)

        # Case 2 - Right Right
        if balance < -1 and node.right and key > node.right.key:
            return self._left_rotate(node)

        # Case 3 - Left Right
        if balance > 1 and node.left and key > node.left.key:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        # Case 4 - Right Left
        if balance < -1 and node.right and key < node.right.key:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def _min_value_node(self, node: AVLNode) -> AVLNode:
        current = node
        while current.left is not None:
            current = current.left
        return current

    def delete(self, key: float, data_id: Optional[str] = None) -> bool:
        """Public method to delete by key (or specific data record by id)."""
        deleted_flag = [False]
        self.root = self._delete_node(self.root, key, data_id, deleted_flag)
        if deleted_flag[0]:
            self.size -= 1
        return deleted_flag[0]

    def _delete_node(self, node: Optional[AVLNode], key: float, data_id: Optional[str], deleted_flag: List[bool]) -> Optional[AVLNode]:
        if not node:
            return None

        if key < node.key - 1e-9:
            node.left = self._delete_node(node.left, key, data_id, deleted_flag)
        elif key > node.key + 1e-9:
            node.right = self._delete_node(node.right, key, data_id, deleted_flag)
        else:
            # Key matches
            if data_id:
                # Remove specific item
                original_len = len(node.data_list)
                node.data_list = [d for d in node.data_list if (isinstance(d, dict) and d.get("id") != data_id) or (not isinstance(d, dict) and d != data_id)]
                if len(node.data_list) < original_len:
                    deleted_flag[0] = True
                if len(node.data_list) > 0:
                    return node  # Still has other data entries at this key
            else:
                deleted_flag[0] = True

            # If node has no data items left or data_id wasn't specified, delete this node
            if not deleted_flag[0] and not data_id:
                deleted_flag[0] = True

            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # Node with two children: Get the inorder successor (smallest in the right subtree)
            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.data_list = list(temp.data_list)
            # Delete the inorder successor
            node.right = self._delete_node(node.right, temp.key, None, [False])

        if not node:
            return None

        # Update height
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        # Check balance
        balance = self._get_balance(node)

        # 4 Balance cases:
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._right_rotate(node)
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._left_rotate(node)
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def search(self, key: float) -> List[Any]:
        """Exact search for a key in the AVL tree. Returns list of matching records."""
        current = self.root
        while current:
            if abs(key - current.key) < 1e-9:
                return current.data_list
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        return []

    def range_query(self, min_key: float, max_key: float) -> List[Tuple[float, List[Any]]]:
        """Finds all records where min_key <= key <= max_key."""
        results: List[Tuple[float, List[Any]]] = []

        def _traverse(node: Optional[AVLNode]):
            if not node:
                return
            if node.key > min_key:
                _traverse(node.left)
            if min_key <= node.key <= max_key:
                results.append((node.key, node.data_list))
            if node.key < max_key:
                _traverse(node.right)

        _traverse(self.root)
        return results

    def in_order_traversal(self) -> List[Tuple[float, List[Any]]]:
        """Returns sorted list of (key, data_list) tuples."""
        results: List[Tuple[float, List[Any]]] = []

        def _in_order(node: Optional[AVLNode]):
            if not node:
                return
            _in_order(node.left)
            results.append((node.key, node.data_list))
            _in_order(node.right)

        _in_order(self.root)
        return results

    def display_tree(self) -> str:
        """Returns ASCII visual representation of the AVL tree."""
        if not self.root:
            return "<Empty AVL Tree>"

        lines = []
        def _build_str(node: Optional[AVLNode], prefix: str = "", is_left: bool = True):
            if not node:
                return
            connector = "|-- " if is_left else "\\-- "
            records_summary = f"[{len(node.data_list)} item(s)]"
            lines.append(f"{prefix}{connector}Key: {node.key} (H={node.height}, BF={self._get_balance(node)}) {records_summary}")
            new_prefix = prefix + ("|   " if is_left else "    ")
            if node.left or node.right:
                if node.left:
                    _build_str(node.left, new_prefix, True)
                else:
                    lines.append(f"{new_prefix}|-- (None)")
                if node.right:
                    _build_str(node.right, new_prefix, False)
                else:
                    lines.append(f"{new_prefix}\\-- (None)")

        lines.append(f"Root: Key: {self.root.key} (H={self.root.height}, BF={self._get_balance(self.root)})")
        if self.root.left:
            _build_str(self.root.left, "", True)
        if self.root.right:
            _build_str(self.root.right, "", False)

        return "\n".join(lines)


# ==============================================================================
# 2. Binary Heap (Priority Queue) Implementation
# ==============================================================================

class HeapItem:
    """Item wrapper for priority queue operations."""
    def __init__(self, priority: float, data: Any):
        self.priority: float = priority
        self.data: Any = data

    def __repr__(self) -> str:
        name = self.data.get("id", str(self.data)) if isinstance(self.data, dict) else str(self.data)
        return f"HeapItem(P={self.priority:.2f}, {name})"


class MaxBinaryHeap:
    """
    Max Binary Heap for retrieving highest-priority matches.
    Provides O(log N) push and pop, and O(1) peek.
    """
    def __init__(self):
        self.heap: List[HeapItem] = []

    def __len__(self) -> int:
        return len(self.heap)

    def is_empty(self) -> bool:
        return len(self.heap) == 0

    def _parent(self, i: int) -> int:
        return (i - 1) // 2

    def _left_child(self, i: int) -> int:
        return 2 * i + 1

    def _right_child(self, i: int) -> int:
        return 2 * i + 2

    def _swap(self, i: int, j: int) -> None:
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def _sift_up(self, i: int) -> None:
        while i > 0 and self.heap[i].priority > self.heap[self._parent(i)].priority:
            p = self._parent(i)
            self._swap(i, p)
            i = p

    def _sift_down(self, i: int) -> None:
        max_idx = i
        n = len(self.heap)

        l = self._left_child(i)
        if l < n and self.heap[l].priority > self.heap[max_idx].priority:
            max_idx = l

        r = self._right_child(i)
        if r < n and self.heap[r].priority > self.heap[max_idx].priority:
            max_idx = r

        if i != max_idx:
            self._swap(i, max_idx)
            self._sift_down(max_idx)

    def push(self, priority: float, data: Any) -> None:
        """Insert a record with specified priority score."""
        item = HeapItem(priority, data)
        self.heap.append(item)
        self._sift_up(len(self.heap) - 1)

    def pop_max(self) -> Optional[HeapItem]:
        """Extract and return the item with the highest priority."""
        if self.is_empty():
            return None
        max_item = self.heap[0]
        last_item = self.heap.pop()
        if len(self.heap) > 0:
            self.heap[0] = last_item
            self._sift_down(0)
        return max_item

    def peek(self) -> Optional[HeapItem]:
        """Return the highest priority item without removing it."""
        return self.heap[0] if not self.is_empty() else None

    def heapify(self, items: List[Tuple[float, Any]]) -> None:
        """Build heap in O(N) linear time from existing list of (priority, data)."""
        self.heap = [HeapItem(p, d) for p, d in items]
        # Start from last non-leaf node
        for i in range((len(self.heap) // 2) - 1, -1, -1):
            self._sift_down(i)

    def display_heap(self) -> str:
        """Returns string representation of the heap array and level structure."""
        if not self.heap:
            return "<Empty Heap>"
        lines = [f"Heap Size: {len(self.heap)}"]
        lines.append("Array view: " + ", ".join([f"[{it.priority:.1f}: {it.data.get('id', 'item') if isinstance(it.data, dict) else it.data}]" for it in self.heap]))
        return "\n".join(lines)


# ==============================================================================
# Demonstration & Verification Function
# ==============================================================================

def run_phase1_demo():
    from dataset.sample_data import DEMAND_RECORDS, SUPPLY_RECORDS

    print("================================================================================")
    print("PHASE 1 DEMO: Core Data Structures (AVL Tree & Binary Heap)")
    print("================================================================================")

    # 1. AVL Tree by Price for Supply Records
    print("\n--- 1.1 Indexing Supply Records into AVL Tree by unit_price ---")
    supply_avl = AVLTree(key_attribute_name="unit_price")
    for s in SUPPLY_RECORDS:
        supply_avl.insert(s["unit_price"], s)
        print(f"  Inserted: {s['id']} ({s['supplier']}) @ ${s['unit_price']}")

    print("\nAVL Tree Structure after insertions (Balanced):")
    print(supply_avl.display_tree())

    # Search in AVL
    target_price = 40.0
    print(f"\nExact Search for unit_price = ${target_price}:")
    search_res = supply_avl.search(target_price)
    for r in search_res:
        print(f"  Found: {r['id']} - {r['supplier']} (${r['unit_price']})")

    # Range Query in AVL
    min_p, max_p = 30.0, 120.0
    print(f"\nRange Query for unit_price between [${min_p}, ${max_p}]:")
    range_res = supply_avl.range_query(min_p, max_p)
    for price, records in range_res:
        for r in records:
            print(f"  Price ${price}: {r['id']} ({r['supplier']}, Qty: {r['available_qty']})")

    # Deletion in AVL
    print("\nDeleting Supplier S202 ($88.0) from AVL Tree...")
    supply_avl.delete(88.0, data_id="S202")
    print(supply_avl.display_tree())

    # 2. Binary Heap for Prioritizing Demands by Urgency & Budget
    print("\n--- 1.2 Priority Queue (Binary Max-Heap) for Demand Urgency ---")
    demand_heap = MaxBinaryHeap()

    for d in DEMAND_RECORDS:
        # Priority composite score: urgency * 10 + budget * 0.1
        priority_score = d["urgency"] * 10.0 + d["max_price"] * 0.1
        demand_heap.push(priority_score, d)
        print(f"  Queued Demand: {d['id']} ({d['client']}) -> Priority Score: {priority_score:.2f} (Urgency={d['urgency']})")

    print("\nHeap State:")
    print(demand_heap.display_heap())

    print("\nExtracting Demands in Order of Highest Priority:")
    rank = 1
    while not demand_heap.is_empty():
        top = demand_heap.pop_max()
        d = top.data
        print(f"  #{rank}: Score {top.priority:.2f} | Demand {d['id']}: {d['client']} (Urgency: {d['urgency']}/10, Budget: ${d['max_price']})")
        rank += 1


if __name__ == "__main__":
    run_phase1_demo()
