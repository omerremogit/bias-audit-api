import numpy as np
import pandas as pd

# Load pre-computed group means
group_means = np.load("group_means.npy", allow_pickle=True).item()
race_map = {0: "White", 1: "Black", 2: "Asian", 3: "Indian", 4: "Others"}

def audit_encoding(encoding):
    distances = {
        race_map[k]: np.linalg.norm(encoding - v) for k, v in group_means.items()
    }
    closest_group = min(distances, key=distances.get)
    return {
        "distances": distances,
        "closest_group": closest_group
    }