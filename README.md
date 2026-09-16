# YUBI-Real2Sim

Real-to-simulation research project for the YUBI robotic platform.

This repository is intended to collect the tools and experiments needed to
connect real-world YUBI data with a simulated robot environment. The goal is
to make calibration, data conversion, policy replay, and real-to-sim
evaluation reproducible.

> **Status:** Early development. The repository is currently being initialized
> and does not yet contain a runnable pipeline.

## Project goals

- Transfer observations, actions, and trajectories between the real robot and simulation.
- Reconstruct or register the relevant scene and robot geometry.
- Evaluate robot policies in simulation before real-world execution.
- Keep experiment configurations, results, and provenance easy to reproduce.

## Planned components

The project structure will be introduced as the implementation grows:

```text
YUBI-Real2Sim/
├── src/       # Core conversion, calibration, and simulation code
├── scripts/   # Reproducible setup and experiment commands
├── configs/   # Experiment and environment configurations
├── docs/      # Design notes and experiment documentation
└── outputs/   # Local experiment results (not committed)
```

Large datasets, checkpoints, scene captures, and other generated assets should
be kept outside Git and documented with their source and checksums.

## Getting started

Clone the repository:

```bash
git clone git@github.com:Hirotin/YUBI-Real2Sim.git
cd YUBI-Real2Sim
```

The setup instructions and dependency versions will be added together with
the first runnable implementation.

## Roadmap

1. Define the real and simulated data formats.
2. Add robot and scene calibration utilities.
3. Implement real-to-sim trajectory and observation conversion.
4. Add policy replay and evaluation scripts.
5. Document reproducible experiments and benchmark results.

## License

License information will be added before the first public release.

