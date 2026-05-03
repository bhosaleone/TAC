import numpy as np
import time
from core.tac_coprocessor import TACCoprocessor

class SATManifold:
    def __init__(self, clauses, num_vars, s0):
        """
        clauses: List of tuples. Each tuple is (var_index, sign), e.g., (3, 1) is x3, (3, -1) is not x3.
        """
        self.clauses = clauses
        self.num_vars = num_vars
        self.state = s0
        
    def get_gradient(self, s):
        # F[s] = sum_c (Product_l in c (1 - val(l)))^2
        # where val(l) = s_i if sign=1, else (1 - s_i)
        
        grad = np.zeros(self.num_vars)
        
        for clause in self.clauses:
            # Calculate (1 - val(l)) for each literal in clause
            l_terms = []
            for var_idx, sign in clause:
                val = s[var_idx] if sign == 1 else (1.0 - s[var_idx])
                l_terms.append(1.0 - val)
            
            clause_prod = np.prod(l_terms)
            clause_cost_grad = 2.0 * clause_prod
            
            for i, (var_idx, sign) in enumerate(clause):
                # d(prod)/ds_var = prod / l_term[i] * d(l_term)/ds_var
                # l_term = 1 - val
                # if sign=1, val=s, l_term=1-s, d(l_term)/ds=-1
                # if sign=-1, val=1-s, l_term=s, d(l_term)/ds=1
                
                other_terms_prod = np.prod(l_terms[:i] + l_terms[i+1:])
                d_l_ds = -1.0 if sign == 1 else 1.0
                grad[var_idx] += clause_cost_grad * other_terms_prod * d_l_ds
        
        # Soft-spin penalty
        penalty = 2.0 * s * (s - 1.0) * (2.0 * s - 1.0)
        return grad / len(self.clauses) + 0.1 * penalty

class SATChallenge:
    """
    Knuth Challenge #2: Hard Satisfiability (SAT) via TAC.
    """
    def __init__(self, num_vars=50, num_clauses=150):
        self.num_vars = num_vars
        self.num_clauses = num_clauses
        self.tac = TACCoprocessor(kappa=0.01, temperature=0.01)
        self.tac.equilibrium_threshold = 0.05
        
    def generate_random_3sat(self):
        self.clauses = []
        for _ in range(self.num_clauses):
            vars = np.random.choice(range(self.num_vars), 3, replace=False)
            signs = np.random.choice([1, -1], 3)
            self.clauses.append(list(zip(vars, signs)))
            
    def solve(self):
        self.generate_random_3sat()
        s0 = np.random.uniform(0, 1, self.num_vars)
        
        manifold = SATManifold(self.clauses, self.num_vars, s0)
        
        print(f"--- Knuth Challenge: Hard 3-SAT (Vars={self.num_vars}, Clauses={self.num_clauses}) ---")
        
        start_t = time.perf_counter()
        s_relaxed, steps = self.tac.tac_offload(manifold)
        t_tac = (time.perf_counter() - start_t) * 1000
        
        # Verify
        final_s = (s_relaxed > 0.5).astype(int)
        satisfied = 0
        for clause in self.clauses:
            is_sat = False
            for var_idx, sign in clause:
                val = final_s[var_idx]
                if (sign == 1 and val == 1) or (sign == -1 and val == 0):
                    is_sat = True
                    break
            if is_sat: satisfied += 1
            
        print(f"Result: {satisfied}/{self.num_clauses} clauses satisfied.")
        print(f"Steps: {steps}, Time: {t_tac:.2f}ms")
        return steps

if __name__ == "__main__":
    challenge = SATChallenge(num_vars=100, num_clauses=430) # Near the phase transition alpha=4.3
    challenge.solve()
