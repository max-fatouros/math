from PIL import Image
from tqdm import tqdm


def gif(frame_count, frame_dir="frames"):
    images = [Image.open(f"{frame_dir}/{frame}.png") for frame in tqdm(range(frame_count), desc="Saving")]
    images[0].save("wave.gif", save_all=True, append_images=images[1:],
                   duration=75, loop=0)
