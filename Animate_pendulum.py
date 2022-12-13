import matplotlib.pyplot as plt
import matplotlib.animation as anim
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import pandas as pd
import os
import numpy as np

data_path = os.path.join("D:", "Big_data", "PHS2107_mec_sup_projet_final", "2022_12_12_17_39_31_806987.csv")

data = pd.read_csv(data_path)
x = data["t"]
y = data["teta"]

fig, ax = plt.subplots(figsize=(10, 10))
mass, = ax.plot([], [], "ob")
tige, = ax.plot([], [], "r")
image_path = "photo_prof.png"

image = OffsetImage(plt.imread(image_path, format="png"), zoom=.2)
ab = AnnotationBbox(image, (0, 0), frameon=False)
sapin = ax.add_artist(ab)

plt.xlim(-1.5, 1.5)
plt.ylim(-1.5, 1.5)
ax.axis("equal")


def animate(i):
    teta = y[i]
    x_now = -np.sin(teta)
    y_now = -np.cos(teta)
    mass.set_data(x_now, y_now)
    tige.set_data([0, x_now], [0, y_now])
    sapin.xybox = (x_now, y_now)
    return mass, tige


ani = anim.FuncAnimation(fig, animate, frames=1000, interval=10)
plt.show()
