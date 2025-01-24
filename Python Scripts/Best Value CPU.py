import pandas as pd
import re

# Συντελεστές για τη συνάρτηση κόστους
k1 = 0.0794
k2 = 0.0794
k3 = 0.0159
a1 = 0.1
a2 = 0.1
a3 = 0.05

# Συνάρτηση για τον υπολογισμό του κόστους
def calculate_cost(L1I_size, L1I_assoc, L1D_size, L1D_assoc, L2_size, L2_assoc):
    return (
        k1 * L1I_size + a1 * L1I_assoc +
        k2 * L1D_size + a2 * L1D_assoc +
        k3 * L2_size + a3 * L2_assoc
    )

# Διαβάζουμε το Excel με τα δεδομένα
file_path = "specsjeng_results.xlsx"  # Αλλάξτε το όνομα αρχείου αν χρειάζεται
sheet_name = 0  # Φύλλο εργασίας

data = pd.read_excel(file_path, sheet_name=sheet_name)

# Εξαγωγή τιμών από τη στήλη "Benchmarks" μέσω regex
pattern = r"icache_(\d+)kB_(\d+)assoc_dcache_(\d+)kB_(\d+)assoc_l2_(\d+)MB_(\d+)assoc"
data[["L1I_size", "L1I_assoc", "L1D_size", "L1D_assoc", "L2_size", "L2_assoc"]] = data["Benchmarks"].str.extract(pattern).astype(float)
data["L2_size"] *= 1024  # Μετατροπή MB σε kB

# Αφαίρεση των γραμμών με NaN
data = data.dropna()

# Μετατροπή στηλών σε float αν δεν είναι ήδη
if data["system.cpu.cpi"].dtype != "float64":
    data["system.cpu.cpi"] = data["system.cpu.cpi"].astype(float)

# Προσθέτουμε στήλη με το κόστος για κάθε run
data["Cost"] = data.apply(lambda row: calculate_cost(
    row["L1I_size"],
    row["L1I_assoc"],
    row["L1D_size"],
    row["L1D_assoc"],
    row["L2_size"],
    row["L2_assoc"]
), axis=1)

# Εύρεση του run με το μικρότερο CPI
best_cpi_run = data.loc[data["system.cpu.cpi"].idxmin()]
print("\nRun με το μικρότερο CPI:")
print(f"Benchmark: {best_cpi_run['Benchmarks']}")
print(f"CPI: {best_cpi_run['system.cpu.cpi']:.6f}")
print(f"Cost: {best_cpi_run['Cost']:.6f}")

# Δυνατότητα ορισμού ορίου κόστους
cost_limit = 50  # Αλλάξτε το όριο αν χρειάζεται
filtered_data = data[data["Cost"] <= cost_limit]

if not filtered_data.empty:
    best_run_within_limit = filtered_data.loc[filtered_data["system.cpu.cpi"].idxmin()]
    print("\nRun με το μικρότερο CPI εντός ορίου κόστους:")
    print(f"Benchmark: {best_run_within_limit['Benchmarks']}")
    print(f"CPI: {best_run_within_limit['system.cpu.cpi']:.6f}")
    print(f"Cost: {best_run_within_limit['Cost']:.6f}")
else:
    print("\nΔεν βρέθηκαν runs εντός του ορίου κόστους.")
