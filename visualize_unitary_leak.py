import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.hawking_engine import HawkingEvaporator

def run_visualization():
    print("Initializing 10,000-Qubit Page Curve Visualization...")
    engine = HawkingEvaporator(N_qubits=10000)
    
    import pandas as pd
    history = pd.read_csv("page_curve_data.csv").to_dict('records')
    print(f"Data loaded: {len(history)} frames.")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
    fig.suptitle("God-Tier Optimization: Resolving the Information Paradox (N=10,000)", fontsize=16)
    
    # Left Plot: The Interior Information Cloud (Projected)
    ax1.set_title("Black Hole Interior (10,000 Qubit Cloud)")
    # We will only plot 1000 points to represent the 10,000 nodes for rendering speed
    N_VIS = 1000
    theta = np.random.uniform(0, 2*np.pi, N_VIS)
    phi = np.random.uniform(0, np.pi, N_VIS)
    r = np.random.uniform(0, 1, N_VIS)**(1/3)
    
    x = r * np.sin(phi) * np.cos(theta)
    y = r * np.sin(phi) * np.sin(theta)
    z = r * np.cos(phi)
    
    scatter = ax1.scatter(x, y, s=2, c='cyan', alpha=0.8)
    ax1.set_xlim(-1.2, 1.2); ax1.set_ylim(-1.2, 1.2); ax1.set_axis_off()
    
    # Right Plot: The Page Curve
    ax2.set_title("Entanglement Entropy (The Page Curve)")
    ax2.set_xlabel("Evaporation Progress")
    ax2.set_ylabel("Radiation Entropy $S_{ent}$")
    ax2.set_xlim(0, len(history))
    ax2.set_ylim(0, 5500)
    line, = ax2.plot([], [], 'r-', lw=2, label="Information Recovery")
    ax2.axhline(y=5000, color='gray', linestyle='--', label="Page Point (N/2)")
    ax2.legend()
    
    times = []
    entropies = []
    
    def update(frame):
        h = history[frame]
        # Fade out visual nodes based on proportion of qubits emitted
        proportion_emitted = h['qubits_emitted'] / 10000.0
        num_to_hide = int(N_VIS * proportion_emitted)
        
        alphas = np.ones(N_VIS) * 0.8
        alphas[:num_to_hide] = 0.0 # evaporated
        
        scatter.set_alpha(alphas)
        
        # Update Page Curve
        times.append(frame)
        entropies.append(h['entropy'])
        line.set_data(times, entropies)
        
        return scatter, line

    anim = FuncAnimation(fig, update, frames=len(history), interval=30, blit=False)
    
    output_path = "unitary_leak_page_curve.mp4"
    print(f"Saving animation to {output_path}...")
    try:
        anim.save(output_path, writer='ffmpeg', fps=30, dpi=150)
        print("Save successful.")
    except Exception as e:
        print(f"Could not save mp4 using ffmpeg: {e}")
        print("Falling back to gif...")
        anim.save("unitary_leak_page_curve.gif", writer='pillow', fps=30)
        print("Gif saved.")

if __name__ == "__main__":
    run_visualization()
