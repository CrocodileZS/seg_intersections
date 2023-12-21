import heapq
# wrong answer

# Classes Definition
class TreeNode:
    def __init__(self, key):
        self.key = key        # key is a tuple (x1, x2, x3)
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
            if key[0] < node.left.key[0]:  # Left Left
                return self.right_rotate(node)
            else:  # Left Right
                node.left = self.left_rotate(node.left)
                return self.right_rotate(node)
        if balance < -1:
            if key[0] > node.right.key[0]:  # Right Right
                return self.left_rotate(node)
            else:  # Right Left
                node.right = self.right_rotate(node.right)
                return self.left_rotate(node)
        return node

    def insert(self, node, key):
        if not node:
            return TreeNode(key)
        if key[0] < node.key[0]:
            node.left = self.insert(node.left, key)
        elif key[0] > node.key[0]:
            node.right = self.insert(node.right, key)
        else:
            return node  # Duplicate keys not allowed

        self.update_height(node)
        return self.rebalance(node, key)

    def min_value_node(self, node):
        while node.left is not None:
            node = node.left
        return node

    def delete(self, node, key):
        if not node:
            return node
        if key[0] < node.key[0]:
            node.left = self.delete(node.left, key)
        elif key[0] > node.key[0]:
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

    def insert_tuple(self, key):
        self.root = self.insert(self.root, key)

    def delete_tuple(self, key):
        self.root = self.delete(self.root, key)

    def in_order_traversal(self, node, result=None):
        if result is None:
            result = []
        if node is not None:
            self.in_order_traversal(node.left, result)
            result.append(node.key[0])
            self.in_order_traversal(node.right, result)
        return result


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
    # (seg, y, param) param=2 means the endpoint is a horizontal segment
    maxpq.push((values, values[2], 2))
    # maxpq.push((values, values[2], 2))

# read the input vertical segments and push endpoints into maxpq
ver_seg_num = int(input().split()[2])

for _ in range(ver_seg_num):
    line = input()
    values = list(map(int, line.split()))
    # (seg, y, param) param=0 means the endpoint is a start point, point=1 means the endpoint is an end point
    maxpq.push((values, values[1], 1))
    maxpq.push((values, values[2], 0))


avl = AVLTree()
res = 0

while not maxpq.is_empty():
    seg, cur_y, param = maxpq.pop()
    if param == 0:
        avl.insert_tuple(seg)
    if param == 1:
        avl.delete_tuple(seg)
    if param == 2:
        cur_ver_segs_x = avl.in_order_traversal(avl.root)
        i = 0
        while i < len(cur_ver_segs_x) and cur_ver_segs_x[i] < seg[0]:
            i = i + 1
        j = i
        while j < len(cur_ver_segs_x) and cur_ver_segs_x[j] <= seg[1]:
            j = j + 1
        res = res + j - i


print(res)


