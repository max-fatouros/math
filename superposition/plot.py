import os
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import multiprocessing


def make(function_list, frame_dir="frames",
         frames=100, grid_points=20000, processes_count=6, bounds=20,
         computational_divisions=3, dpi=500, amplitude=1, is_transparent=False):
    x = np.linspace(-bounds, bounds, grid_points)
    y = np.linspace(-bounds, bounds, grid_points)

    # Ensure directory exists
    os.makedirs(frame_dir, exist_ok=True)

    # Work that will be split up into separate processes.
    def multiprocess_func(process, frame_bunch):
        # Generate one plot per frame
        for frame in tqdm(frame_bunch, desc=f"Process: {process}", position=1, leave=False):
            # Initialize plot
            fig = plt.figure()
            ax = fig.add_subplot(projection='3d')
            ax.set_zlim(0, 20 * amplitude)
            # Let 0 <= t < 2*pi so that the gif loops perfectly
            t = (2*np.pi / frames) * frame
            if is_transparent:
                plt.axis("off")
                ax.grid(False)
                ax.set_xticks([])
                ax.set_yticks([])
                ax.set_zticks([])

            for xs in np.array_split(x, computational_divisions):
                for ys in np.array_split(y, computational_divisions):
                    X, Y = np.meshgrid(xs, ys, sparse=True)
                    Z = amplitude * np.array(
                        [function(np.hypot(X - a, Y - b) - t) for function, a, b in function_list]
                    )[0]

                    ax.plot_surface(X, Y, Z, cmap=plt.cm.YlGnBu_r)

            plt.savefig(f"{frame_dir}/{frame}.png", dpi=dpi, transparent=is_transparent)
            # plt.show()
            plt.close()

    # Choose process count at top of file.
    # Divide frames into bunches and distribute across cores.
    frame_bunches = np.array_split(
        np.arange(frames),
        processes_count
    )
    processes = []
    for process in range(processes_count):
        p = multiprocessing.Process(target=multiprocess_func, args=(process, frame_bunches[process],))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()
