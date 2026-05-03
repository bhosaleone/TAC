import numpy as np
import time
import matplotlib.pyplot as plt
from core.tac_coprocessor import TACCoprocessor

class NeuralFieldManifold:
    """
    Treats a Neural Network's weight landscape as a thermodynamic manifold.
    """
    def __init__(self, X, y, layer_sizes):
        self.X = X
        self.y = y
        self.layer_sizes = layer_sizes
        
        # Initialize weights
        self.weights = []
        self.total_params = 0
        for i in range(len(layer_sizes) - 1):
            w = np.random.normal(0, 0.1, (layer_sizes[i], layer_sizes[i+1]))
            self.weights.append(w)
            self.total_params += layer_sizes[i] * layer_sizes[i+1]
            
        self.state = self.flatten_weights(self.weights)
        
    def flatten_weights(self, weights):
        return np.concatenate([w.flatten() for w in weights])
        
    def unflatten_weights(self, state):
        weights = []
        curr = 0
        for i in range(len(self.layer_sizes) - 1):
            size = self.layer_sizes[i] * self.layer_sizes[i+1]
            w = state[curr:curr+size].reshape((self.layer_sizes[i], self.layer_sizes[i+1]))
            weights.append(w)
            curr += size
        return weights

    def forward(self, weights, X):
        a = X
        for i, w in enumerate(weights):
            z = np.dot(a, w)
            a = np.tanh(z) if i < len(weights) - 1 else z # Tanh for hidden, Linear for output
        return a

    def get_gradient(self, state):
        weights = self.unflatten_weights(state)
        
        # Forward pass
        activations = [self.X]
        zs = []
        for i, w in enumerate(weights):
            z = np.dot(activations[-1], w)
            zs.append(z)
            a = np.tanh(z) if i < len(weights) - 1 else z
            activations.append(a)
            
        # Backward pass (to get the gradient of the loss functional)
        # Loss = MSE
        error = activations[-1] - self.y
        delta = error # Linear output
        
        grads = []
        for i in reversed(range(len(weights))):
            grad_w = np.dot(activations[i].T, delta) / len(self.X)
            grads.append(grad_w)
            if i > 0:
                delta = np.dot(delta, weights[i].T) * (1 - activations[i]**2) # Tanh derivative
                
        # The TAC receives the FULL gradient vector of the manifold at once
        return self.flatten_weights(reversed(grads))

class AIFieldCollapseChallenge:
    """
    Target 1: Neural Network Training as Thermodynamic Relaxation.
    """
    def __init__(self, input_dim=10, hidden_dim=20, output_dim=1):
        # Generate synthetic regression data
        self.X = np.random.randn(100, input_dim)
        self.y = np.sum(self.X[:, :3], axis=1, keepdims=True) # Target is sum of first 3 features
        
        self.layer_sizes = [input_dim, hidden_dim, output_dim]
        self.tac = TACCoprocessor(kappa=0.01, temperature=0.01)
        self.tac.equilibrium_threshold = 0.01
        
    def train_via_field_collapse(self):
        manifold = NeuralFieldManifold(self.X, self.y, self.layer_sizes)
        
        print(f"--- AI Field Collapse: Training {manifold.total_params} Parameters ---")
        
        start_t = time.perf_counter()
        relaxed_weights_flat, steps = self.tac.tac_offload(manifold)
        t_tac = (time.perf_counter() - start_t) * 1000
        
        relaxed_weights = manifold.unflatten_weights(relaxed_weights_flat)
        preds = manifold.forward(relaxed_weights, self.X)
        final_loss = np.mean((preds - self.y)**2)
        
        print(f"Final Loss: {final_loss:.6f}")
        print(f"Steps: {steps}, Time: {t_tac:.2f}ms")
        
        return steps, final_loss

def run_scaling_test():
    configs = [
        [50, 100, 1],    # 5,100 params
        [50, 200, 1],    # 10,200 params
        [50, 500, 1],    # 25,500 params
        [50, 1000, 1],   # 51,000 params
        [50, 100, 100, 1] # Deep (15,000 params)
    ]
    
    param_counts = []
    tac_steps = []
    
    for config in configs:
        challenge = AIFieldCollapseChallenge(input_dim=config[0], hidden_dim=config[1], output_dim=config[-1])
        # Force a specific hidden structure if more than 3 elements
        if len(config) > 3:
            challenge.layer_sizes = config
            
        steps, loss = challenge.train_via_field_collapse()
        
        # Calculate total params
        total_p = 0
        for i in range(len(challenge.layer_sizes) - 1):
            total_p += challenge.layer_sizes[i] * challenge.layer_sizes[i+1]
            
        param_counts.append(total_p)
        tac_steps.append(steps)
        
    plt.figure(figsize=(10, 6))
    plt.plot(param_counts, tac_steps, 'o-', color='magenta', linewidth=3, label='TAC Field Collapse (O(1))')
    plt.axhline(y=1001, color='gray', linestyle='--', label='Turing Complexity Wall (Hypothetical)')
    
    plt.title('AI Scaling Supremacy: Training Complexity vs. Parameter Count', fontsize=16)
    plt.xlabel('Number of Parameters', fontsize=14)
    plt.ylabel('Thermodynamic Relaxation Steps', fontsize=14)
    plt.xscale('log')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('visual_artifacts/ai_scaling_supremacy.png', dpi=300)
    print("Saved visual_artifacts/ai_scaling_supremacy.png")

if __name__ == "__main__":
    run_scaling_test()
