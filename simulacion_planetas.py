import numpy
import scipy
import matplotlib

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


masa_sol = 1.989e30
G = 6.67e-11            # constante de gravitacion universal

planetas = [
    {"nombre": "Tierra", "masa": 5.972e24, "posicion": np.array([1.49e11, 0]), "velocidad": np.array([0, 29780]), "trayectoria": []},
    {"nombre": "Marte", "masa": 6.417e23, "posicion": np.array([2.279e11, 0]), "velocidad": np.array([0, 24070]), "trayectoria": []},
    {"nombre": "Venus", "masa": 4.867e24, "posicion": np.array([1.082e11, 0]), "velocidad": np.array([0, 35020]), "trayectoria": []},
    {"nombre": "Júpiter", "masa": 1.898e27, "posicion": np.array([7.785e11, 0]), "velocidad": np.array([0, 13070]), "trayectoria": []},
    {"nombre": "Saturno", "masa": 5.683e26, "posicion": np.array([1.4335e12, 0]), "velocidad": np.array([0, 9680]), "trayectoria": []},
    {"nombre": "Urano", "masa": 8.681e25, "posicion": np.array([2.8725e12, 0]), "velocidad": np.array([0, 6800]), "trayectoria": []},
    {"nombre": "Neptuno", "masa": 1.024e26, "posicion": np.array([4.4951e12, 0]), "velocidad": np.array([0, 5430]), "trayectoria": []},
]

posicion_sol = np.array([0,0])

#3. Funcion que calcula la distancia entre dos posiciones [x, y]

def fuerza_gravedad(pos1, masa1, pos2, masa2):
    diferencia = pos2 - pos1
    d = np.linalg.norm(diferencia)
    F = G * masa1 * masa2 / d**2
    direccion = diferencia / d
    return F * direccion

masas = [p["masa"] for p in planetas]
nombres = [p["nombre"] for p in planetas]

estado_inicial = []
for p in planetas:
    estado_inicial.extend(p["posicion"])
    estado_inicial.extend(p["velocidad"])
estado_inicial = np.array(estado_inicial)

def derivadas(t, estado):
    n = len(planetas)
    resultado = np.zeros(len(estado))
    
    for i in range(n):
        x = estado[4*i]
        y = estado[4*i + 1]
        vx = estado[4*i + 2]
        vy = estado[4*i + 3]
        pos = np.array([x, y])
        
        F= fuerza_gravedad(pos, masas[i], posicion_sol, masa_sol)
        aceleracion = F / masas[i]
        
        resultado[4*i] = vx
        resultado[4*i + 1] = vy
        resultado[4*i + 2] = aceleracion[0]
        resultado[4*i + 3] = aceleracion[1]
    return resultado

from scipy.integrate import solve_ivp

tiempo_total = 165 * 365 * 24 * 3600
tiempo_evaluacion = np.linspace(0, tiempo_total, 3000)

solucion = solve_ivp(
    derivadas, 
    t_span=(0, tiempo_total),
    y0 = estado_inicial,
    t_eval=tiempo_evaluacion,
    method="DOP853",
    rtol=1e-9,
    atol=1e-6,
)


for i, planeta in enumerate(planetas):
    x_vals = solucion.y[4*i]
    y_vals = solucion.y[4*i + 1]
    planeta["trayectoria"] = list(zip(x_vals, y_vals))
    


  
from matplotlib.widgets import Slider

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)

puntos = []
etiquetas = []
for planeta in planetas:
    punto, = ax.plot([], [], 'o', label=planeta["nombre"])
    puntos.append(punto)
    
    etiqueta = ax.annotate(planeta["nombre"], xy=(0, 0), xytext=(0, 10), textcoords="offset points", ha="center")
    etiquetas.append(etiqueta)

ax.scatter([0], [0], color="yellow", s=200, label="Sol")
ax.set_xlim(-5e12, 5e12)
ax.set_ylim(-5e12, 5e12)
ax.set_xscale("symlog", linthresh=1e10)
ax.set_yscale("symlog", linthresh=1e10)
ax.legend()

ax_slider = plt.axes([0.2, 0.05, 0.6, 0.03])
slider_velocidad = Slider(ax_slider, "Velocidad", 1, 2000, valinit=1, valstep=1)

contador = [0]

def actualizar(frame):
    velocidad = int(slider_velocidad.val)
    contador[0] += velocidad
    
    if contador[0] >= len(planetas[0]["trayectoria"]):
        contador[0] = 0
    
    for i, planeta in enumerate(planetas):
        posicion = planeta["trayectoria"][contador[0]]
        puntos[i].set_data([posicion[0]], [posicion[1]])
        etiquetas[i].xy = ([posicion[0], posicion[1]])
    return puntos + etiquetas





ani = animation.FuncAnimation(fig, actualizar, frames=len(planetas[0]["trayectoria"]), interval=1)
plt.show()


