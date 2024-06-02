# Boids Simulation

This project simulates the behavior of boids using the principles of separation, cohesion, and alignment. The simulation is controlled through a GUI made with PyQt, where you can adjust various coefficients using sliders.

## Introduction

Boids is an artificial life program, developed by Craig Reynolds in 1986, which simulates the flocking behavior of birds. The system is based on three simple steering behaviors:

| Interactions Type                                                                                                 | Visualization                        |
|-------------------------------------------------------------------------------------------------------------------|--------------------------------------|
| **Separation**: Attempt to not be too close to other boids in the perception radius.                              | ![image](https://github.com/tka4nik/applied-mathematics-python/assets/39916647/884476d8-a149-4b31-a6c9-9294fd274520) |
| **Alignment**: Speed vector strives to match the speed vectors of other boids in the perception radius.           | ![image](https://github.com/tka4nik/applied-mathematics-python/assets/39916647/93a7d688-5a8e-4b46-bec6-05a4335daa24) |
| **Cohesion**: Attempt to move towards the center of the mass of the surrounding boids.                            |![image](https://github.com/tka4nik/applied-mathematics-python/assets/39916647/26f1032a-822a-43fb-a74a-36a0a3c1e3b2) |

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
