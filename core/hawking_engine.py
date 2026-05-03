import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from God_Tier_Optimization.hilbert_crystal import FlexibleCrystal5D, HilbertSpaceMapper
from core.black_hole_manifold import BlackHoleManifold
from core.tac_coprocessor import TACCoprocessor

class HawkingEvaporator:
    """
    Simulates the unitary evaporation of a black hole and tracks information transfer.
    Upgraded with True Von Neumann Entanglement Tracking.
    """
    def __init__(self, N_qubits=10000):
        self.N = N_qubits
        self.topology = FlexibleCrystal5D(dims=(10, 10, 10, 5, 2))
        self.mapper = HilbertSpaceMapper(self.topology)
        
        # Interior information state (amplitudes)
        raw_state = np.random.randn(self.N)
        self.amplitudes = raw_state / np.linalg.norm(raw_state)
        
        self.mass = 100.0
        self.radiation_qubits = 0
        self.S_int = 0.0
        self.S_rad = 0.0
        self.S_ent = 0.0 # Total Entanglement Entropy
        self.trace = np.sum(self.amplitudes**2)

    def _calculate_von_neumann(self, probs):
        """Calculates -sum(p log p) for a probability distribution."""
        probs = probs[probs > 1e-15] # Numerical stability
        return -np.sum(probs * np.log(probs))

    def check_unitarity(self):
        current_trace = np.sum(self.amplitudes**2)
        deviation = abs(1.0 - current_trace)
        return current_trace, deviation

    def evaporate_step(self, dt=1.0):
        if self.mass <= 0:
            return False
            
        dM = (1.0 / (self.mass**2)) * dt
        self.mass -= dM
        
        # Emission count
        qubits_to_emit = int(self.N * (dM / 100.0) * 1.5)
        for _ in range(qubits_to_emit):
            if self.radiation_qubits < self.N:
                self.radiation_qubits += 1
                
        # Calculate True Von Neumann Entropy
        # We split the probability distribution into Interior and Radiation
        p_dist = self.amplitudes**2
        p_int = p_dist[self.radiation_qubits:]
        p_rad = p_dist[:self.radiation_qubits]
        
        # Normalize sub-distributions for separate entropy check
        if len(p_int) > 0: self.S_int = self._calculate_von_neumann(p_int / np.sum(p_int))
        if len(p_rad) > 0: self.S_rad = self._calculate_von_neumann(p_rad / np.sum(p_rad))
        
        # The true entanglement entropy is bounded by the smaller subspace (Page Curve)
        # S_ent = min(log(dim_int), log(dim_rad)) in a maximally entangled state
        # Here we track the actual distribution entropy
        self.S_ent = min(self.S_int, self.S_rad)
        
        # Renormalize (TUA)
        self.amplitudes /= np.linalg.norm(self.amplitudes)
        self.trace = np.sum(self.amplitudes**2)
        
        return True

if __name__ == "__main__":
    engine = HawkingEvaporator(N_qubits=10000)
    print(f"Hawking Engine Initialized. N={engine.N} qubits.")
    while engine.evaporate_step():
        if int(engine.mass) % 20 == 0:
            print(f"M: {engine.mass:6.2f} | S_int: {engine.S_int:6.2f} | S_rad: {engine.S_rad:6.2f} | S_ent: {engine.S_ent:6.2f}")
    
    print(f"Evaporation Complete. Final S_ent: {engine.S_ent:.4f}")
