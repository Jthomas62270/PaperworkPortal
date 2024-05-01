"""
Author: John 
"""

import pandas as pd 

def extract_patch(filename, outfile): 
    data = pd.read_csv(
        filename, usecols=[0, 1, 6], skiprows=[0, 1], names=["Channels", "Fixture Type", "Address"]).dropna()
    data = data.set_index("Channels")

    data = data[:60]
    
    print(data)
    data.to_csv(outfile)
