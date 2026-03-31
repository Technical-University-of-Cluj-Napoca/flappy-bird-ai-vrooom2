import math

class Node:
    def __init__(self, node_id: int, layer: int):
        self.id = node_id
        self.layer = layer
        self.input_value = 0
        self.output_value = 0
        self.connections = [] 
    
    def activate(self) -> None:
        def sigmoid(x):
            return 1 / (1 + math.exp(-x))
        if self.layer == 1:
            self.output_value = sigmoid(self.input_value)
        
        for i in range(len(self.connections)):
            self.connections[i].to_node.input_value += self.output_value * self.connections[i].weight
    
    def clone(self):
        clone = Node(self.id, self.layer)
        return clone