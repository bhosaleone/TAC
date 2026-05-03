import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from God_Tier_Optimization.hilbert_crystal import CrystalTopology5D, HilbertSpaceMapper
from core.tac_coprocessor import TACCoprocessor

def run_visualization():
    print("Initializing God-Tier 120-Qubit 5D Crystal Topology...")
    np.random.seed(42)
    topology = CrystalTopology5D(num_nodes=120)
    mapper = HilbertSpaceMapper(topology)
    
    # Generate a random but structured coupling matrix (J_ij)
    # We want a phase transition, so we create a ferromagnetic-like ground state bias
    J_matrix = np.random.randn(120, 120) * 0.1
    # Make it symmetric
    J_matrix = (J_matrix + J_matrix.T) / 2
    # Add strong ferromagnetic couplings for visual clustering
    for i in range(120):
        for j in topology.adjacency_list[i]:
            J_matrix[i, j] = np.abs(J_matrix[i, j]) + 0.5 

    cost_func = mapper.construct_cost_functional(J_matrix)
    
    # Build NetworkX graph for 3D spring layout
    G = nx.Graph()
    for i in range(120):
        G.add_node(i)
        for j in topology.adjacency_list[i]:
            G.add_edge(i, j)
            
    print("Computing 3D Spring Layout Projection...")
    # Compute 3D layout
    pos = nx.spring_layout(G, dim=3, seed=42)
    
    # Extract xyz
    x_nodes = [pos[i][0] for i in range(120)]
    y_nodes = [pos[i][1] for i in range(120)]
    z_nodes = [pos[i][2] for i in range(120)]
    
    # Initialize random state (amplitudes)
    initial_state = {f'node_{i}': np.random.randn() * 0.5 for i in range(120)}
    state = initial_state.copy()
    
    coprocessor = TACCoprocessor(kappa=0.02, temperature=0.005)
    
    history = [state.copy()]
    print("Running TAC Relaxation...")
    for _ in range(150):
        grad = cost_func.gradient(state)
        new_state = {}
        max_grad = 0
        for i in range(120):
            g = grad[f'node_{i}']
            noise = np.random.randn() * np.sqrt(2 * coprocessor.kappa * coprocessor.temperature)
            new_state[f'node_{i}'] = state[f'node_{i}'] - (coprocessor.kappa * g) + noise
            max_grad = max(max_grad, abs(g))
        state = new_state
        history.append(state.copy())
        if max_grad < coprocessor.equilibrium_threshold:
            break
            
    print(f"Collapse completed in {len(history)} steps.")
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title("God-Tier Optimization: 120-Qubit 5D Crystal Collapse", fontsize=14)
    ax.set_axis_off()
    
    # Plot edges once
    for edge in G.edges():
        ax.plot([pos[edge[0]][0], pos[edge[1]][0]],
                [pos[edge[0]][1], pos[edge[1]][1]],
                [pos[edge[0]][2], pos[edge[1]][2]], color='gray', alpha=0.3, linewidth=0.5)
                
    # Scatter plot for nodes
    scatter = ax.scatter(x_nodes, y_nodes, z_nodes, s=100, c='black', alpha=0.9, edgecolor='white')
    
    def update(frame):
        ax.set_title(f"God-Tier Optimization: 5D Crystal Collapse\nMacroscopic Step: {frame}/{len(history)}", fontsize=14)
        current_s = history[frame]
        colors = [current_s[f'node_{i}'] for i in range(120)]
        scatter.set_array(np.array(colors))
        scatter.set_cmap('coolwarm')
        scatter.set_clim(-1.5, 1.5)
        return scatter,

    anim = FuncAnimation(fig, update, frames=len(history), interval=50, blit=False)
    
    output_path = "crystal_collapse.mp4"
    print(f"Saving animation to {output_path}...")
    try:
        anim.save(output_path, writer='ffmpeg', fps=30, dpi=150)
        print("Save successful.")
    except Exception as e:
        print(f"Could not save mp4 using ffmpeg: {e}")
        print("Falling back to gif...")
        anim.save("crystal_collapse.gif", writer='pillow', fps=30)
        print("Gif saved.")

if __name__ == "__main__":
    run_visualization()
