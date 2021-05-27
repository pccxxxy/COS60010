from matplotlib import pyplot as plt
import pandas as pd

df = pd.read_csv('book_sorted.csv')
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
print(df.head(5))
print(df['Keywords'].dtype)
ax.scatter(df['Keywords'], df['Frequency'])  # You can also add more variables here to represent color and size.
plt.show()
