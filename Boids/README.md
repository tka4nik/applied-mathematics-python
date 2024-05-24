# Boids Simulation

This project simulates the behavior of boids using the principles of separation, cohesion, and alignment. The simulation is controlled through a GUI made with PyQt, where you can adjust various coefficients using sliders.

## Introduction

Boids is an artificial life program, developed by Craig Reynolds in 1986, which simulates the flocking behavior of birds. The system is based on three simple steering behaviors:
- **Separation**: steer to avoid crowding local flockmates.
- **Cohesion**: steer to move toward the average position of local flockmates.
- **Alignment**: steer towards the average heading of local flockmates.

![Boids Simulation](./boids.gif)

## Features

- **Interactive GUI**: Adjust simulation parameters in real-time using sliders.
- **Numba Optimization**: High-performance computations using Numba for real-time simulation.
- **Wall Interactions**: Configurable behaviors for boids interacting with the simulation boundaries.
- **Class-Based Coefficients**: Different groups of boids can have unique behavior parameters.
