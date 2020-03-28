#%matplotlib inline
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

def main(arg):
    df = pd.read_csv(arg[0])
    df.head(10)
    df.describe()
    means = df.groupby(['Station', 'Year'])['Traffic'].mean()

    means.to_frame(name='Means AM Peak').to_excel('means_' + arg[0].split(".")[0] + '_peak.xlsx', 'Sheet1')

if __name__ == '__main__':
    main(sys.argv[1:])
