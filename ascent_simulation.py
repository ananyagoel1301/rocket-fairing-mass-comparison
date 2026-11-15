"""Idealised 1-D vertical powered-ascent simulation using Euler's method."""
import numpy as np

# Engine and physical parameters
T = 100000.0
Isp = 305.0
g0 = 9.80665
RE = 6.371e6

# Atmospheric and aerodynamic parameters
A = 0.7854
Cd = 0.3
rho0 = 1.225
H = 8500.0

# Propellant parameters
propellant_mass = 4330.0
mdot = T / (Isp * g0)

# Fairing masses (kg)
M_baseline = 332.38
M_modified = 172.52

# Dry and initial masses
dry_baseline = 900.0
dry_modified = 900.0 - M_baseline + M_modified
initial_baseline = dry_baseline + propellant_mass
initial_modified = dry_modified + propellant_mass


def simulate(initial_mass, dry_mass, dt=0.01):
    t = 0.0
    h = 0.0
    v = 0.0
    m = initial_mass
    results = []

    while m > dry_mass:
        step = min(dt, (m - dry_mass) / mdot)

        # Atmospheric density and gravity
        rho_air = rho0 * np.exp(-h / H)
        g = g0 * (RE / (RE + h))**2

        # Drag, acceleration, and dynamic pressure
        D = 0.5 * rho_air * Cd * A * v**2
        acceleration = (T - D - m*g) / m
        q = 0.5 * rho_air * v**2

        results.append([t, h, v, m, acceleration, q])

        # Euler updates
        h = h + v * step
        v = v + acceleration * step
        m = max(dry_mass, m - mdot * step)
        t = t + step

    return np.array(results)


if __name__ == "__main__":
    baseline = simulate(initial_baseline, dry_baseline)
    modified = simulate(initial_modified, dry_modified)

    print("Baseline burnout altitude (m):", baseline[-1, 1])
    print("Baseline burnout velocity (m/s):", baseline[-1, 2])
    print("Modified burnout altitude (m):", modified[-1, 1])
    print("Modified burnout velocity (m/s):", modified[-1, 2])
    print("Baseline maximum dynamic pressure (Pa):", np.max(baseline[:, 5]))
    print("Modified maximum dynamic pressure (Pa):", np.max(modified[:, 5]))
