# Applied Mathematics in Python

This repository contains a collection of projects in applied mathematics implemented in Python. The projects cover various topics such as fractals, heat transfer and ferromagnetics simulations, and nonlinear dynamics.

## Projects

1. [**Julia Set Fractal**](Fractals): Given a mapping generates a corresponding Julia fractal that you can interactively explore.
2. [**Heat Transfer Simulation**](Heat%20Transfer): Simulate heat transfer scenarios using diffusion equations.
3. [**Ferromagnetics Simulation**](Ferromagnetics): Calculates Mean Energy of a ferromagnetic using Ising's model.
4. [**Boids Simulation**](Boids): Simulates behavior of a flock of "birds" by applying 3 simple rules: separation, cohesion and alignment.
5. [**Nonlinear Dynamics Graphs**](Nonlinear%20Systems%20Exploration):
   - Bifurcation Diagrams: Visualizes the behavior of nonlinear systems as parameters change.
   - Mapping Diagrams: Mappps the evolution of a given discrete dynamic system. 
   - Lyapunov Exponent Graphs: Analyze the stability of chaotic systems.
6. [**Numerical Methods**](Numerical%20Methods): Implementaion of various numerical methods to solve different problems in mathematics.

## About the Author

This project is the work of **Nikita Tkachenko**, a student at **Higher School of Economics** during the academic years 2023-2024.

## Installation Guide

### Requirements
- Python (>=3.6)
- Jupyter Notebook
- Each projects' requirements are listed in corresponding `requirenemets.txt` files.

### Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/tka4nik/Applied_Mathematics_Python.git
    cd applied-mathematics-python
    ```

2. Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

3. Install dependencies:
    ```bash
    pip install -r <choosen_project_ditectory>/requirements.txt
    ```

4. Launch Jupyter Notebook:
    ```bash
    jupyter notebook
    ```
    
## License

This project is licensed under the [MIT License](LICENSE).
