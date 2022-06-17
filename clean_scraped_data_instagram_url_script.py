import numpy as np
import pandas as pd

file_name = "raw_scraped_data_instagram_url.txt"
file = open(file_name, errors="ignore")

for x in file:
    print(x)