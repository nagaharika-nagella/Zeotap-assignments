import ast

# Node structure for the AST
class Node:
    def __init__(self, node_type, value=None, left=None, right=None):
        self.node_type = node_type  # "operator" or "operand"
        self.value = value  # Operator: AND, OR / Operand: (age > 30)
        self.left = left  # Left child node
        self.right = right  # Right child node

    def __repr__(self):
        return f"Node(type={self.node_type}, value={self.value}, left={self.left}, right={self.right})"


# Function to create AST from rule string
def create_rule(rule_string):
    # Replace uppercase AND/OR with lowercase and/or for Python syntax
    rule_string = rule_string.replace("AND", "and").replace("OR", "or")
    
    # Parse the rule string into an Abstract Syntax Tree (AST)
    tree = ast.parse(rule_string, mode='eval')
    return convert_to_ast(tree.body)

# Convert the parsed AST into the custom Node structure
def convert_to_ast(expr):
    if isinstance(expr, ast.BoolOp):  # AND/OR operations
        op_type = "AND" if isinstance(expr.op, ast.And) else "OR"
        return Node("operator", op_type, convert_to_ast(expr.values[0]), convert_to_ast(expr.values[1]))
    elif isinstance(expr, ast.Compare):  # Comparison operations
        left = expr.left.id  # Get the left operand (e.g., 'age')
        comparator = expr.ops[0]
        
        # Map the comparator to its operator
        if isinstance(comparator, ast.Gt):
            operator = ">"
        elif isinstance(comparator, ast.Lt):
            operator = "<"
        elif isinstance(comparator, ast.Eq):
            operator = "=="
        
        # Use 'value' attribute for constants (fixing the deprecation warning)
        right = expr.comparators[0].value if isinstance(expr.comparators[0], ast.Constant) else expr.comparators[0].s
        return Node("operand", f"{left} {operator} {right}")

# Combine multiple rules into one AST
def combine_rules(rules):
    if not rules:
        return None
    root = create_rule(rules[0])
    for rule in rules[1:]:
        new_rule_ast = create_rule(rule)
        root = Node("operator", "AND", root, new_rule_ast)  # Combine using AND
    return root

# Evaluate the AST against provided data
def evaluate_rule(json_data, ast_node):
    if ast_node.node_type == "operand":
        return eval_operand(json_data, ast_node.value)
    elif ast_node.node_type == "operator":
        if ast_node.value == "AND":
            return evaluate_rule(json_data, ast_node.left) and evaluate_rule(json_data, ast_node.right)
        elif ast_node.value == "OR":
            return evaluate_rule(json_data, ast_node.left) or evaluate_rule(json_data, ast_node.right)

def eval_operand(json_data, condition):
    key, operator, value = condition.split(" ")
    value = int(value) if value.isdigit() else value.strip("'")
    if operator == ">":
        return json_data[key] > value
    elif operator == "<":
        return json_data[key] < value
    elif operator == "==":
        return json_data[key] == value

# Sample rules
rule1 = "((age > 30 AND department == 'Sales') OR (age < 25 AND department == 'Marketing')) AND (salary > 50000 OR experience > 5)"
rule2 = "((age > 30 AND department == 'Marketing')) AND (salary > 20000 OR experience > 5)"

# Create AST for the individual rules
ast_rule1 = create_rule(rule1)
ast_rule2 = create_rule(rule2)

# Combine the rules
combined_ast = combine_rules([rule1, rule2])

# Sample data to evaluate the rules
data1 = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
data2 = {"age": 23, "department": "Marketing", "salary": 45000, "experience": 2}

# Evaluate the rules with the data
print(evaluate_rule(data1, combined_ast))  # True or False
print(evaluate_rule(data2, combined_ast))  # True or False
