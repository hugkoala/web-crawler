import numpy as np, pandas as pd, matplotlib.pyplot as plt


json1 = pd.read_json(path_or_buf='../web-crawler/stock_20190122.json', encoding='utf-8')
print(json1)

# json1.plot()
# plt.show()
