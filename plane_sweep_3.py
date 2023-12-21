import heapq
# O((m+n)log(m+n))

# Classes Definition
class TreeNode:
    def __init__(self, key):
        self.key = key        # key is an int
        self.left = None
        self.right = None
        self.height = 1
        self.children_count = 1  # Initialize count of children


class AVLTree:
    def __init__(self):
        self.root = None

    def get_height(self, node):
        if not node:
            return 0
        return node.height

    def update_height_and_count(self, node):
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        # Update the children count as sum of children of left and right plus 1 (the node itself)
        node.children_count = 1 + (node.left.children_count if node.left else 0) + (node.right.children_count if node.right else 0)

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def right_rotate(self, z):
        y = z.left
        if y is None:  # Check if y is not None
            return z

        T3 = y.right

        # Perform rotation
        y.right = z
        z.left = T3

        # Update heights
        self.update_height_and_count(z)
        self.update_height_and_count(y)
        return y

    def left_rotate(self, z):
        y = z.right
        if y is None:  # Check if y is not None
            return z

        T2 = y.left

        # Perform rotation
        y.left = z
        z.right = T2

        # Update heights
        self.update_height_and_count(z)
        self.update_height_and_count(y)
        return y

    def rebalance(self, node, key):
        balance = self.get_balance(node)
        if balance > 1:
            if key < node.left.key:  # Left Left
                return self.right_rotate(node)
            else:  # Left Right
                node.left = self.left_rotate(node.left)
                return self.right_rotate(node)
        if balance < -1:
            if key > node.right.key:  # Right Right
                return self.left_rotate(node)
            else:  # Right Left
                node.right = self.right_rotate(node.right)
                return self.left_rotate(node)
        return node

    def insert(self, node, key):
        if not node:
            return TreeNode(key)
        if key <= node.key:
            node.left = self.insert(node.left, key)
        else:
            node.right = self.insert(node.right, key)

        self.update_height_and_count(node)  # Update height and count after insertion
        return self.rebalance(node, key)

    def delete(self, node, key):
        if not node:
            return node
        if key < node.key:
            node.left = self.delete(node.left, key)
        elif key > node.key:
            node.right = self.delete(node.right, key)
        else:
            if not node.left:
                temp = node.right
                node = None  # Delete the node
                return temp
            elif not node.right:
                temp = node.left
                node = None  # Delete the node
                return temp
            temp = self.min_value_node(node.right)
            node.key = temp.key
            node.right = self.delete(node.right, temp.key)

        if not node:  # If the tree had only one node then return
            return node

        self.update_height_and_count(node)  # Update height and count after deletion
        return self.rebalance(node, key)

    def min_value_node(self, node):
        while node.left is not None:
            node = node.left
        return node

    def insert_x(self, key):
        self.root = self.insert(self.root, key)

    def delete_x(self, key):
        self.root = self.delete(self.root, key)

    def total_nodes(self):
        """
        Return the total number of nodes in the AVL tree by checking the children_count
        of the root node.
        """
        if self.root:
            return self.root.children_count
        else:
            return 0

    def count_geq(self, node, x):
        """
        Count the number of nodes in the AVL tree greater than or equal to x.
        """
        if not node:
            return 0

        # If node's key is greater than or equal to x, count the node, its right subtree,
        # and continue searching the left subtree.
        if node.key >= x:
            right_count = node.right.children_count if node.right else 0
            return 1 + right_count + self.count_geq(node.left, x)

        # If node's key is less than x, all nodes in the left subtree are also less than x,
        # so move to the right subtree.
        else:
            return self.count_geq(node.right, x)

    def count_leq(self, node, x):
        """
        Count the number of nodes in the AVL tree less than or equal to x.
        """
        if not node:
            return 0

        # If node's key is less than or equal to x, count the node, its left subtree,
        # and continue searching the right subtree.
        if node.key <= x:
            left_count = node.left.children_count if node.left else 0
            return 1 + left_count + self.count_leq(node.right, x)

        # If node's key is greater than x, all nodes in the right subtree are also greater than x,
        # so move to the left subtree.
        else:
            return self.count_leq(node.left, x)


class MaxPriorityQueue:
    def __init__(self):
        self.heap = []

    def push(self, point):
        # Negate both first and third dimensions for max-heap behavior
        heapq.heappush(self.heap, (-point[1], -point[2], point[0]))

    def pop(self):
        y, param, x = heapq.heappop(self.heap)
        # Restore the original values by negating them again
        return (x, -y, -param)

    def peek(self):
        if self.heap:
            y, param, x = self.heap[0]
            # Restore the original values
            return (x, -y, -param)
        return None

    def is_empty(self):
        return len(self.heap) == 0


# read the input horizontal segments and push endpoints into maxpq
maxpq = MaxPriorityQueue()
hor_seg_num = int(input().split()[2])

for _ in range(hor_seg_num):
    line = input()
    values = list(map(int, line.split()))
    # (seg, y, param) param=1 means the endpoint is a horizontal segment
    maxpq.push((values, values[2], 1))
    # maxpq.push((values, values[2], 2))

# read the input vertical segments and push endpoints into maxpq
ver_seg_num = int(input().split()[2])

for _ in range(ver_seg_num):
    line = input()
    values = list(map(int, line.split()))
    # (seg, y, param) param=2 means the endpoint is a start point, point=0 means the endpoint is an end point
    maxpq.push((values, values[1], 0))
    maxpq.push((values, values[2], 2))


avl = AVLTree()
res = 0

while not maxpq.is_empty():
    seg, cur_y, param = maxpq.pop()
    if param == 2:
        avl.insert_x(seg[0])
    if param == 0:
        avl.delete_x(seg[0])
    if param == 1:
        res = res + avl.count_geq(avl.root, seg[0]) + avl.count_leq(avl.root, seg[1]) - avl.total_nodes()


print(res)