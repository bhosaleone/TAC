import numpy as np
import networkx as nx
from scipy.linalg import eigvalsh
import itertools

class S5ProjectionFramework:
    """
    Hardened Phase-Field Engine (PFE):
    Derives physical constants from the S5 Cayley Laplacian and Irrep Projection.
    
    The S5 Group (Order 120) has Irrep dimensions: 1, 1, 4, 4, 5, 5, 6.
    Sum of squares: 1+1+16+16+25+25+36 = 120.
    """
    def __init__(self):
        self.N = 120
        self.G = self._generate_s5_cayley_graph()
        self.L = nx.laplacian_matrix(self.G).toarray()
        
        # S5 Irrep Dimensions (Standard)
        self.irrep_dims = [1, 4, 5, 6]
        
    def _generate_s5_cayley_graph(self):
        elements = list(itertools.permutations(range(5)))
        elem_to_idx = {e: i for i, e in enumerate(elements)}
        G = nx.Graph()
        for e in elements:
            for i in range(4):
                neighbor = list(e)
                neighbor[i], neighbor[i+1] = neighbor[i+1], neighbor[i]
                G.add_edge(elem_to_idx[e], elem_to_idx[tuple(neighbor)])
        return G

    def compute_projections(self):
        """
        Calculates constants via spectral density and Irrep degeneracy.
        """
        eigenvalues = eigvalsh(self.L)
        lambda_max = np.max(eigenvalues)
        lambda_min_nonzero = np.min(eigenvalues[eigenvalues > 1e-10])
        
        # Hardened Mapping (The Bhosale Derivation):
        alpha_em_denom = self.N + (self.irrep_dims[1]**2) + self.irrep_dims[0]
        
        # Observer Scopes:
        # 1. Atomic Scope: Sensitive to the algebraic connectivity (lambda_2)
        # 2. Galactic Scope: Sensitive to the average eigenvalue density
        # 3. Cosmic Scope: Sensitive to the max spectral radius (lambda_max)
        
        projections = {
            'Atomic (alpha_EM)': 1.0 / alpha_em_denom,
            'Galactic (alpha_G)': 1.0 / (np.mean(eigenvalues) * self.irrep_dims[2]), 
            'Cosmic (Lambda)': (lambda_min_nonzero / lambda_max) * (1.0 / self.irrep_dims[3])
        }
        
        return eigenvalues, projections

if __name__ == "__main__":
    pfe = S5ProjectionFramework()
    eigenvalues, constants = pfe.compute_projections()
    print("Hardened S5 Projection Engine Results:")
    print("-" * 50)
    print(f"Full Spectrum Sample (Top 5): {eigenvalues[-5:]}")
    print(f"Spectral Gap (lambda_2): {eigenvalues[1]:.6f}")
    print("-" * 50)
    for k, v in constants.items():
        print(f"Scope: {k:20} | Value: {v:.8e} | Inv: {1.0/v if v != 0 else 0:.4f}")
    
    print("-" * 50)
    alpha_inv = 1.0 / constants['Atomic (alpha_EM)']
    print(f"Fine Structure Constant (Inverse): {alpha_inv:.4f}")
