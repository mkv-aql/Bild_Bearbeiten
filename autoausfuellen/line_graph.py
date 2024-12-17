
import matplotlib as plt
import matplotlib.pyplot as plt
import numpy as np


x = [38.81, 80, 98, 100, 160]
y = [528.01, 1088.4, 1333.29, 1357.59,  2016.22]

# create interpolation
x_new = np.linspace(min(x), max(x), 100)
y_new = np.interp(x_new, x, y)

# plot the original data
plt.scatter(x, y)
# plot the interpolated data
plt.plot(x_new, y_new)
plt.show()



plt.plot(x, y)
plt.show()

z = []
for i in range(len(x)):
    z.append((y[i] / x[i]))

# create interpolation
x_new = np.linspace(0, max(x), 100)
z_new = np.interp(x_new, x, z)

plt.scatter(x, z)
plt.plot(x_new, z_new)
plt.show()
