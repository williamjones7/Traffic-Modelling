from multi_lanes import Car, Road
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import pandas as pd

raw_counts = pd.read_csv('Data/dft_rawcount_local_authority_id_31.csv')

print(raw_counts.head())