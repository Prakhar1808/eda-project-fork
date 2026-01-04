import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

x=np.linspace(0, 10, 100)
print("x values:")
print(x)
y=np.sin(x)
print("y values (sine of x):")
print(y)

# plotting the values
plt.plot(x, y)
plt.title("Sine Wave") # Add title to the plot
plt.xlabel("x") # Label for x-axis
plt.ylabel("sin(x)") # Label for y-axis
plt.grid(True) # Add grid for better readability
plt.show()