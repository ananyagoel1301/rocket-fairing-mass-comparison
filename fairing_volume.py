"""Fairing volume and mass comparison."""
import numpy as np

# Geometry and material parameters
L = 1.5
R = 0.5
rho = 2.5
density = 2700.0

x = np.linspace(0, L, 100_000)
yo = -2 + np.sqrt(6.25 - (1.5 - x)**2)
yi_baseline = 0.9 * yo

u = x / L
yi_modified = (
    0.02181035 * u**3
    - 0.52362070 * u**2
    + 0.98181035 * u
)

# Numerical volume integration
V_outer = np.pi * np.trapezoid(yo**2, x)
V_internal_baseline = np.pi * np.trapezoid(yi_baseline**2, x)
V_internal_modified = np.pi * np.trapezoid(yi_modified**2, x)
V_material_baseline = V_outer - V_internal_baseline
V_material_modified = V_outer - V_internal_modified

# Estimated fairing masses and percentage reduction
M_baseline = density * V_material_baseline
M_modified = density * V_material_modified
reduction = (M_baseline - M_modified) / M_baseline * 100

if __name__ == "__main__":
    print(f"Baseline internal volume: {V_internal_baseline:.6f} m^3")
    print(f"Modified internal volume: {V_internal_modified:.6f} m^3")
    print(f"Baseline material volume: {V_material_baseline:.6f} m^3")
    print(f"Modified material volume: {V_material_modified:.6f} m^3")
    print(f"Baseline fairing mass: {M_baseline:.2f} kg")
    print(f"Modified fairing mass: {M_modified:.2f} kg")
    print(f"Mass reduction: {reduction:.2f}%")
