import numpy as np
import time
from core.tac_coprocessor import TACCoprocessor

class ExactCoverManifold:
    def __init__(self, A, s0):
        """
        A: Incidence matrix (sets x elements). A_ij = 1 if set i contains element j.
        """
        self.A = A
        self.state = s0
        
    def get_gradient(self, s):
        # Normalize by num_elements to keep gradient scale stable
        num_elements = self.A.shape[1]
        
        coverage = np.dot(s, self.A) 
        diff = coverage - 1.0
        
        # Gradient from coverage constraint (normalized)
        grad = 2.0 * np.dot(self.A, diff) / num_elements
        
        # Soft-spin penalty: forcing toward 0 or 1
        penalty = 2.0 * s * (s - 1.0) * (2.0 * s - 1.0)
        
        return grad + 0.1 * penalty

class ExactCoverChallenge:
    """
    Knuth Challenge #1: Exact Cover (X3C) via Thermodynamic Relaxation.
    """
    def __init__(self, num_sets=100, num_elements=50):
        self.num_sets = num_sets
        self.num_elements = num_elements
        self.tac = TACCoprocessor(kappa=0.01, temperature=0.01)
        self.tac.equilibrium_threshold = 0.1
        
    def generate_hard_instance(self):
        # Random sparse incidence matrix
        self.A = np.random.choice([0, 1], (self.num_sets, self.num_elements), p=[0.9, 0.1])
        
    def solve(self):
        self.generate_hard_instance()
        s0 = np.random.uniform(0, 1, self.num_sets)
        
        manifold = ExactCoverManifold(self.A, s0)
        
        print(f"--- Knuth Challenge: Exact Cover (Sets={self.num_sets}, Elements={self.num_elements}) ---")
        
        start_t = time.perf_counter()
        s_relaxed, steps = self.tac.tac_offload(manifold)
        t_tac = (time.perf_counter() - start_t) * 1000
        
        # Final coverage check
        final_s = (s_relaxed > 0.5).astype(int)
        final_coverage = np.dot(final_s, self.A)
        uncovered = np.sum(final_coverage == 0)
        overcovered = np.sum(final_coverage > 1)
        
        print(f"Result: {uncovered} uncovered, {overcovered} overcovered.")
        print(f"Steps: {steps}, Time: {t_tac:.2f}ms")
        
        return steps

if __name__ == "__main__":
    challenge = ExactCoverChallenge(num_sets=500, num_elements=200)
    challenge.solve()
