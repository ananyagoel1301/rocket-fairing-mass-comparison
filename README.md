# Rocket Fairing Mass Comparison

Python implementation for the Advanced Calculus project **Launch Vehicle: Mass Comparison of Two Designs**.

This project investigates how changing the internal geometry of a rocket nose fairing affects its material volume and estimated structural mass. It also includes a simplified vertical ascent simulation to compare the motion of a launch vehicle using the two fairing designs.

## Project Overview

Both designs share the same external tangent-ogive profile but differ in their internal profiles:

- **Baseline design:** The inner radius is set to 90% of the outer radius.
- **Modified design:** The inner radius is defined by a constrained cubic polynomial.

Each fairing is modelled as a hollow surface of revolution. Numerical integration is used to calculate the internal volume, material volume and estimated mass of each design.

The calculated fairing masses are then used in a separate ascent simulation to investigate how the change in structural mass affects the vehicle's vertical motion.

## Repository Structure

```text
rocket-fairing-mass-comparison/
│
├── README.md
├── requirements.txt
│
├── code/
│   ├── fairing_volume.py
│   └── ascent_simulation.py
│
├── results/
│   ├── fairing_volume_output.txt
│   └── ascent_simulation_output.txt
│
└── Latex code/
    └── Project report source files
```

## Requirements

- Python 3.9 or later
- NumPy 2.0 or later

Install the required library using:

```bash
python -m pip install -r requirements.txt
```

## Running the Programs

To run the fairing volume and mass comparison:

```bash
python code/fairing_volume.py
```

To run the vertical ascent simulation:

```bash
python code/ascent_simulation.py
```

The programs print their calculated results in the terminal. The corresponding text files in the `results` folder contain the numerical outputs.

## 1. Fairing Volume and Mass Comparison

The fairing geometry uses the following parameters:

| Parameter | Value |
|---|---:|
| Fairing length | 1.5 m |
| Outer base radius | 0.5 m |
| Material density | 2700 kg/m³ |
| Number of integration points | 100,000 |

The material density is assumed to be 2700 kg/m³, corresponding approximately to aluminium 6061.

The program calculates:

- Outer volume
- Internal volume of both designs
- Material volume of both designs
- Estimated fairing mass
- Percentage reduction in mass

The volume calculations use numerical integration through NumPy's trapezoidal integration method.

### Fairing comparison results

| Measurement | Baseline | Modified |
|---|---:|---:|
| Internal volume | 0.524807 m³ | 0.584013 m³ |
| Material volume | 0.123103 m³ | 0.063897 m³ |
| Estimated mass | 332.38 kg | 172.52 kg |

The modified design gives an estimated mass reduction of approximately **48.09%** compared with the baseline design.

## 2. Vertical Ascent Simulation

The second program compares the idealised vertical ascent of the launch vehicle using the two fairing masses.

The simulation uses the following parameters:

| Parameter | Value |
|---|---:|
| Thrust | 100,000 N |
| Specific impulse | 305 s |
| Propellant mass | 4,330 kg |
| Drag coefficient | 0.3 |
| Reference area | 0.7854 m² |
| Time step | 0.01 s |

The model includes:

- Variable gravitational acceleration with altitude
- Atmospheric density based on a layered US Standard Atmosphere 1976 model
- Aerodynamic drag
- Changing vehicle mass as propellant is consumed
- Numerical integration using the forward Euler method

The simulation calculates:

- Initial and dry vehicle mass
- Burnout time
- Burnout altitude
- Burnout velocity
- Maximum dynamic pressure
- Maximum drag force
- Gravitational work
- Work done against aerodynamic drag
- Ratio of drag work to gravitational work

### Ascent simulation results

The results are recorded in `results/ascent_simulation_output.txt`.

The two designs are compared using the same thrust, specific impulse, propellant mass and other simulation parameters. Their initial and dry masses differ because of the change in estimated fairing mass.

## Assumptions and Limitations

### Fairing model

The fairing mass calculation assumes uniform material density and estimates mass from the difference between the outer and internal volumes.

The calculation does not include additional components such as joints, fasteners, separation mechanisms, insulation or manufacturing allowances.

The estimated mass reduction is based on geometry and material density. It does not establish that the modified design can withstand actual launch loads.

### Ascent model

The ascent simulation is an idealised one-dimensional vertical model, not a validated rocket flight prediction.

It assumes constant thrust, specific impulse, drag coefficient and reference area. Gravitational acceleration varies with altitude.

Atmospheric density is calculated using a layered US Standard Atmosphere 1976 model. The implemented model sets atmospheric density to zero above 84.852 km geopotential altitude.

The simulation does not account for changing vehicle orientation, staging, detailed aerodynamic effects, thermal loading or structural deformation.

### Structural considerations

The geometric comparison does not establish structural safety. Further engineering analysis would be required to evaluate stress, buckling, vibration, joints, manufacturing constraints and other structural requirements.

## Project Scope

The purpose of this project is to apply concepts from Advanced Calculus to an engineering problem.

The mathematical modelling connects surface representation, differentiation and numerical integration with the estimation of material volume and mass. The ascent simulation provides a further comparison of how the estimated mass difference affects the motion of a simplified launch vehicle.

The results should be interpreted within the assumptions and limitations of the mathematical models.
