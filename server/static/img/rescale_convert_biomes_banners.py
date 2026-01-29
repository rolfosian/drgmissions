import subprocess
import os

scalefactor = 0.6

for file in os.listdir():
    if file.endswith(".png") and "DeepDive_MissionBar" in file:
        subprocess.run(["ffmpeg", "-i", file, "-vf", "scale=iw*0.6:ih*0.6", file.replace(".png", "") + "RESIZED.png"])
        os.remove(file)
        os.rename(file.replace(".png", "") + "RESIZED.png", file)
        subprocess.run(["ffmpeg", "-i", file, "-q:v 75", file.replace(".png", ".webp")])