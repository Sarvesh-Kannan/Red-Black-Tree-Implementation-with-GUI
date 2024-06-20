import tkinter as tk
from tkinter import messagebox
import sys

# Node creation
class Node:
    def _init_(self, item):
        self.item = item
        self.parent = None
        self.left = None
        self.right = None
        self.color = 0  # New nodes are always black

class RedBlackTree:
    def _init_(self):
        self.TNULL = Node(0)
        self.TNULL.color = 0  # TNULL is black
        self.TNULL.left = None
        self.TNULL.right = None
        self.root = self.TNULL

    def pre_order_helper(self, node):
        if node != self.TNULL:
            sys.stdout.write(str(node.item) + " ")
            self.pre_order_helper(node.left)
            self.pre_order_helper(node.right)

    def in_order_helper(self, node):
        if node != self.TNULL:
            self.in_order_helper(node.left)
            sys.stdout.write(str(node.item) + " ")
            self.in_order_helper(node.right)

    def post_order_helper(self, node):
        if node != self.TNULL:
            self.post_order_helper(node.left)
            self.post_order_helper(node.right)
            sys.stdout.write(str(node.item) + " ")

    def search_tree_helper(self, node, key):
        if node == self.TNULL or key == node.item:
            return node

        if key < node.item:
            return self.search_tree_helper(node.left, key)
        return self.search_tree_helper(node.right, key)

    def delete_fix(self, x):
        while x != self.root and x.color == 0:
            if x == x.parent.left:
                s = x.parent.right
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if s.left.color == 0 and s.right.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.right.color == 0:
                        s.left.color = 0
                        s.color = 1
                        self.right_rotate(s)
                        s = x.parent.right

                    s.color = x.parent.color
                    x.parent.color = 0
                    s.right.color = 0
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if s.right.color == 0 and s.left.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.left.color == 0:
                        s.right.color = 0
                        s.color = 1
                        self.left_rotate(s)
                        s = x.parent.left

                    s.color = x.parent.color
                    x.parent.color = 0
                    s.left.color = 0
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = 0

    def __rb_transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def delete_node_helper(self, node, key):
        z = self.TNULL
        while node != self.TNULL:
            if node.item == key:
                z = node

            if node.item <= key:
                node = node.right
            else:
                node = node.left

        if z == self.TNULL:
            print("Cannot find key in the tree")
            return

        y = z
        y_original_color = y.color
        if z.left == self.TNULL:
            x = z.right
            self.__rb_transplant(z, z.right)
        elif z.right == self.TNULL:
            x = z.left
            self.__rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.__rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.__rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == 0:
            self.delete_fix(x)

    def fix_insert(self, k):
        while k.parent.color == 1:
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right

                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 0

    def preorder(self):
        self.pre_order_helper(self.root)

    def inorder(self):
        self.in_order_helper(self.root)

    def postorder(self):
        self.post_order_helper(self.root)

    def searchTree(self, k):
        return self.search_tree_helper(self.root, k)

    def minimum(self, node):
        while node.left != self.TNULL:
            node = node.left
        return node

    def maximum(self, node):
        while node.right != self.TNULL:
            node = node.right
        return node

    def successor(self, x):
        if x.right != self.TNULL:
            return self.minimum(x.right)

        y = x.parent
        while y != self.TNULL and x == y.right:
            x = y
            y = y.parent
        return y

    def predecessor(self, x):
        if x.left != self.TNULL:
            return self.maximum(x.left)

        y = x.parent
        while y != self.TNULL and x == y.left:
            x = y
            y = y.parent

        return y

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def insert(self, key):
        node = Node(key)
        node.parent = None
        node.item = key
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = 1  # New nodes are red

        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            if node.item < x.item:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y == None:
            self.root = node
        elif node.item < y.item:
            y.left = node
        else:
            y.right = node

        if node.parent == None:
            node.color = 0
            return

        if node.parent.parent == None:
            return

        self.fix_insert(node)

    def get_root(self):
        return self.root

    def delete_node(self, item):
        self.delete_node_helper(self.root, item)
    
    def __print_tree_visual_helper(self, node, indent="", last='updown'):
        if node != self.TNULL:
            sys.stdout.write(indent)
            if last == 'updown':
                sys.stdout.write("Root----")
                indent += "        "
            elif last == 'right':
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "

            s_color = "RED" if node.color == 1 else "BLACK"
            print(str(node.item) + "(" + s_color + ")")
            self.__print_tree_visual_helper(node.left, indent, 'left')
            self.__print_tree_visual_helper(node.right, indent, 'right')
            
    def print_tree_visual(self, node):
        self.__print_tree_visual_helper(node)

class RBTreeApp:
    def _init_(self, root):
        self.rb_tree = RedBlackTree()
        self.root = root
        self.root.title("Red-Black Tree Visualization")

        self.canvas = tk.Canvas(self.root, width=800, height=600, bg='white')
        self.canvas.pack()

        self.controls_frame = tk.Frame(self.root)
        self.controls_frame.pack()

        self.entry = tk.Entry(self.controls_frame)
        self.entry.grid(row=0, column=0)

        self.insert_button = tk.Button(self.controls_frame, text="Insert", command=self.insert_node)
        self.insert_button.grid(row=0, column=1)

        self.delete_button = tk.Button(self.controls_frame, text="Delete", command=self.delete_node)
        self.delete_button.grid(row=0, column=2)

        self.print_button = tk.Button(self.controls_frame, text="Print Tree", command=self.print_tree)
        self.print_button.grid(row=0, column=3)

    def insert_node(self):
        try:
            item = int(self.entry.get())
            self.rb_tree.insert(item)
            self.entry.delete(0, tk.END)
            self.display_tree()
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid integer")

    def delete_node(self):
        try:
            item = int(self.entry.get())
            self.rb_tree.delete_node(item)
            self.entry.delete(0, tk.END)
            self.display_tree()
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid integer")

    def print_tree(self):
        self.rb_tree.print_tree_visual(self.rb_tree.get_root())

    def display_tree(self):
        self.canvas.delete("all")
        self.display_tree_helper(self.rb_tree.get_root(), 400, 50, 200)

    def display_tree_helper(self, node, x, y, dx):
        if node != self.rb_tree.TNULL:
            self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="red" if node.color == 1 else "black")
            self.canvas.create_text(x, y, text=str(node.item), fill="white")

            if node.left != self.rb_tree.TNULL:
                self.canvas.create_line(x - 10, y + 10, x - dx + 10, y + 50 - 10)
                self.display_tree_helper(node.left, x - dx, y + 50, dx // 2)

            if node.right != self.rb_tree.TNULL:
                self.canvas.create_line(x + 10, y + 10, x + dx - 10, y + 50 - 10)
                self.display_tree_helper(node.right, x + dx, y + 50, dx // 2)

if __name__ == "_main_":
    root = tk.Tk()
    app = RBTreeApp(root)
    root.mainloop()
