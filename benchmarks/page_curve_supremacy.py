import numpy as np
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.hawking_engine import HawkingEvaporator

def run_page_curve_simulation():
    print("Initializing 10,000-Node Page Curve Simulation...")
    engine = HawkingEvaporator(N_qubits=10000)
    
    data = []
    time = 0.0
    
    # We want to capture the full evaporation until mass reaches 0
    print("Evaporating Black Hole (The Unitary Leak)...")
    while engine.mass > 0.5:
        success = engine.evaporate_step(dt=2000.0) # Much larger dt
        if not success:
            break
            
        time += 5.0
        data.append({
            'time': time,
            'mass': engine.mass,
            'entropy': engine.radiation_entropy,
            'qubits_emitted': engine.radiation_qubits
        })
        
        if len(data) % 100 == 0:
            print(f"Time: {time:.1f} | Mass: {engine.mass:.2f} | Entropy: {engine.radiation_entropy}")
            
    df = pd.DataFrame(data)
    df.to_csv("page_curve_data.csv", index=False)
    print("Simulation Complete. Dataset saved to page_curve_data.csv")

if __name__ == "__main__":
    run_page_curve_simulation()
