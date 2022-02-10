import numpy as np
import matplotlib.pyplot as plt


# Producing 2 arrays called days and cases
days, cases = np.loadtxt("COVIDData.dat", skiprows=1, unpack=True)

print "Emma Hughes, 19335855"



fig = plt.figure(1)
plt.title("Covid Data")
plt.ylabel("Number of Cases")
plt.xlabel("Number of Days since 3/3/20")
ax = fig.gca()
ax.set_yticks(np.arange(0, 8000, 500))
plt.plot(days, cases)

fig = plt.figure(2)
plt.title("Logarithmic Covid Data")
plt.ylabel("ln(Number of Cases)")
plt.xlabel("Number of Days since 3/3/20")
plt.plot(days, np.log(cases))
plt.grid(which = 'both', linestyle = '--')
plt.grid(which = 'both', linestyle = '--')
ax = fig.gca()
ax.set_xticks(np.arange(0, 600, 25))
plt.show()