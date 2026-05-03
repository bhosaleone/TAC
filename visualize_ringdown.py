import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sys
import os

# Add current dir to pythonpath to import core
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.black_hole_manifold import BlackHoleManifold
from core.tac_coprocessor import TACCoprocessor

def run_visualization():
    # Setup
    N_DIM = 400  # We will map this 1D state into a 20x20 2D grid for 3D surface plotting
    GRID_SIZE = int(np.sqrt(N_DIM))
    manifold = BlackHoleManifold(N_dimensions=N_DIM, initial_distortion=5.0)
    
    # We use a slightly modified TAC to yield states step-by-step
    coprocessor = TACCoprocessor(kappa=0.05, temperature=0.01)
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title("God-Tier Optimization: O(1) Black Hole Ringdown Relaxation", fontsize=14, pad=20)
    
    X, Y = np.meshgrid(np.arange(GRID_SIZE), np.arange(GRID_SIZE))
    
    # Initial state
    Z = manifold.state.copy().reshape((GRID_SIZE, GRID_SIZE))
    surf = [ax.plot_surface(X, Y, Z, cmap='plasma', edgecolor='none')]
    
    ax.set_zlim(-10, 10)
    ax.set_axis_off()
    
    # Store history for animation
    history = [manifold.state.copy()]
    
    # Run the relaxation simulation
    state = manifold.state.copy()
    for _ in range(200): # max 200 steps
        grad = manifold.get_gradient(state)
        noise = np.random.randn(N_DIM) * np.sqrt(2 * coprocessor.kappa * coprocessor.temperature)
        state -= (coprocessor.kappa * grad) + noise
        history.append(state.copy())
        if np.linalg.norm(grad) < coprocessor.equilibrium_threshold:
            break
            
    print(f"Relaxation completed in {len(history)} steps.")
            
    def update(frame):
        ax.clear()
        ax.set_title(f"God-Tier Optimization: O(1) Black Hole Ringdown\nMacroscopic Step: {frame}/{len(history)}", fontsize=14)
        ax.set_zlim(-10, 10)
        ax.set_axis_off()
        Z_frame = history[frame].reshape((GRID_SIZE, GRID_SIZE))
        surf[0] = ax.plot_surface(X, Y, Z_frame, cmap='plasma', edgecolor='none', vmin=-5, vmax=5)
        return surf[0],

    anim = FuncAnimation(fig, update, frames=len(history), interval=50, blit=False)
    
    output_path = "ringdown_relaxation.mp4"
    print(f"Saving animation to {output_path}...")
    try:
        anim.save(output_path, writer='ffmpeg', fps=30, dpi=150)
        print("Save successful.")
    except Exception as e:
        print(f"Could not save mp4 using ffmpeg: {e}")
        print("Falling back to gif...")
        anim.save("ringdown_relaxation.gif", writer='pillow', fps=30)
        print("Gif saved.")

if __name__ == "__main__":
    print("Initializing Black Hole Manifold Continuous Relaxation...")
    run_visualization()
