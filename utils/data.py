import os 
import pandas as pd 
from glob import glob

def model_load(data_path):
    subtitle = glob(data_path + "/*.ass")

    scripts = []
    episode_num = []

    for path in subtitle:
        with open(path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            lines = lines[27:]  # Skip the first 27 lines
            lines = [",".join(line.split(',')[9:]) for line in lines]

        lines = [line.replace("\\N", " ") for line in lines]
        script = " ".join(lines)

        # Extract the episode number from the filename
        episode = int(path.split("-")[-1].split(".")[0].strip())

        scripts.append(script)
        episode_num.append(episode)

    # Create the DataFrame and return it
    df = pd.DataFrame.from_dict({"episode": episode_num, "script": scripts})
    return df

