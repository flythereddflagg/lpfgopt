import matplotlib.pyplot as plt
import numpy as np
from lpfg_0_5_2 import minimize
data = np.array([
    # T(K)  K_f
    [1000, 7.5E15],
    [2000, 3.8E15],
    [3000, 2.5E15],
    [4000, 1.9E15],
    [5000, 1.5E15]])

def k1(x, t): return x[0] * t**x[1] * np.exp(-x[2]/t)

def err(x): return np.sum((data[:,1] - k1(x, data[:,0]))**2.0)

guess = [5.3e16, -0.42265, -972.0] # powell method gave final error of ~ 2.81e13
intervals = [
    [1.0e10, 1.0e20],
    [-1.0 , 2.0],
    [-1000.0, 1000.0]]

opt_obj = minimize(err, intervals, full_output=True)
#print opt_obj.success   # Successful optimization?
#sol = opt_obj.x
print(opt_obj['best'])
#print(err(sol)/np.mean(data[:,1])) # Final error
'''
ts = np.linspace(1000,5000,1000)
ks = k1(sol, ts)
#kg = k1(guess, ts)

plt.plot(data[:,0],data[:,1],"ro")
plt.plot(ts,ks,"g--")
#plt.plot(ts,kg,"k-")
plt.legend(['data','fit'],loc='center left', bbox_to_anchor=(1, 0.5))

plt.show()'''