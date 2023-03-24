import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("")

print(df)

for col in df.columns:
    print(col)

plt.plot(df[""])
plt.show()