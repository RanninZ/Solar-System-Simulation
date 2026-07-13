Solar System Simulation 

2D Simulation of the orbital movement of the 7 planets around the Sun, solving Newtons's gravitational equations with 'scipy.integrate.solve_ivp'.

## What does the program do 

- Modeling of the gravitational force between the Sun and each planet with Newton's Universal Gravitational Law. 
- Converts second-order system of equations (F=ma) in a first-order system of equations, resolved with the integrator 'DOP853' of SciPy
- Animates the orbits at an adjustable speed with an interactive slider (matplotlib widgets).
- Uses symmetrical logarithmic scale in the axes to be able to view inner and outer planets.

## How to run.

'''bash
pip install -r requirements.txt
python simulacion_planetas.py

## Motivation 

Project created for learning the complete workflow of a physic simulation:
with the mathematic model ranging from manual numerical integration 
(Euler-Cromer method) as a first approach, to migrating 
to a professional SciPy solver.

## Future updates.

-Extend to 3D
- Add moons
- Include planet-planet gravitational interaction, not only planet-Sun