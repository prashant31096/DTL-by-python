import pandas as pd
import math

class Node:
    def __init__(self, attribute=None, value=None, result=None):
        self.attribute = attribute
        self.value = value
        self.result = result
        self.children = {}
def calculate_entropy(df):
    classes = df['Play Tennis'].unique()
    entropy = 0
    total = len(df)
    for c in classes:
        p = len(df[df['Play Tennis'] == c]) / total
        entropy -= p * math.log2(p)
    return entropy

def calculate_information_gain(df, attribute):
    values = df[attribute].unique()
    gain = calculate_entropy(df)
    total = len(df)
    for v in values:
        subset = df[df[attribute] == v]
        gain -= (len(subset) / total) * calculate_entropy(subset)
    return gain

def get_majority_class(df):
    return df['Play Tennis'].mode()[0]

def build_tree(df, attributes):
    if len(df['Play Tennis'].unique()) == 1:
        return Node(result=df['Play Tennis'].iloc[0])

    if len(attributes) == 0:
        return Node(result=get_majority_class(df))

    max_gain = -1
    best_attr = None
    for attr in attributes:
        gain = calculate_information_gain(df, attr)
        if gain > max_gain:
            max_gain = gain
            best_attr = attr

    root = Node(attribute=best_attr)
    for value in df[best_attr].unique():
        subset = df[df[best_attr] == value]
        if len(subset) == 0:
            root.children[value] = Node(result=get_majority_class(df))
        else:
            root.children[value] = build_tree(subset.drop(columns=[best_attr]), [a for a in attributes if a != best_attr])
    return root

def print_tree(node, depth=0):
    if node.result is not None:
        print('  ' * depth, "Result:", node.result)
        return
    print('  ' * depth, "Attribute:", node.attribute)
    for value, child in node.children.items():
        print('  ' * (depth + 1), "Value:", value)
        print_tree(child, depth + 2)

data = [
    ["D1", "Sunny", "Hot", "High", "Weak", "No"],
    ["D2", "Sunny", "Hot", "High", "Strong", "No"],
    ["D3", "Overcast", "Hot", "High", "Weak", "Yes"],
    ["D4", "Rain", "Mild", "High", "Weak", "Yes"],
    ["D5", "Rain", "Cool", "Normal", "Weak", "Yes"],
    ["D6", "Rain", "Cool", "Normal", "Strong", "No"],
    ["D7", "Overcast", "Cool", "Normal", "Strong", "Yes"],
    ["D8", "Sunny", "Mild", "High", "Weak", "No"],
    ["D9", "Sunny", "Cool", "Normal", "Weak", "Yes"],
    ["D10", "Rain", "Mild", "Normal", "Weak", "Yes"],
    ["D11", "Sunny", "Mild", "Normal", "Strong", "Yes"],
    ["D12", "Overcast", "Mild", "High", "Strong", "Yes"],
    ["D13", "Overcast", "Hot", "Normal", "Weak", "Yes"],
    ["D14", "Rain", "Mild", "High", "Strong", "No"]
]

columns = ["Day", "Outlook", "Temperature", "Humidity", "Wind", "Play Tennis"]
data = pd.DataFrame(data, columns=columns)

root = build_tree(data, ['Outlook', 'Temperature', 'Humidity', 'Wind'])
print_tree(root)
