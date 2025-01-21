import numpy as np
from scipy.optimize import least_squares

# Δεδομένα από τους επεξεργαστές (cores, boost frequency (GHz), price ($))
data = np.array([
    #Zen3
    #[8, 4.7, 499],    # Ryzen 7 5800X
    #[6, 4.6, 299],    # Ryzen 7 5600X
    #Zen2
    # [8, 4.4, 329],    # Ryzen 7 3700X
    # [6, 4.4, 249],    # Ryzen 5 3600X
    # Coffe Lake
    #[8, 4.7, 330],    # Coffe Lake i7-9700F
    #[6, 4.1, 182],    # Coffe Lake i5-9400F
    #Rocket lake
    [8, 5.0, 399],    # Rocket Lake i9-11700KF
    [6, 4.9, 262],    # Rocket Lake i7-11600F
])

# Fix k4 to a constant value
fixed_k4 = 10

# Συνάρτηση κόστους
def cost_function(params, data):
    k1, k2, k3 = np.maximum(params, 0)  # Ensure non-negative coefficients
    errors = []
    for cores, boost_freq, price in data:
        predicted_price = k1 * cores + k2 * cores**2 + k3 * (boost_freq-2)**2 + fixed_k4
        errors.append(predicted_price - price)
    return errors

# Αρχικές τιμές για τους συντελεστές (k1, k2, k3)
initial_guess = [10, 1, 10]

# Εφαρμογή least squares για να βρούμε τους συντελεστές
result = least_squares(cost_function, initial_guess, args=(data,))

# Εξαγωγή των υπολογισμένων συντελεστών (non-negative and non-zero)
k1, k2, k3 = np.maximum(result.x, 0.001)
print(f"k1: {k1}, k2: {k2}, k3: {k3}, k4: {fixed_k4}")

# Υπολογισμός και εκτύπωση των σφαλμάτων (errors) για κάθε επεξεργαστή
errors = cost_function([k1, k2, k3], data)
for i, (cores, boost_freq, price) in enumerate(data):
    predicted_price = k1 * cores + k2 * cores**2 + k3 * (boost_freq-2)**2 + fixed_k4
    print(f"Processor {i + 1}: Cores={cores}, Boost_Freq={boost_freq}GHz, "
          f"Actual_Price=${price}, Predicted_Price=${predicted_price:.2f}, "
          f"Error=${errors[i]:.2f}")

print(f"Core cost for a 1GHz CPU would be :{k1 + k2 +  fixed_k4}, ")
print(f"Core cost for a 3GHz CPU would be :{k1 + k2 + k3 + fixed_k4}, ")
print(f"Core cost for a 4 core 3GHz CPU would be :{k1 * 4 + 16 * k2 + k3  + fixed_k4}, ")
print(f"Core cost for a 4 core 4GHz CPU would be :{k1 * 4 + 16 * k2 + k3  + fixed_k4}, ")
print(f"Core cost for a 2 core 3GHz CPU would be :{k1 * 2 + 4 * k2 + k3  + fixed_k4}, ")
