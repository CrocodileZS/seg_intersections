import heapq
#O((m+n+k)log(m+n))

# Classes Definition
class TreeNode:
    def __init__(self, key):
        self.key = key        # key is an int
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None

    def get_height(self, node):
        if not node:
            return 0
        return node.height

    def update_height(self, node):
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

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
        self.update_height(z)
        self.update_height(y)
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
        self.update_height(z)
        self.update_height(y)
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

        self.update_height(node)
        return self.rebalance(node, key)

    def min_value_node(self, node):
        while node.left is not None:
            node = node.left
        return node

    def delete(self, node, key):
        if not node:
            return node
        if key < node.key:
            node.left = self.delete(node.left, key)
        elif key > node.key:
            node.right = self.delete(node.right, key)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            temp = self.min_value_node(node.right)
            node.key = temp.key
            node.right = self.delete(node.right, temp.key)

        self.update_height(node)
        return self.rebalance(node, key)

    def insert_x(self, key):
        self.root = self.insert(self.root, key)

    def delete_x(self, key):
        self.root = self.delete(self.root, key)

    def count_nodes_in_range(self, node, begin, end):
        # Base case: if the current node is None, return 0
        if node is None:
            return 0

        # If the current node's key is within the range, include it in the count
        # and check both subtrees.
        if begin <= node.key <= end:
            return (1 + self.count_nodes_in_range(node.left, begin, end)
                    + self.count_nodes_in_range(node.right, begin, end))

        # If the current node's key is smaller than the beginning of the range,
        # then check the right subtree because the left subtree will also be smaller.
        elif node.key < begin:
            return self.count_nodes_in_range(node.right, begin, end)

        # If the current node's key is larger than the end of the range,
        # then check the left subtree because the right subtree will also be larger.
        else:  # node.key > end
            return self.count_nodes_in_range(node.left, begin, end)


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
    # (seg, y, param) param=2 means the endpoint is a start point, point=0 means the endpoint is an end point of the segments
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
        res = res + avl.count_nodes_in_range(avl.root, seg[0], seg[1])


print(res)


