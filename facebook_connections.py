import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import random

class FacebookGraph:
    def __init__(self):
        self.graph = nx.Graph()
        self.prob_graph = {}  # Additional graph to handle probabilistic connections
    
    def add_connection(self, user1, user2):
        """Add a deterministic connection (friendship) between two users."""
        self.graph.add_edge(user1, user2)
    
    def add_probabilistic_connection(self, user1, user2, probability):
        """Add a probabilistic connection between two users with a specified probability."""
        if user1 not in self.prob_graph:
            self.prob_graph[user1] = {}
        if user2 not in self.prob_graph:
            self.prob_graph[user2] = {}
        self.prob_graph[user1][user2] = probability
        self.prob_graph[user2][user1] = probability  # Assuming undirected graph

    def get_mutual_friends(self, user1, user2):
        """Get mutual friends between two users."""
        if user1 not in self.graph or user2 not in self.graph:
            raise ValueError("One or both users do not exist in the graph")
        return set(self.graph.neighbors(user1)) & set(self.graph.neighbors(user2))
    
    def find_connection_path(self, start, end, max_depth=3):
        """Find a path between two users within a certain depth."""
        if start not in self.graph or end not in self.graph:
            raise ValueError("One or both users do not exist in the graph")
        
        queue = deque([(start, [start])])
        visited = set([start])
        
        while queue:
            (node, path) = queue.popleft()
            
            if len(path) > max_depth:
                return None
            
            for neighbor in self.graph.neighbors(node):
                if neighbor == end:
                    return path + [end]
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None

    def get_friend_count(self, user):
        """Get the number of friends a user has."""
        if user not in self.graph:
            raise ValueError("User does not exist in the graph")
        return self.graph.degree(user)

    def get_friends_of_friends(self, user):
        """Get friends of friends for a user."""
        if user not in self.graph:
            raise ValueError("User does not exist in the graph")
        friends = set(self.graph.neighbors(user))
        friends_of_friends = set()
        for friend in friends:
            friends_of_friends.update(self.graph.neighbors(friend))
        friends_of_friends.discard(user)
        return friends_of_friends - friends

    def get_probability(self, user1, user2):
        """Return the probability of a probabilistic edge between two users."""
        return self.prob_graph.get(user1, {}).get(user2, 0)
    
    def are_connected_probabilistically(self, user1, user2):
        """Simulate if two users are connected based on their edge probability."""
        probability = self.get_probability(user1, user2)
        return random.random() < probability

    def visualize_graph(self, highlight_path=None):
        """Visualize the graph and optionally highlight a path."""
        pos = nx.spring_layout(self.graph, k=0.5, iterations=50)
        plt.figure(figsize=(12, 8))
        
        # Draw all nodes and edges
        nx.draw_networkx_nodes(self.graph, pos, node_color='lightblue', node_size=500)
        nx.draw_networkx_edges(self.graph, pos, edge_color='gray', alpha=0.5)
        nx.draw_networkx_labels(self.graph, pos, font_size=10, font_weight='bold')
        
        if highlight_path:
            path_edges = list(zip(highlight_path, highlight_path[1:]))
            nx.draw_networkx_nodes(self.graph, pos, nodelist=highlight_path, node_color='lightgreen', node_size=600)
            nx.draw_networkx_edges(self.graph, pos, edgelist=path_edges, edge_color='r', width=2)
        
        plt.title("Facebook-inspired Social Graph with Probabilistic Connections")
        plt.axis('off')
        plt.tight_layout()
        plt.show()

# Create a FacebookGraph instance
fb_graph = FacebookGraph()

# Add deterministic connections
connections = [
    ("Alice", "Bob"), ("Alice", "Charlie"), ("Alice", "David"),
    ("Bob", "Charlie"), ("Bob", "Eve"), ("Bob", "Frank"),
    ("Charlie", "David"), ("Charlie", "Eve"),
    ("David", "Frank"), ("Eve", "George"),
    ("Frank", "George"), ("George", "Harry")
]

for user1, user2 in connections:
    fb_graph.add_connection(user1, user2)

# Add probabilistic connections
fb_graph.add_probabilistic_connection('UserA', 'UserB', 0.7)
fb_graph.add_probabilistic_connection('UserA', 'UserC', 0.4)
fb_graph.add_probabilistic_connection('UserB', 'UserC', 0.6)

# Test Case 1: Mutual Friends
print("Test Case 1: Mutual Friends")
try:
    mutual_friends = fb_graph.get_mutual_friends("Alice", "Bob")
    print("Mutual friends of Alice and Bob:", mutual_friends)
except ValueError as e:
    print(f"Error: {e}")

# Test Case 2: Connection Path
print("\nTest Case 2: Connection Path")
try:
    path = fb_graph.find_connection_path("Alice", "George")
    print("Connection path from Alice to George:", path)
    fb_graph.visualize_graph(highlight_path=path)
except ValueError as e:
    print(f"Error: {e}")

# Test Case 3: No Connection Path
print("\nTest Case 3: No Connection Path")
try:
    path = fb_graph.find_connection_path("Alice", "Harry", max_depth=2)
    print("Connection path from Alice to Harry (max depth 2):", path)
except ValueError as e:
    print(f"Error: {e}")

# Test Case 4: Friend Count
print("\nTest Case 4: Friend Count")
try:
    print("Bob's friend count:", fb_graph.get_friend_count("Bob"))
    print("George's friend count:", fb_graph.get_friend_count("George"))
except ValueError as e:
    print(f"Error: {e}")

# Test Case 5: Friends of Friends
print("\nTest Case 5: Friends of Friends")
try:
    fof_alice = fb_graph.get_friends_of_friends("Alice")
    print("Alice's friends of friends:", fof_alice)
except ValueError as e:
    print(f"Error: {e}")

# Test Case 6: Mutual Friends (No mutual friends)
print("\nTest Case 6: Mutual Friends (No mutual friends)")
try:
    mutual_friends = fb_graph.get_mutual_friends("Alice", "George")
    print("Mutual friends of Alice and George:", mutual_friends)
except ValueError as e:
    print(f"Error: {e}")

# Test Case 7: Connection Path (Longer path)
print("\nTest Case 7: Connection Path (Longer path)")
try:
    path = fb_graph.find_connection_path("Alice", "Harry")
    print("Connection path from Alice to Harry:", path)
    fb_graph.visualize_graph(highlight_path=path)
except ValueError as e:
    print(f"Error: {e}")

# Test Case 8: Probabilistic Connections
print("\nTest Case 8: Probabilistic Connections")
print(f"Probability of connection between UserA and UserB: {fb_graph.get_probability('UserA', 'UserB')}")
print(f"Probability of connection between UserA and UserC: {fb_graph.get_probability('UserA', 'UserC')}")
print(f"Are UserA and UserB connected? {'Yes' if fb_graph.are_connected_probabilistically('UserA', 'UserB') else 'No'}")
print(f"Are UserA and UserC connected? {'Yes' if fb_graph.are_connected_probabilistically('UserA', 'UserC') else 'No'}")

# Visualize the entire graph
fb_graph.visualize_graph()