from node import Node
from connection import Connection
import random

class Brain:
    def __init__(self, inputs: int, clone: bool = False):
        self.connections = []
        self.nodes = []
        self.inputs = inputs
        self.net = []
        self.layers = 2
        
        if not clone:
            # input nodes
            for i in range(self.inputs):
                self.nodes.append(Node(i, 0)) # Nodes 0 thru 2
            # bias node
            self.nodes.append(Node(inputs, 0)) # Node 3
            # output node
            self.nodes.append(Node(inputs + 1, 1)) # Node 4

            for i in range(inputs+1):
                self.connections.append(Connection(self.nodes[i], self.nodes[inputs+1], random.uniform(-1, 1)))
    
    def connect_nodes(self) -> None:
        for i in range(len(self.nodes)):
            self.nodes[i].connections = []
        
        for i in range(len(self.connections)):
            self.connections[i].from_node.connections.append(self.connections[i])
    
    def generate_net(self):
        self.connect_nodes()
        self.net = []
        for j in range(self.layers):
            for i in range(len(self.nodes)):
                if self.nodes[i].layer == j:
                    self.net.append(self.nodes[i])
    
    def feed_forward(self, vision):
        for i in range(self.inputs):
            self.nodes[i].output_value  = vision[i]
        self.nodes[self.inputs].output_value = 1  # bias node

        for i in range(len(self.net)):
            self.net[i].activate()

        output_value = self.nodes[self.inputs + 1].output_value

        for i in range(len(self.nodes)):
            self.nodes[i].input_value = 0
        return output_value
    
    def clone(self):
        clone = Brain(self.inputs, True)

        for n in self.nodes:
            clone.nodes.append(n.clone())
        for c in self.connections:
            clone.connections.append(c.clone(clone.getNode(c.from_node.id), clone.getNode(c.to_node.id)))
        
        clone.layers = self.layers
        clone.connect_nodes()
        return clone

    def getNode(self, node_id: int) -> Node:
        for n in self.nodes:
            if n.id == node_id:
                return n
            
    def mutate(self) -> None:
        if random.uniform(0, 1) < 0.8:
            for i in range(len(self.connections)):
                self.connections[i].mutate_weight()