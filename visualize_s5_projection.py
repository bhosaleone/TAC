import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.s5_projection import S5ProjectionFramework
from core.stability_engine import StabilityEngine

def run_visualization():
    print("Initializing Phase III Ultimate Visualizer...")
    pfe = S5ProjectionFramework()
    engine = StabilityEngine(N_nodes=120)
    
    # 1. S5 Cayley Graph Layout
    print("Computing S5 Cayley Graph Layout...")
    pos_s5 = nx.spring_layout(pfe.G, seed=42)
    
    # 2. Stability Simulation (Wormhole in S5)
    wormhole = engine.inject_wormhole(0, 119, strength=2.0)
    
    # Pre-simulate the relaxation
    J_matrix = np.random.randn(120, 120) * 0.05
    J_matrix[0, 119] = 2.0; J_matrix[119, 0] = 2.0
    cost_func = engine.mapper.construct_cost_functional(J_matrix)
    
    state = {f'node_{i}': np.random.randn() * 0.1 for i in range(120)}
    history = [state.copy()]
    for _ in range(100):
        grad = cost_func.gradient(state)
        new_state = {}
        for i in range(120):
            g = grad[f'node_{i}']
            noise = np.random.randn() * 0.01
            new_state[f'node_{i}'] = state[f'node_{i}'] - (0.01 * g) + noise
        state = new_state
        history.append(state.copy())

    fig = plt.figure(figsize=(16, 8))
    fig.suptitle("Phase III: Structural Stability & Observer-Scope Projection", fontsize=18)
    
    # Panel A: The S5 Cayley Source
    ax1 = fig.add_subplot(121)
    ax1.set_title("Panel A: S5 Cayley Graph (The Invariant Kernel)")
    nx.draw(pfe.G, pos_s5, ax=ax1, node_size=20, node_color='gold', edge_color='gray', alpha=0.3)
    scatter_s5 = ax1.scatter([], [], c=[], s=50, cmap='plasma', zorder=10)
    
    # Panel B: Stability Heatmap
    ax2 = fig.add_subplot(122, projection='3d')
    ax2.set_title("Panel B: Manifold Stability (Wormhole Relaxation)")
    
    # Projected coordinates for 3D view
    x_nodes = [pos_s5[i][0] for i in range(120)]
    y_nodes = [pos_s5[i][1] for i in range(120)]
    z_nodes = np.zeros(120)
    
    scatter_3d = ax2.scatter(x_nodes, y_nodes, z_nodes, s=100, c='black', alpha=0.9, edgecolor='white')
    ax2.set_axis_off()
    
    # Add the wormhole line
    wormhole_line, = ax2.plot([pos_s5[0][0], pos_s5[119][0]], 
                             [pos_s5[0][1], pos_s5[119][1]], 
                             [0, 0], 'r--', lw=2, label="Wormhole Bridge")
    ax2.legend()

    def update(frame):
        # Update Panel A colors
        curr_s = history[frame]
        colors = [curr_s[f'node_{i}'] for i in range(120)]
        
        # Update Panel B 3D surface (we'll oscillate z based on amplitude)
        z_curr = np.array(colors)
        scatter_3d._offsets3d = (x_nodes, y_nodes, z_curr)
        scatter_3d.set_array(z_curr)
        scatter_3d.set_cmap('viridis')
        scatter_3d.set_clim(-1, 1)
        
        # Update wormhole line Z
        wormhole_line.set_data_3d([pos_s5[0][0], pos_s5[119][0]], 
                                  [pos_s5[0][1], pos_s5[119][1]], 
                                  [z_curr[0], z_curr[119]])
        
        return scatter_3d, wormhole_line

    anim = FuncAnimation(fig, update, frames=len(history), interval=50, blit=False)
    
    output_path = "phase3_structural_stability.mp4"
    print(f"Saving animation to {output_path}...")
    try:
        anim.save(output_path, writer='ffmpeg', fps=30, dpi=150)
        print("Save successful.")
    except Exception as e:
        print(f"Could not save mp4: {e}")
        anim.save("phase3_structural_stability.gif", writer='pillow', fps=30)
        print("Gif saved.")

if __name__ == "__main__":
    run_visualization()
