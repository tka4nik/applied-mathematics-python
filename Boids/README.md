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

## Images

![Screenshot_20240524_112755](https://github.com/tka4nik/applied-mathematics-python/assets/39916647/c2751a8a-98df-48cd-aa05-06c9207ecef0)

![Screenshot_20240524_113809](https://github.com/tka4nik/applied-mathematics-python/assets/39916647/171d1cb3-5b41-4067-8a7d-ad65c16bba19)

![Screenshot_20240524_113830](https://github.com/tka4nik/applied-mathematics-python/assets/39916647/7fe078dc-c5e6-4fe4-b083-76f08272a4c0)

Tkachenko Nikita, 2024
