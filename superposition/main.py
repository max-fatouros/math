import plot
import save
import numpy as np


FRAMES = 100

plot.make([
    (np.cos, 0, 3),
    (np.cos, 0, -3),
], frames=FRAMES, processes_count=6, is_transparent=True)

save.gif(FRAMES)