import numpy as np

### Using geometrized units; c=G=1.

'''
Initial Velocity       c
BG Image Position      -100 m
Target Plane           100 m
Mass                   6.3419408698e9 m (=8.54e36 kg) Mass of Sagittarius A*. Note: Yes masses are in units of length here, so Rs=2M
'''

# Default Values
c = 1 # Speed of light
G = 1 # Gravitational constant
m = 6.3419408698e9 # Mass
Rs = 2*m # Schwarzschild Radius

# RK4
def rk4(u, f, t, h):
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
	TE = np.absolute(CT[0]*k1 + CT[1]*k2 + CT[2]*k3 + CT[3]*k4 + CT[4]*k5 + CT[5]*k6) # Truncation Error
	hnew = 0.9*h*(Tol/np.max(TE))**(1/5)
	#uLow = 
	#uHigh = 

	if np.max(TE) > Tol:
		return hnew, rk45(u, f, t, hnew, Tol)
	else:
		return hnew, uAvg

def rk4RE(u, f, t, h):
	p = 4
	eps_rel = 1e-6
	eps_abs = 1e-15
	# u1 using usual RK4 with two half-time steps
	u1 = rk4(u, f, t, h/2)
	u1 = u1 + rk4(u1, f, t, h/2)

	# u2 with one timestep
	u2 = rkt(u, f, t, h)

	lte = 2^p/(2^p-1)*np.abs(u1-u2) # Local truncation error (local error estimate)
	re = lte/(eps_rel*abs(u) + eps_abs)
	hnew = h/re^(1/(p+1)) # time step adjustment

	return hnew, rk4(u, f, t, hnew)

# Acceleration
def F(t, u):
	x, y, z, vx, vy, vz = u
	# vel = np.array([vx, vy, vz])
	ax, ay, az = np.array([0, -9.8, 0], dtype = np.float64)
	return np.array([vx, vy, vz, ax, ay, az])

# Equations of motion for the Schwarchild Metric
def F_schwarz(t, u): # Note, this takes in SPHERICAL COORDINATES and outputs them in SPHERICAL COORDINATES
	r, theta, phi, vr, vtheta, vphi = u
	# vel = np.array([vx, vy, vz])
	ar = -Rs/(2*r**2)*((L/r)**2)+((L**2)/(r**3))*(1-(Rs/r))
	atheta = 
	aphi = 0


	return np.array([vr, vtheta, vphi, ar, atheta, aphi])

# Using physics convention. Theta = polar angle [0,pi] (measured from z axis), Phi = Azimuthal angle [0,2*pi](measured AROUND z axis; in xy plane)
def cart2sph(x,y,z,vx,vy,vz):
	r = np.sqrt(x**2+y**2+z**2)
	theta = np.arccos(z/r)
	phi = np.sign(y)*np.arccos(x/np.sqrt(x**2+y**2))
	vr = (x*vx + y*vy + z*vz)/r
	vtheta = np.sum(np.array([vx,vy,vz])*np.array([np.cos(theta)*np.cos(phi),np.cos(theta)*np.sin(phi),-np.sin(theta)]))/r # come back and make these trigonometric functions into functions of x, y, z
	vphi = np.sum(np.array([vx,vy,vz])*np.array([-np.sin(phi),np.cos(phi),0]))/np.sqrt(x**2 + y**2)
	return r,theta,phi,vr,vtheta,vphi

def sph2cart(r,theta,phi,vr,vtheta,vphi=0):
	x = r*np.sin(theta)*np.cos(phi)
	y = r*np.sin(theta)*np.sin(phi)
	z = r*np.cos(theta)
	rho = r*np.sin(theta)
	vx = vr*np.sin(theta)*np.cos(phi) + r*vtheta*np.cos(theta)*np.cos(phi) - rho*vphi*np.sin(phi)
	vy = vr*np.sin(theta)*np.sin(phi) + r*vtheta*np.cos(theta)*np.sin(phi) + rho*vphi*np.cos(phi)
	vz = vr*np.cos(theta) - np.sin(theta)
	return x,y,z,vx,vy,vz

def integrate_EOM(r0=np.array([0, 0, 0], dtype = np.float64), v0=np.array([50, 50, 0], dtype = np.float64), h=1e-3):
	t = 0
	u = np.array([r0[0], r0[1], r0[2], v0[0], v0[1], v0[2]])
	uList = [[t, u[0], u[1], u[2], u[3], u[4], u[5]]]
	counter = 0
	MaxCount = 10000
	while (t < 10) and counter < MaxCount:
		t += h
		counter += 1
		h, u[:] = rk4(u, F, t, h)
		uList.append([t, u[0], u[1], u[2], u[3], u[4], u[5]])
	uArr = np.transpose(np.array([uList])) # transposed to make positions easier to grab.
	return uArr