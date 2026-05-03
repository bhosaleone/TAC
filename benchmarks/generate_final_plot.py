import pandas as pd
import matplotlib.pyplot as plt

def generate_plot():
    try:
        df = pd.read_csv('page_curve_data.csv')
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    plt.figure(figsize=(12, 8))
    plt.plot(df['time'], df['entropy'], 'r-', lw=2.5, label='Radiation Entropy $S_{ent}$')
    
    # Identify Page Time (Peak)
    peak_idx = df['entropy'].idxmax()
    page_time = df.loc[peak_idx, 'time']
    page_entropy = df.loc[peak_idx, 'entropy']
    
    plt.axvline(x=page_time, color='gray', ls='--', alpha=0.8, label=f'Page Time (t={page_time:.1f})')
    plt.axhline(y=5000, color='blue', ls=':', alpha=0.5, label='Information Saturation ($N/2=5000$)')
    
    # Formatting
    plt.xlabel('Evaporation Time', fontsize=14)
    plt.ylabel('Entanglement Entropy', fontsize=14)
    plt.title('Unitary Page Curve — 10,000 Qubits (TAC Memory Bypass)', fontsize=16, pad=15)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3, which='both', linestyle='--')
    
    # Annotate the purification phase
    plt.annotate('Information Purification Phase', 
                 xy=(page_time + 100, page_entropy - 1000), 
                 xytext=(page_time + 200, page_entropy - 2000),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=8),
                 fontsize=12)

    plt.tight_layout()
    plt.savefig('page_curve_final.png', dpi=300)
    print("Successfully generated page_curve_final.png")

if __name__ == "__main__":
    generate_plot()
