import numpy as np

### Using geometrized units; c=G=1.

'''
Initial Velocity       c
BG Image Position      -100 m
Target Plane           100 m
Mass                   6.3419408698e9 m (=8.54e36 kg) Note: Yes masses are in units of length here, so Rs=2M
'''

# Default Values
c = 1 # Speed of light
G = 1 # Gravitational constant

# rk4
def rk4(u, f, t, h):
	"""Runge-Kutta RK4"""
	k1 = f(t, u)
	k2 = f(t + 0.5*h, u + 0.5*h*k1)
	k3 = f(t + 0.5*h, u + 0.5*h*k2)
	k4 = f(t + h, u + h*k3)
	return u + h/6 * (k1 + 2*k2 + 2*k3 + k4)

# Runge-Kutta-Fehlberg method (dynamic time step)
# Butcher tableau from, FORMULA 2 Table III in Fehlberg.
def rk45(u, f, t, h, Tol = 1e-3):
	A = np.array([0, 1/4, 3/8, 12/13, 1, 1/2])
	B = np.array([
		[0,0,0,0,0],
		[1/4, 0, 0, 0, 0],
		[3/32, 9/32, 0,0,0],
		[1932/2197, -7200/2197, 7296/2197, 0, 0],
		[439/216, -8, 3680/513, -845/4104, 0],
		[-8/27, 2, -3544/2565, 1859/4104, -11/40]
	])
	C = np.array([25/216,0,1408/2565,2197/4101,-1/5,0])
	CH = np.array([16/135,0,6656/12825,28561/56430,-9/50,2/55])
	CT = np.array([-1/360,0,128/4275,2197/75240,-1/50,-2/55])
	k1 = h*f(t+A[0]*h, u)
	k2 = h*f(t+A[1]*h, u+B[1,0]*k1)
	k3 = h*f(t+A[2]*h, u+B[2,0]*k1+B[2,1]*k2)
	k4 = h*f(t+A[3]*h, u+B[3,0]*k1+B[3,1]*k2+B[3,2]*k3)
	k5 = h*f(t+A[4]*h, u+B[4,0]*k1+B[4,1]*k2+B[4,2]*k3+B[4,3]*k4)
	k6 = h*f(t+A[5]*h, u+B[5,0]*k1+B[5,1]*k2+B[5,2]*k3+B[5,3]*k4+B[5,4]*k5)

	uAvg = u + CH[0]*k1 + CH[1]*k2 + CH[2]*k3 + CH[3]*k4 + CH[4]*k5 + CH[5]*k6 # Average
	# TE = np.absolute(CT[0]*k1 + CT[1]*k2 + CT[2]*k3 + CT[3]*k4 + CT[4]*k5 + CT[5]*k6) # Truncation Error
	# hnew = 0.9*h*(Tol/np.max(TE))**(1/5)
	uLow = 
	uHigh = 

	if np.max(TE) > Tol:
		return rk45(u, f, t, hnew, Tol)
	else:
		return uAvg

# Acceleration
def F(t, u):
	x, y, z, vx, vy, vz = u
	# vel = np.array([vx, vy, vz])
	ax, ay, az = np.array([0, -9.8, 0], dtype = np.float64)
	return np.array([vx, vy, vz, ax, ay, az])

def integrate_EOM(r0=np.array([0, 0, 0], dtype = np.float64), v0=np.array([10, 10, 0], dtype = np.float64), h=1):
	t = 0
	u = np.array([r0[0], r0[1], r0[2], v0[0], v0[1], v0[2]])
	uList = [[t, u[0], u[1], u[2], u[3], u[4], u[5]]]
	counter = 0
	MaxCount = 10000
	while (t < 2.04) and counter < MaxCount:
		t += h
		counter += 1
		u[:] = rk45(u, F, t, h)
		uList.append([t, u[0], u[1], u[2], u[3], u[4], u[5]])
	uArr = np.transpose(np.array([uList])) # transposed to make positions easier to grab.
	return uArr

