# Rocket Fairing Mass Comparison

Python implementation for the Advanced Calculus project **Launch Vehicle: Mass Comparison of Two Designs**.

The project compares two hollow, axisymmetric fairing designs with the same fixed external tangent-ogive profile:
- **Baseline:** inner radius is 90% of the outer radius.
- **Modified:** inner radius is a constrained cubic polynomial.

The code estimates internal volume, material volume, fairing mass, and percentage mass reduction. A separate program uses Euler's method to compare idealised vertical powered ascent.

## Repository structure

```text
rocket-fairing-mass-comparison/
├── README.md
├── requirements.txt
├── .gitignore
├── code/
│   ├── fairing_volume.py
│   └── ascent_simulation.py
└── results/
    ├── fairing_volume_output.txt
    └── ascent_simulation_output.txt
```

## Requirements and execution

Python 3.9+ and NumPy 2.0+.

```bash
python -m pip install -r requirements.txt
python code/fairing_volume.py
python code/ascent_simulation.py
```

## Main assumptions

**Fairing geometry:** length 1.5 m; outer base radius 0.5 m; tangent-ogive generating-circle radius 2.5 m; baseline inner profile 0.9 times the outer profile; modified inner profile is the constrained cubic; aluminium 6061 density is assumed to be 2700 kg/m³. Volume integrals are evaluated with the trapezoidal rule.

**Powered ascent:** thrust 100,000 N; specific impulse 305 s; propellant mass 4330 kg; drag coefficient 0.3; reference area 0.7854 m²; sea-level air density 1.225 kg/m³; atmospheric scale height 8500 m; variable gravity; Euler time step 0.01 s.

## Limitations

The ascent model is an idealised one-dimensional vertical simulation, not a validated flight prediction. It assumes constant thrust, specific impulse, and drag coefficient, and uses an exponential atmospheric-density approximation. It does not include a full aerodynamic, thermal, or structural assessment.

The geometric wall-thickness condition is not a structural safety assessment. Stress, buckling, vibration, joints, fasteners, and manufacturing allowances are not modelled.
