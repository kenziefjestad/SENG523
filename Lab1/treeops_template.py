import sys
import ast
import zss

class MyVisitor(ast.NodeVisitor):
    def generic_visit(self, node):
        print(f'entering {node.__class__.__name__}')
        super().generic_visit(node)

def test():
    tree = ast.parse("def iseven(x):\n    if x % 2:\n        return False\n    else:\n        return True")
    print(ast.dump(tree, indent=2))
    visitor = MyVisitor()
    visitor.visit(tree)

def recursive_eq(n1, n2):
    print(f'comparing {n1.__class__.__name__} to {n2.__class__.__name__}')
    print(ast.dump(ast.iter_child_nodes(n1)))
    # if node_equals(n1, n2):
    #     print("nodes are equal")
    #     recursive_eq(n1.body, n2.body)


    # if type(n1) != type(n2):
        
    #     return False
    
def node_equals(n1, n2):
    if type(n1) == type(n2):
        return True
    return False

def main():
    print(sys.argv)
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
    print(ast.dump(n1, indent = 2))
    print(ast.dump(n2, indent = 2))
    equals = recursive_eq(n1, n2)
    print(equals)
    print("WHOPS! 'cmd' command not implemented!")
    return -1

# Provide the solution to Exercise 3 by implementing the function below
def do_dst(fname1, fname2):
    print("WHOPS! 'dst' command not implemented!")
    return -1

# Provide the solution to Exercise 4 by implementing the function below
def do_run(fname):
    print("WHOPS! 'run' command not implemented!")
    return -1


if __name__ == "__main__":
    main()
    # test()