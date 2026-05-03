import numpy as np
import time
from core.tac_coprocessor import TACCoprocessor

class HamiltonianManifold:
    def __init__(self, adj_matrix, s0):
        """
        adj_matrix: N x N adjacency matrix.
        state: N x N matrix flattened (position, node).
        """
        self.adj = adj_matrix
        self.N = adj_matrix.shape[0]
        self.state = s0
        
    def get_gradient(self, s_flat):
        s = s_flat.reshape((self.N, self.N))
        grad = np.zeros((self.N, self.N))
        
        # 1. Each position has exactly one node: sum_v x_iv = 1
        pos_coverage = np.sum(s, axis=1) - 1.0
        grad += 2.0 * np.outer(pos_coverage, np.ones(self.N))
        
        # 2. Each node is at exactly one position: sum_i x_iv = 1
        node_coverage = np.sum(s, axis=0) - 1.0
        grad += 2.0 * np.outer(np.ones(self.N), node_coverage)
        
        # 3. Adjacency constraint: if x_iv=1 and x_{i+1,u}=1, then adj[v,u] must be 1
        # Penalty if adj[v,u] == 0: sum_i sum_v,u (1 - adj[v,u]) * x_iv * x_{i+1,u}
        for i in range(self.N - 1):
            for v in range(self.N):
                for u in range(self.N):
                    if self.adj[v, u] == 0:
                        # Gradient contribution to x_iv: (1-0) * x_{i+1,u}
                        grad[i, v] += s[i+1, u]
                        # Gradient contribution to x_{i+1,u}: (1-0) * x_iv
                        grad[i+1, u] += s[i, v]
                        
        # Soft-spin penalty
        penalty = 2.0 * s * (s - 1.0) * (2.0 * s - 1.0)
        
        return (grad.flatten() / self.N) + 0.1 * penalty.flatten()

class HamiltonianChallenge:
    """
    Knuth Challenge #3: Hamiltonian Path via TAC.
    """
    def __init__(self, num_nodes=20):
        self.N = num_nodes
        self.tac = TACCoprocessor(kappa=0.01, temperature=0.01)
        self.tac.equilibrium_threshold = 0.1
        
    def generate_random_graph(self):
        # Generate a random graph with a known Hamiltonian path for testing
        self.adj = np.zeros((self.N, self.N))
        path = np.random.permutation(self.N)
        for i in range(self.N - 1):
            self.adj[path[i], path[i+1]] = 1
            self.adj[path[i+1], path[i]] = 1
            
        # Add some random edges
        extra_edges = np.random.choice([0, 1], (self.N, self.N), p=[0.8, 0.2])
        self.adj = np.maximum(self.adj, extra_edges)
        np.fill_diagonal(self.adj, 0)
        
    def solve(self):
        self.generate_random_graph()
        s0 = np.random.uniform(0, 1, self.N * self.N)
        
        manifold = HamiltonianManifold(self.adj, s0)
        
        print(f"--- Knuth Challenge: Hamiltonian Path (Nodes={self.N}) ---")
        
        start_t = time.perf_counter()
        s_relaxed, steps = self.tac.tac_offload(manifold)
        t_tac = (time.perf_counter() - start_t) * 1000
        
        # Verify
        path_matrix = s_relaxed.reshape((self.N, self.N))
        final_path = np.argmax(path_matrix, axis=1)
        
        valid_edges = 0
        for i in range(self.N - 1):
            if self.adj[final_path[i], final_path[i+1]] == 1:
                valid_edges += 1
                
        print(f"Result: {valid_edges}/{self.N-1} valid edges in path.")
        print(f"Steps: {steps}, Time: {t_tac:.2f}ms")
        return steps

if __name__ == "__main__":
    challenge = HamiltonianChallenge(num_nodes=30)
    challenge.solve()
