import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from God_Tier_Optimization.hilbert_crystal import FlexibleCrystal5D, HilbertSpaceMapper
from core.tac_coprocessor import TACCoprocessor

class StabilityEngine:
    """
    Tests the TAC architecture's stability against topological perturbations.
    Introduces 'Wormholes' (non-local couplings) and UV noise.
    """
    def __init__(self, N_nodes=5000):
        self.N = N_nodes
        if N_nodes == 5000: dims = (10, 10, 10, 5, 1)
        elif N_nodes == 1000: dims = (10, 10, 10, 1, 1)
        elif N_nodes == 500: dims = (5, 5, 4, 5, 1)
        elif N_nodes == 100: dims = (5, 5, 2, 2, 1)
        else: dims = (N_nodes, 1, 1, 1, 1)
        
        self.topology = FlexibleCrystal5D(dims=dims)
        self.mapper = HilbertSpaceMapper(self.topology)
        self.coprocessor = TACCoprocessor(kappa=0.01, temperature=0.01)
        
    def inject_wormhole(self, node_a, node_b, strength=5.0):
        print(f"Injecting Wormhole Bridge: {node_a} <==> {node_b} | Strength: {strength}")
        return (node_a, node_b, strength)

    def test_structural_relaxation(self, perturbations):
        print(f"Running Stability Test for N={self.N}...")
        J_matrix = np.random.randn(self.N, self.N) * 0.01
        for a, b, s in perturbations:
            if a < self.N and b < self.N:
                J_matrix[a, b] = s
                J_matrix[b, a] = s
            
        cost_func = self.mapper.construct_cost_functional(J_matrix)
        state = {f'node_{i}': np.random.randn() * 0.1 for i in range(self.N)}
        
        steps = 0
        max_grad = 1.0
        while max_grad > self.coprocessor.equilibrium_threshold and steps < 500:
            grad = cost_func.gradient(state)
            max_grad = 0
            for i in range(self.N):
                g = grad[f'node_{i}']
                noise = np.random.randn() * np.sqrt(2 * self.coprocessor.kappa * self.coprocessor.temperature)
                state[f'node_{i}'] -= (self.coprocessor.kappa * g) + noise
                max_grad = max(max_grad, abs(g))
            steps += 1
            if steps % 100 == 0:
                print(f"Step {steps} | Max Gradient: {max_grad:.6f}")
                
        return steps, max_grad

if __name__ == "__main__":
    engine = StabilityEngine(N_nodes=5000)
    wormholes = [engine.inject_wormhole(0, 4999)]
    engine.test_structural_relaxation(wormholes)
