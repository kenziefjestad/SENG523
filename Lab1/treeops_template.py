import sys
import ast
import zss

class NodeVisitor(ast.NodeVisitor):
    
    def generic_visit(self, node):
        print(f'entering {node.__class__.__name__}')
        super().generic_visit(node)
        print(f'leaving {node.__class__.__name__}')

    def compare_trees(self, node1, node2):
        print(f'comparing {node1.__class__.__name__} to {node2.__class__.__name__}')
        compare_nodes(ast.iter_child_nodes(node1), ast.iter_child_nodes(node2))

def test():
    tree = ast.parse("def iseven(x):\n    if x % 2:\n        return False\n    else:\n        return True")
    tree2 = ast.parse("def isodd(x):\n    if x % 2:\n        return True\n    else:\n        return False")

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
        print("The programs are different")
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