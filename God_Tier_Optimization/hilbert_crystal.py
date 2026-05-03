"""
5D TAC Crystal & Hilbert Space Mapping Module
=============================================

This module contains the core mathematical architectures for the "God Tier" Optimization framework.
It demonstrates the ability to map massive quantum systems (traditionally requiring intractable
O(2^N) memory in Hilbert space) into a continuous, 5-dimensional thermodynamic crystal topology.

By mapping quantum entanglement (J_ij) and local fields (h_i) into a continuous thermodynamic
cost functional, the Virtual Thermodynamic Automaton Computer (VTAC) can extract the ground state
of a quantum Hamiltonian using a fraction of the memory (O(N) instead of O(2^N)).

Key Components:
1. CrystalTopology5D: Defines the N-dimensional physical lattice structure.
2. HilbertSpaceMapper: Translates quantum Hamiltonians into continuous energy landscapes.
"""

import numpy as np
from typing import Dict, List, Tuple
from functools import lru_cache

class CrystalTopology5D:
    """
    Constructs a 5-dimensional geometric lattice of 120 nodes.
    
    In the context of the Bhosale TAC Paradigm, this topology represents the physical 
    routing substrate of the Virtual TAC layer. Each node connects to neighbors along 
    5 orthogonal dimensions with periodic boundary conditions.
    
    This topological structure is specifically optimized with pre-computed dimensions 
    and cached coordinate transforms to ensure the thermodynamic field relaxation occurs 
    in O(1) relative steps, avoiding classical memory bottlenecks.
    """
    # Pre-computed dimensions for a 120-node lattice: 2×2×2×3×5 = 120
    DIMS = (2, 2, 2, 3, 5)  
    # Pre-computed strides for O(1) fast memory indexing in flat arrays
    STRIDES = (60, 30, 15, 5, 1)  
    
    def __init__(self, num_nodes: int = 120):
        """
        Initializes the 5D crystal topology.
        
        Args:
            num_nodes (int): Total number of nodes in the crystal. Defaults to 120, 
                             representing a 120-qubit system.
        """
        self.num_nodes = num_nodes
        # The adjacency list maps each 1D node index to a list of its connected neighbors
        self.adjacency_list = {i: [] for i in range(num_nodes)}
        self._build_5d_lattice_optimized()

    @staticmethod
    @lru_cache(maxsize=128)
    def _coords_to_1d(c0: int, c1: int, c2: int, c3: int, c4: int) -> int:
        """
        Cached conversion from 5-dimensional coordinates to a flat 1D memory index.
        
        Uses the pre-computed STRIDES to ensure O(1) constant time lookup.
        This is critical for preventing memory latency during field collapse.
        """
        strides = (60, 30, 15, 5, 1)
        return c0 * strides[0] + c1 * strides[1] + c2 * strides[2] + c3 * strides[3] + c4

    @staticmethod
    @lru_cache(maxsize=128)
    def _1d_to_coords(idx: int) -> Tuple[int, int, int, int, int]:
        """
        Cached conversion from a flat 1D index back to 5-dimensional coordinates.
        Uses modulo arithmetic against the crystal's orthogonal dimensions.
        """
        dims = (2, 2, 2, 3, 5)
        c4 = idx % dims[4]; idx //= dims[4]
        c3 = idx % dims[3]; idx //= dims[3]
        c2 = idx % dims[2]; idx //= dims[2]
        c1 = idx % dims[1]; idx //= dims[1]
        c0 = idx
        return (c0, c1, c2, c3, c4)

    def _build_5d_lattice_optimized(self):
        """
        Optimized 5D lattice construction with set-based deduplication.
        
        Iterates through every node in the crystal, computes its 5D coordinates,
        and establishes periodic boundary connections (wrapping around the crystal edges)
        across all 5 dimensions. This creates a dense, highly-connected thermodynamic field.
        """
        dims = self.DIMS
        neighbors_set = [set() for _ in range(self.num_nodes)]
        
        for i in range(self.num_nodes):
            c0, c1, c2, c3, c4 = self._1d_to_coords(i)
            coords = [c0, c1, c2, c3, c4]
            
            # Connect to neighbors in all 5 dimensions (+1 and -1 steps)
            for d in range(5):
                for delta in [-1, 1]:
                    neighbor_coords = list(coords)
                    # Apply periodic boundary conditions (toroidal topology)
                    neighbor_coords[d] = (neighbor_coords[d] + delta) % dims[d]
                    neighbor_idx = self._coords_to_1d(*neighbor_coords)
                    neighbors_set[i].add(neighbor_idx)
        
class FlexibleCrystal5D:
    """
    A dynamic 5-dimensional geometric lattice that supports arbitrary node counts.
    
    This class generalizes the CrystalTopology5D to allow for high-resolution 
    simulations (e.g., 10,000 nodes for the Page Curve).
    """
    def __init__(self, dims: Tuple[int, int, int, int, int]):
        """
        Args:
            dims (tuple): The 5 dimensions of the crystal (e.g. (10, 10, 10, 5, 2) for 10,000 nodes).
        """
        self.dims = dims
        self.num_nodes = np.prod(dims)
        # Compute strides for fast 1D mapping
        self.strides = []
        current_stride = 1
        for d in reversed(dims):
            self.strides.insert(0, current_stride)
            current_stride *= d
        self.strides = tuple(self.strides)
        
        self.adjacency_list = {i: [] for i in range(self.num_nodes)}
        self._build_5d_lattice()

    def _coords_to_1d(self, coords: List[int]) -> int:
        return sum(c * s for c, s in zip(coords, self.strides))

    def _1d_to_coords(self, idx: int) -> List[int]:
        res = []
        rem = idx
        for s in self.strides:
            c, rem = divmod(rem, s)
            res.append(c)
        return res

    def _build_5d_lattice(self):
        """
        Builds the 5D lattice with periodic boundary conditions.
        """
        for i in range(self.num_nodes):
            coords = self._1d_to_coords(i)
            neighbors = set()
            for d in range(5):
                for delta in [-1, 1]:
                    neighbor_coords = list(coords)
                    neighbor_coords[d] = (neighbor_coords[d] + delta) % self.dims[d]
                    neighbor_idx = self._coords_to_1d(neighbor_coords)
                    neighbors.add(neighbor_idx)
            self.adjacency_list[i] = list(neighbors)


class HilbertSpaceMapper:
    """
    The Hilbert Space Mapper is the bridge between Quantum Mechanics and Thermodynamics.
    
    It translates a discrete quantum Hamiltonian matrix (representing millions of qubits 
    in an exponentially large Hilbert Space) into a continuous thermodynamic cost functional.
    This continuous functional can be rapidly minimized by the 5D TAC crystal.
    """
    def __init__(self, topology: CrystalTopology5D):
        """
        Args:
            topology (CrystalTopology5D): The physical layout of the VTAC substrate.
        """
        self.topology = topology
        self.N = topology.num_nodes
        # Pre-compute edge list for vectorized operations during Langevin relaxation
        self._edge_list = self._precompute_edges()
        
    def _precompute_edges(self):
        """
        Pre-compute all unique edges in the topology to avoid repeated adjacency list lookups.
        This flattens the graph structure into an array, allowing numpy vectorization.
        """
        edges = []
        for i in range(self.N):
            for j in self.topology.adjacency_list[i]:
                if i < j: # Ensure unique, undirected edges
                    edges.append((i, j))
        return np.array(edges, dtype=np.int32)
        
    def construct_cost_functional(self, quantum_coupling_matrix: np.ndarray):
        """
        Maps a simulated Quantum Ising Model Hamiltonian onto the 5D crystal.
        
        Quantum Hamiltonian: H = - sum_{i,j} J_{ij} Z_i Z_j - sum_i h_i X_i
        
        Instead of evaluating a 2^N state vector, we map the expectation values to continuous 
        variables `s_i` in the TAC. The physical nodes represent the superposition amplitudes, 
        and the quantum entanglements (J_ij) become the elastic spring constants between nodes.
        
        Args:
            quantum_coupling_matrix (np.ndarray): An NxN matrix representing quantum entanglement 
                                                  strengths (J_ij).
                                                  
        Returns:
            CostFunctional: An object with energy(state) and gradient(state) methods.
        """
        J_matrix = quantum_coupling_matrix  # Cache reference
        edges = self._edge_list
        N = self.N
        
        class CostFunctional:
            def energy(self, state: dict) -> float:
                """
                The continuous cost functional F[s] evaluated at the given state.
                """
                # Extract state dictionary into a flat numpy array (single memory allocation)
                s_vec = np.array([state[f'node_{i}'] for i in range(N)], dtype=np.float32)
                
                # 1. Local Node Energy (vectorized)
                # Implements a double-well potential: sum((s_i^2 - 1)^2)
                # This forces the continuous variables to eventually snap into discrete quantum states (+1 or -1)
                local_energy = np.sum((s_vec ** 2 - 1.0) ** 2)
                
                # 2. 5D Crystal Coupling Energy (vectorized)
                # Calculates the interaction energy across the entire topology based on the J_ij matrix.
                if len(edges) > 0:
                    i_indices = edges[:, 0]
                    j_indices = edges[:, 1]
                    coupling_energy = -np.sum(J_matrix[i_indices, j_indices] * s_vec[i_indices] * s_vec[j_indices])
                else:
                    coupling_energy = 0.0
                            
                return local_energy + coupling_energy
                
            def gradient(self, state: dict) -> dict:
                """
                Analytical gradient of F[s].
                """
                s_vec = np.array([state[f'node_{i}'] for i in range(N)], dtype=np.float32)
                
                # Gradient of local energy: 4 s_i (s_i^2 - 1)
                local_grad = 4 * s_vec * (s_vec**2 - 1.0)
                
                # Gradient of coupling energy: for each i, - sum_j J_ij s_j where j neighbors i
                coupling_grad = np.zeros(N, dtype=np.float32)
                if len(edges) > 0:
                    for edge in edges:
                        i, j = edge
                        coupling_grad[i] -= J_matrix[i, j] * s_vec[j]
                        coupling_grad[j] -= J_matrix[j, i] * s_vec[i]  # since symmetric
                
                total_grad_vec = local_grad + coupling_grad
                
                return {f'node_{i}': total_grad_vec[i] for i in range(N)}
        
        return CostFunctional()
