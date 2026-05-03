import numpy as np
import matplotlib.pyplot as plt
from core.gtf_engine import GTFEngine

def run_energy_supremacy():
    engine = GTFEngine(eta_geo=0.72)
    
    # Simulation Parameters (City Scale)
    hours = np.arange(24)
    solar_gradient = 800 * np.sin(np.pi * hours / 24)**2 # Solar cycle
    sky_gradient = 100 * np.ones(24)                    # Constant sky background
    input_power = 20 * np.ones(24)                      # Minimal active control
    
    gtf_elec = []
    gtf_cool = []
    trad_ac_cost = []
    
    for h in hours:
        elec, cool = engine.simulate_energy_coproduct(solar_gradient[h], sky_gradient[h], input_power[h])
        gtf_elec.append(elec)
        gtf_cool.append(cool)
        
        # Traditional AC cost (to get same cooling, COP=3.0)
        trad_ac_cost.append(cool / 3.0)
        
    print("===================================================================")
    print("CLEAN ENERGY SUPREMACY: Bhosale GTF vs. Traditional Infrastructure")
    print("===================================================================")
    print(f"Total Electricity Generated (24h): {sum(gtf_elec):.2f} Wh/m^2")
    print(f"Total Passive Cooling Provided (24h): {sum(gtf_cool):.2f} Wh/m^2")
    print(f"Energy Debt Avoided (vs. Trad AC): {sum(trad_ac_cost):.2f} Wh/m^2")
    print("===================================================================")
    
    # Generate Plot
    plt.figure(figsize=(10, 6))
    plt.plot(hours, gtf_elec, label='GTF Electricity (Co-product)', color='orange', linewidth=2)
    plt.plot(hours, gtf_cool, label='GTF Passive Cooling (Co-product)', color='cyan', linestyle='--')
    plt.fill_between(hours, trad_ac_cost, color='red', alpha=0.2, label='Traditional AC Energy Debt')
    
    plt.title('Bhosale GTF: Solving the "Cold Crunch" via Geometry', fontsize=16)
    plt.xlabel('Hour of Day', fontsize=14)
    plt.ylabel('Power Output (W/m^2)', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('gtf_energy_supremacy.png', dpi=300)
    print("Saved gtf_energy_supremacy.png")

if __name__ == "__main__":
    run_energy_supremacy()
