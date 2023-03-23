import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("")

print(df)

plt.plot(df["netIncome"])
plt.show()