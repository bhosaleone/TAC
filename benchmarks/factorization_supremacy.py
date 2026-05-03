import numpy as np
import time
import matplotlib.pyplot as plt
from core.tac_coprocessor import TACCoprocessor

class FactorizationManifold:
    def __init__(self, n, s0):
        self.n = n
        self.state = s0
        
    def get_gradient(self, s):
        p, q = s
        # Log-space: F[s] = (log(p) + log(q) - log(n))^2
        # dF/dp = 2*(log(p) + log(q) - log(n)) * (1/p)
        # dF/dq = 2*(log(p) + log(q) - log(n)) * (1/q)
        
        diff = np.log(max(p, 1.1)) + np.log(max(q, 1.1)) - np.log(self.n)
        grad_p = 2.0 * diff / p
        grad_q = 2.0 * diff / q
        
        return np.array([grad_p, grad_q])

class FactorizationSupremacy:
    """
    Simulates Prime Factorization as a Thermodynamic Relaxation problem.
    Target: Factor n = p * q.
    """
    def __init__(self, p_true, q_true):
        self.n = p_true * q_true
        self.p_true = p_true
        self.q_true = q_true
        self.tac = TACCoprocessor(kappa=0.5, temperature=0.0)
        self.tac.equilibrium_threshold = 1e-6
        
    def run_test(self):
        # Initial guess (square root area)
        s0 = np.array([np.sqrt(self.n) * 0.8, np.sqrt(self.n) * 1.2])
        
        manifold = FactorizationManifold(self.n, s0)
        
        print(f"--- Factoring n = {self.n} ({self.p_true} x {self.q_true}) ---")
        
        start_t = time.perf_counter()
        s_relaxed, steps = self.tac.tac_offload(manifold)
        t_tac = (time.perf_counter() - start_t) * 1000
        
        p_res, q_res = s_relaxed
        print(f"Result: p={p_res:.2f}, q={q_res:.2f} (Product: {p_res*q_res:.2f})")
        print(f"Steps: {steps}, Time: {t_tac:.2f}ms")
        
        return steps

if __name__ == "__main__":
    # Test with a medium semiprime
    p, q = 104729, 1299709 # Two primes
    bench = FactorizationSupremacy(p, q)
    bench.run_test()
