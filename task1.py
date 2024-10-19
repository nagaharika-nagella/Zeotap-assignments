class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.node_type = node_type  # "operator" or "operand"
        self.left = left  # Left child node
        self.right = right  # Right child node
        self.value = value  # Value for operand nodes (e.g., number for comparisons)

def precedence(op):
    precedence_map = {'AND': 1, 'OR': 1, '>': 2, '<': 2, '=': 2}
    return precedence_map.get(op, 0)

def apply_op(a, b, op):
    operations = {
        'AND': lambda a, b: a and b,
        'OR': lambda a, b: a or b,
        '>': lambda a, b: a > b,
        '<': lambda a, b: a < b,
        '=': lambda a, b: a == b
    }
    return operations[op](a, b)

def convert_to_postfix(expression):
    tokens = expression.split()
    stack = []
    output = []
    
    for token in tokens:
        if token.isnumeric() or token.isalpha() or token.startswith("'"):
            output.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # Remove '(' from stack
        else:
            while stack and precedence(stack[-1]) >= precedence(token):
                output.append(stack.pop())
            stack.append(token)
    
    while stack:
        output.append(stack.pop())
    
    return output

def build_ast(postfix_expr):
    stack = []
    
    for token in postfix_expr:
        if token.isnumeric() or token.isalpha() or token.startswith("'"):
            stack.append(Node("operand", value=token))
        else:
            right = stack.pop()
            left = stack.pop()
            stack.append(Node("operator", left=left, right=right, value=token))
    
    return stack[0]

def create_rule(rule_string):
    postfix_expr = convert_to_postfix(rule_string)
    return build_ast(postfix_expr)

def combine_rules(rule_asts):
    """Combine multiple ASTs using AND operator"""
    if len(rule_asts) == 1:
        return rule_asts[0]
    combined_ast = Node("operator", left=rule_asts[0], right=rule_asts[1], value="AND")
    for i in range(2, len(rule_asts)):
        combined_ast = Node("operator", left=combined_ast, right=rule_asts[i], value="AND")
    return combined_ast

def evaluate_rule(node, data):
    if node.node_type == "operand":
        if node.value.isnumeric():
            return int(node.value)
        elif node.value.startswith("'"):
            return node.value.strip("'")
        else:
            return data.get(node.value)
    
    left_val = evaluate_rule(node.left, data)
    right_val = evaluate_rule(node.right, data)
    return apply_op(left_val, right_val, node.value)

def validate_rule_string(rule_string):
    try:
        postfix_expr = convert_to_postfix(rule_string)
        if not postfix_expr:
            raise ValueError("Invalid rule string")
    except Exception as e:
        raise ValueError(f"Error in rule string: {str(e)}")

def validate_attributes(attributes, data):
    for attr in attributes:
        if attr not in data:
            raise ValueError(f"Attribute {attr} is missing from the data")

# --- Flask API ---
from flask import Flask, request, jsonify

app = Flask(__name__)

# Store rules in memory (in practice, this would be stored in a database)
rules = {}

@app.route('/create_rule', methods=['POST'])
def create_rule_api():
    rule_string = request.json.get('rule_string')
    try:
        rule_ast = create_rule(rule_string)
        rule_id = len(rules) + 1
        rules[rule_id] = rule_ast
        return jsonify({"rule_id": rule_id, "message": "Rule created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/combine_rules', methods=['POST'])
def combine_rules_api():
    rule_ids = request.json.get('rule_ids')
    try:
        selected_rules = [rules[rule_id] for rule_id in rule_ids]
        combined_ast = combine_rules(selected_rules)
        rule_id = len(rules) + 1
        rules[rule_id] = combined_ast
        return jsonify({"rule_id": rule_id, "message": "Rules combined successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule_api():
    rule_id = request.json.get('rule_id')
    data = request.json.get('data')
    try:
        rule_ast = rules.get(rule_id)
        if not rule_ast:
            raise ValueError("Invalid rule_id")
        result = evaluate_rule(rule_ast, data)
        return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

# --- Sample Data ---
data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
# This will need to be done via API calls in practice, but here's a simple test
rule1 = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
rule2 = "((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)"

# Create individual rules
ast1 = create_rule(rule1)
ast2 = create_rule(rule2)

# Combine the two ASTs
combined_ast = combine_rules([ast1, ast2])

# Evaluate the combined rule with the sample data
result = evaluate_rule(combined_ast, data)
print(result)  # True or False
{
    "rule_string": "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
}
