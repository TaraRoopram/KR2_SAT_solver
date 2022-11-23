import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data = {
    'mean_runtime': [1.78, 3.63, 1.87, 1.76, 1.99],
    'mean_backtracks': [4.02, 113.28, 6.21, 2.97, 11.29],
    'mean_sat_clauses': [3335.35, 1365.89, 3031.51, 3878.34, 2849.76]
}

# form dataframe
df = pd.DataFrame(data, columns=['mean_runtime', 'mean_backtracks', 'mean_sat_clauses'])
print("Dataframe is : ")
print(df)

matrix = df.corr().round(3)
print("Correlation matrix is : ")
print(matrix)

sns.heatmap(matrix, annot=True, vmax=1, vmin=-1, center=0)
plt.show()
