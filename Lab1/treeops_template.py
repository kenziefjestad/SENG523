import sys
import ast
import zss

class NodeVisitor(ast.NodeVisitor):

    len = 0

    vars = {}

    final_var = None
    
    def generic_visit(self, node):
        # if node.__class__.__name__ == "Assign":
        #     print("Assignment")
        # print(f'entering {node.__class__.__name__}')
        assign_eq(node, NodeVisitor.vars)
        if node.__class__.__name__ != "Load" and node.__class__.__name__ != "Store":
            NodeVisitor.len += 1
        # elif node.__class__.__name__ != "Store":
        #     NodeVisitor.len += 1
            # print(f'Skipping {node.__class__.__name__}')
        # NodeVisitor.len += 1
        super().generic_visit(node)
        # print(f'leaving {node.__class__.__name__}')

    # def compare_trees(self, node1, node2):
    #     print(f'comparing {node1.__class__.__name__} to {node2.__class__.__name__}')
    #     compare_nodes(ast.iter_child_nodes(node1), ast.iter_child_nodes(node2))

    @staticmethod
    def get_children(node):
        # print(f'getting children of {node.__class__.__name__}')
        #print(list(ast.iter_child_nodes(node)))
        return list(ast.iter_child_nodes(node))

    @staticmethod
    def get_label(node):
        # print(f'getting label of {node.__class__.__name__}')
        # print(node.__class__.__name__)
        # return type(node)
        return node.__class__.__name__

def test():
    tree = ast.parse("def iseven(x):\n    if x % 2:\n        return False\n    else:\n        return True")
    tree2 = ast.parse("def isodd(x):\n    if x % 2:\n        return True\n    else:\n        return False")

    tree3 = ast.parse("def f(x):\n    return x")

    # print(ast.dump(tree3, indent = 2))

    v = NodeVisitor()
    v.visit(tree)
    print(f'Number of nodes: {NodeVisitor.len}')

    # print(NodeVisitor.get_label(tree))
    # print(NodeVisitor.get_children(tree))
    # print(NodeVisitor.get_label(tree2))

def compare_nodes(n1, n2):
    if type(n1) != type(n2):
        return False

    for (field1, value1), (field2, value2) in zip(ast.iter_fields(n1), ast.iter_fields(n2)):
        if field1 != field2:
            return False

        if isinstance(value1, list):
            if len(value1) != len(value2):
                return False
            for child1, child2 in zip(value1, value2):
                if not compare_nodes(child1, child2):
                    return False

        elif isinstance(value1, ast.AST):
            if not compare_nodes(value1, value2):
                return False

        else:
            if value1 != value2:
                return False

    return True

def expr_eq(node, vars):
    # if node.__class__.__name__ == "Constant":
    #     print(ast.literal_eval(node))
    # pass

    # BinOp with left and right side
    # check if left is binop, if so, recurse
    # if not, check if left is a variable, if so, look up in vars
    # if not, it's a constant, so just use it
    # do the same for right side
    # then do the operation and return the result

    if node.__class__.__name__ == "BinOp":
        left = expr_eq(node.left, vars)
        right = expr_eq(node.right, vars)
        if left is not None and right is not None:
            if node.op.__class__.__name__ == "Add":
                return left + right
            elif node.op.__class__.__name__ == "Mult":
                return left * right
    elif node.__class__.__name__ == "Name":
        return vars.get(node.id, None)
    elif node.__class__.__name__ == "Constant":
        return ast.literal_eval(node)
    return None

def assign_eq(node, vars):
    # check if node is an Assign node
    # if so, get the target name and evaluate the value expression
    # store the result in vars under the target name
    if node.__class__.__name__ == "Assign":
        target = node.targets[0].id
        value = expr_eq(node.value, vars)
        if value is not None:
            vars[target] = value
            NodeVisitor.final_var = value

def main():
    if len(sys.argv) == 4 and sys.argv[1] == "cmp":
        return do_cmp(sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 4 and sys.argv[1] == "dst":
        return do_dst(sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 3 and sys.argv[1] == "run":
        return do_run(sys.argv[2])
    else:
        print("Usage: python treeops.py <cmd> <file 1> <optional file 2>")
        return -1

# Provide the solution to Exercise 2 by implementing the function below
def do_cmp(fname1, fname2):
    n1 = ast.parse(open(fname1).read())
    n2 = ast.parse(open(fname2).read())
    # print(ast.dump(n1, indent = 2))
    # print(ast.dump(n2, indent = 2))
    # equals = recursive_eq(n1, n2)
    # print(equals)
    # print("WHOPS! 'cmd' command not implemented!")
    if compare_nodes(n1, n2):
        print("The programs are identical")
    else:
        print("The programs are not identical")
    return -1

# def label_dist(str1, str2):
#     # print(f'comparing {n1.__class__.__name__} to {n2.__class__.__name__}')
#     # if n1.__class__.__name__ == "Constant" and n2.__class__.__name__ == "Constant":
#     #     return 0
#     # elif n1.__class__.__name__ == "Name" and n2.__class__.__name__ == "Name":
#     #     return 0
#     if str1 == "Load" or str2 == "Load":
#         return 0
#     if str1 == "Store" or str2 == "Store":
#         return 0
#     # print(f'comparing {str1} to {str2}')
#     if str1 != str2:
#         return 1
#     return 0

# Provide the solution to Exercise 3 by implementing the function below
def do_dst(fname1, fname2):
    n1 = ast.parse(open(fname1).read())
    n2 = ast.parse(open(fname2).read())
    print(ast.dump(n1, indent = 2))
    # print(ast.dump(n2, indent = 2))
    dist = zss.simple_distance(n1, n2, NodeVisitor.get_children, NodeVisitor.get_label)
    v = NodeVisitor()
    v.visit(n1)
    n1_len = NodeVisitor.len
    NodeVisitor.len = 0
    v.visit(n2)
    n2_len = NodeVisitor.len
    print(f'Number of nodes in tree 1: {n1_len}')
    print(f'Number of nodes in tree 2: {n2_len}')
    normalized_dist = dist / (n1_len + n2_len)
    # print(n1_len)
    # print(n2_len)
    # print(f'{NodeVisitor.len + len(ast.dump(n2))}')
    print(f"Tree distance: {dist}")
    print(f"Normalized distance: {normalized_dist}")
    print(f"The normalized tree edit distance is {normalized_dist}")
    # print("WHOPS! 'dst' command not implemented!")
    return -1

# Provide the solution to Exercise 4 by implementing the function below
def do_run(fname):
    n = ast.parse(open(fname).read())
    # print(ast.dump(n, indent = 2))
    v = NodeVisitor()
    v.visit(n)
    # print(NodeVisitor.vars)
    print(f'The final value is {NodeVisitor.final_var}')
    # print("WHOPS! 'run' command not implemented!")
    return -1


if __name__ == "__main__":
    main()
    # test()