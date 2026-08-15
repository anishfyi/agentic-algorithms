"""Binary tree algorithms."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass


@dataclass
class TreeNode:
    """Binary tree node."""

    val: int = 0
    left: TreeNode | None = None
    right: TreeNode | None = None


def inorder_recursive(root: TreeNode | None) -> list[int]:
    """Inorder traversal (left, root, right) recursively.

    Time: O(n). Space: O(h).
    """
    result: list[int] = []

    def dfs(node: TreeNode | None) -> None:
        if not node:
            return
        dfs(node.left)
        result.append(node.val)
        dfs(node.right)

    dfs(root)
    return result


def inorder_iterative(root: TreeNode | None) -> list[int]:
    """Inorder traversal iteratively.

    Time: O(n). Space: O(h).
    """
    result: list[int] = []
    stack: list[TreeNode] = []
    current = root
    while stack or current:
        while current:
            stack.append(current)
            current = current.left
        node = stack.pop()
        result.append(node.val)
        current = node.right
    return result


def preorder_recursive(root: TreeNode | None) -> list[int]:
    """Preorder traversal (root, left, right) recursively.

    Time: O(n). Space: O(h).
    """
    result: list[int] = []

    def dfs(node: TreeNode | None) -> None:
        if not node:
            return
        result.append(node.val)
        dfs(node.left)
        dfs(node.right)

    dfs(root)
    return result


def preorder_iterative(root: TreeNode | None) -> list[int]:
    """Preorder traversal iteratively.

    Time: O(n). Space: O(h).
    """
    if not root:
        return []
    result: list[int] = []
    stack = [root]
    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return result


def postorder_recursive(root: TreeNode | None) -> list[int]:
    """Postorder traversal (left, right, root) recursively.

    Time: O(n). Space: O(h).
    """
    result: list[int] = []

    def dfs(node: TreeNode | None) -> None:
        if not node:
            return
        dfs(node.left)
        dfs(node.right)
        result.append(node.val)

    dfs(root)
    return result


def postorder_iterative(root: TreeNode | None) -> list[int]:
    """Postorder traversal iteratively.

    Time: O(n). Space: O(h).
    """
    if not root:
        return []
    result: list[int] = []
    stack: list[tuple[TreeNode, bool]] = [(root, False)]
    while stack:
        node, visited = stack.pop()
        if visited:
            result.append(node.val)
        else:
            stack.append((node, True))
            if node.right:
                stack.append((node.right, False))
            if node.left:
                stack.append((node.left, False))
    return result


def level_order(root: TreeNode | None) -> list[list[int]]:
    """Return level-order traversal as list of levels.

    Time: O(n). Space: O(n).
    """
    if not root:
        return []
    result: list[list[int]] = []
    queue: deque[TreeNode] = deque([root])
    while queue:
        level: list[int] = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    return result


def max_depth(root: TreeNode | None) -> int:
    """Return maximum depth of the tree.

    Time: O(n). Space: O(h).
    """
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))


def is_valid_bst(root: TreeNode | None) -> bool:
    """Check if binary tree is a valid BST.

    Time: O(n). Space: O(h).
    """

    def validate(node: TreeNode | None, low: float, high: float) -> bool:
        if not node:
            return True
        if not (low < node.val < high):
            return False
        return validate(node.left, low, node.val) and validate(node.right, node.val, high)

    return validate(root, float("-inf"), float("inf"))


def lowest_common_ancestor(root: TreeNode | None, p: TreeNode, q: TreeNode) -> TreeNode | None:
    """Return lowest common ancestor of p and q in a binary tree.

    Time: O(n). Space: O(h).
    """
    if not root or root is p or root is q:
        return root
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right:
        return root
    return left or right


def serialize(root: TreeNode | None) -> str:
    """Serialize binary tree to comma-separated string (BFS with null markers).

    Time: O(n). Space: O(n).
    """
    if not root:
        return ""
    values: list[str] = []
    queue: deque[TreeNode | None] = deque([root])
    while queue:
        node = queue.popleft()
        if node:
            values.append(str(node.val))
            queue.append(node.left)
            queue.append(node.right)
        else:
            values.append("#")
    while values and values[-1] == "#":
        values.pop()
    return ",".join(values)


def deserialize(data: str) -> TreeNode | None:
    """Deserialize tree from comma-separated string.

    Time: O(n). Space: O(n).
    """
    if not data:
        return None
    tokens = data.split(",")
    root = TreeNode(int(tokens[0]))
    queue: deque[TreeNode] = deque([root])
    index = 1
    while queue and index < len(tokens):
        node = queue.popleft()
        if index < len(tokens) and tokens[index] != "#":
            node.left = TreeNode(int(tokens[index]))
            queue.append(node.left)
        index += 1
        if index < len(tokens) and tokens[index] != "#":
            node.right = TreeNode(int(tokens[index]))
            queue.append(node.right)
        index += 1
    return root


def diameter(root: TreeNode | None) -> int:
    """Return diameter (longest path between any two nodes) in edges.

    Time: O(n). Space: O(h).
    """
    best = 0

    def height(node: TreeNode | None) -> int:
        nonlocal best
        if not node:
            return 0
        left = height(node.left)
        right = height(node.right)
        best = max(best, left + right)
        return 1 + max(left, right)

    height(root)
    return best


def path_sum(root: TreeNode | None, target_sum: int) -> bool:
    """Return True if tree has root-to-leaf path with given sum.

    Time: O(n). Space: O(h).
    """

    def dfs(node: TreeNode | None, remaining: int) -> bool:
        if not node:
            return False
        remaining -= node.val
        if not node.left and not node.right:
            return remaining == 0
        return dfs(node.left, remaining) or dfs(node.right, remaining)

    return dfs(root, target_sum)


def build_from_preorder_inorder(preorder: list[int], inorder: list[int]) -> TreeNode | None:
    """Build binary tree from preorder and inorder traversals.

    Time: O(n). Space: O(n).
    """
    if not preorder or not inorder:
        return None
    index_map = {value: i for i, value in enumerate(inorder)}

    def build(pre_start: int, pre_end: int, in_start: int, in_end: int) -> TreeNode | None:
        if pre_start > pre_end:
            return None
        root_val = preorder[pre_start]
        in_root = index_map[root_val]
        left_size = in_root - in_start
        root = TreeNode(root_val)
        root.left = build(pre_start + 1, pre_start + left_size, in_start, in_root - 1)
        root.right = build(pre_start + left_size + 1, pre_end, in_root + 1, in_end)
        return root

    return build(0, len(preorder) - 1, 0, len(inorder) - 1)
