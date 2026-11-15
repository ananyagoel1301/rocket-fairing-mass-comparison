"""Idealised 1-D vertical powered-ascent simulation using Euler's method."""
import numpy as np

# ============================================================
# 1. ENGINE AND PHYSICAL PARAMETERS
# ============================================================

T = 100000.0
Isp = 305.0
g0 = 9.80665
RE = 6.371e6
R_air = 287.05287

# ============================================================
# 2. AERODYNAMIC PARAMETERS
# ============================================================

A = 0.7854
Cd = 0.3

# ============================================================
# 3. U.S. STANDARD ATMOSPHERE 1976
# ============================================================

# Geopotential altitude boundaries (m)
hb = np.array([
    0.0, 11000.0, 20000.0, 32000.0,
    47000.0, 51000.0, 71000.0, 84852.0
])

# Temperature lapse rates (K/m)
lapse = np.array([
    -0.0065, 0.0, 0.001, 0.0028,
    0.0, -0.0028, -0.002
])

# Calculate temperature and pressure at layer boundaries
Tb = [288.15]
pb = [101325.0]

for i, L in enumerate(lapse):
    dh = hb[i + 1] - hb[i]
    t_base = Tb[-1]
    p_base = pb[-1]

    if L == 0:
        t_next = t_base
        p_next = p_base * np.exp(
            -g0 * dh / (R_air * t_base)
        )
    else:
        t_next = t_base + L * dh
        p_next = p_base * (
            t_next / t_base
        ) ** (-g0 / (R_air * L))

    Tb.append(t_next)
    pb.append(p_next)

Tb = np.array(Tb)
pb = np.array(pb)


def atmospheric_density(h):
    """Calculate density using USSA76.

    h is geometric altitude in metres.
    Density is set to zero above 84.852 km geopotential altitude.
    """

    # Convert geometric altitude to geopotential altitude
    z = RE * h / (RE + h)

    # Simplifying assumption above 84.852 km
    if z > hb[-1]:
        return 0.0

    i = np.searchsorted(hb, z, side="right") - 1
    i = max(0, min(i, len(lapse) - 1))

    dz = z - hb[i]
    L = lapse[i]
    t_base = Tb[i]
    p_base = pb[i]

    if L == 0:
        temperature = t_base
        pressure = p_base * np.exp(
            -g0 * dz / (R_air * t_base)
        )
    else:
        temperature = t_base + L * dz
        pressure = p_base * (
            temperature / t_base
        ) ** (-g0 / (R_air * L))

    return pressure / (R_air * temperature)


# ============================================================
# 4. PROPELLANT AND FAIRING PARAMETERS
# ============================================================

propellant_mass = 4330.0
mdot = T / (Isp * g0)

# Fairing masses (kg)
M_baseline = 332.38
M_modified = 172.52

# Dry and initial masses (kg)
dry_baseline = 900.0
dry_modified = 900.0 - M_baseline + M_modified

initial_baseline = dry_baseline + propellant_mass
initial_modified = dry_modified + propellant_mass


# ============================================================
# 5. ASCENT SIMULATION
# ============================================================

def simulate(initial_mass, dry_mass, dt=0.01):
    """Simulate vertical powered ascent using Euler's method."""

    t = 0.0
    h = 0.0
    v = 0.0
    m = initial_mass

    results = []

    while m > dry_mass + 1e-12:
        step = min(dt, (m - dry_mass) / mdot)

        # Atmospheric density and gravity
        rho_air = atmospheric_density(h)
        g = g0 * (RE / (RE + h))**2

        # Drag force, acceleration and dynamic pressure
        D = 0.5 * rho_air * Cd * A * v**2
        acceleration = (T - D - m * g) / m
        q = 0.5 * rho_air * v**2

        results.append([t, h, v, m, acceleration, q])

        # Euler updates
        h = h + v * step
        v = v + acceleration * step
        m = max(dry_mass, m - mdot * step)
        t = t + step

    # Record the actual final burnout state
    rho_air = atmospheric_density(h)
    g = g0 * (RE / (RE + h))**2
    D = 0.5 * rho_air * Cd * A * v**2
    acceleration = (T - D - m * g) / m
    q = 0.5 * rho_air * v**2

    results.append([t, h, v, m, acceleration, q])

    return np.array(results)


# ============================================================
# 6. WORK CALCULATIONS
# ============================================================

def calculate_work(results):
    """Calculate gravitational work and drag work."""

    # Extract trajectory data
    t = results[:, 0]
    h = results[:, 1]
    v = results[:, 2]
    m = results[:, 3]

    # Gravitational acceleration at each altitude
    g = g0 * (RE / (RE + h))**2

    # Atmospheric density at each altitude
    rho = np.array([
        atmospheric_density(height) for height in h
    ])

    # Drag force at each point
    D = 0.5 * rho * Cd * A * v**2

    # Work done by gravity
    W_gravity = -np.trapezoid(m * g * v, t)

    # Work done by drag
    W_drag = -np.trapezoid(D * v, t)

    # Ratio of drag work to gravitational work
    ratio = abs(W_drag) / abs(W_gravity) * 100

    return W_gravity, W_drag, ratio, np.max(D)


# ============================================================
# 7. RUN BOTH SIMULATIONS AND DISPLAY RESULTS
# ============================================================

if __name__ == "__main__":

    # Run ascent simulations
    baseline = simulate(initial_baseline, dry_baseline)
    modified = simulate(initial_modified, dry_modified)

    # Calculate work for both designs
    Wg_baseline, Wd_baseline, ratio_baseline, Dmax_baseline = (
        calculate_work(baseline)
    )

    Wg_modified, Wd_modified, ratio_modified, Dmax_modified = (
        calculate_work(modified)
    )

    # --------------------------------------------------------
    # BASELINE DESIGN
    # --------------------------------------------------------

    print("========== BASELINE DESIGN ==========")

    print("Initial mass (kg):", initial_baseline)
    print("Dry mass (kg):", dry_baseline)
    print("Burnout time (s):", baseline[-1, 0])
    print("Burnout altitude (km):", baseline[-1, 1] / 1000)
    print("Burnout velocity (m/s):", baseline[-1, 2])

    print("Maximum dynamic pressure (kPa):",
          np.max(baseline[:, 5]) / 1000)

    print("Maximum drag force (kN):",
          Dmax_baseline / 1000)

    print("Gravitational work (GJ):",
          Wg_baseline / 1e9)

    print("Drag work (MJ):",
          Wd_baseline / 1e6)

    print("Drag/gravity work ratio (%):",
          ratio_baseline)

    print()

    # --------------------------------------------------------
    # MODIFIED DESIGN
    # --------------------------------------------------------

    print("========== MODIFIED DESIGN ==========")

    print("Initial mass (kg):", initial_modified)
    print("Dry mass (kg):", dry_modified)
    print("Burnout time (s):", modified[-1, 0])
    print("Burnout altitude (km):", modified[-1, 1] / 1000)
    print("Burnout velocity (m/s):", modified[-1, 2])

    print("Maximum dynamic pressure (kPa):",
          np.max(modified[:, 5]) / 1000)

    print("Maximum drag force (kN):",
          Dmax_modified / 1000)

    print("Gravitational work (GJ):",
          Wg_modified / 1e9)

    print("Drag work (MJ):",
          Wd_modified / 1e6)

    print("Drag/gravity work ratio (%):",
          ratio_modified)
