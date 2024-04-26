import numpy as np
from inputVariables import *
from numba import njit

# RK4
@njit
def rk4(u, t, h, E, L):
	# Equations of motion for the Schwarchild Metric
	def F_schwarz(t, u, E, L): # Note, this takes in SPHERICAL COORDINATES and outputs them in SPHERICAL COORDINATES
		r, theta, phi, vr, vtheta, vphi = u
		# vel = np.array([vx, vy, vz])
		vtheta = 0
		vphi = L/(r**2)
		ar = -Rs/(2*r**2)*((L/r)**2)+((L**2)/(r**3))*(1-(Rs/r))
		atheta = 0
		aphi = 0
		return np.array([vr, vtheta, vphi, ar, atheta, aphi], dtype = np.float64)
	k1 = F_schwarz(t, u, E, L)
	k2 = F_schwarz(t + 0.5*h, u + 0.5*h*k1, E, L)
	k3 = F_schwarz(t + 0.5*h, u + 0.5*h*k2, E, L)
	k4 = F_schwarz(t + h, u + h*k3, E, L)
	return u + h/6 * (k1 + 2*k2 + 2*k3 + k4)

# Richardson Extrapolation using RK4 with a full time step and two half time steps.
# [This one works!]
def rk4RE(u, t, h, E, L):
	p = 4
	eps_rel = 1e-7
	eps_abs = 1e-15
	# u1 using usual RK4 with two half-time steps

	u1 = rk4(u, t, h/2, E, L)
	u1 = rk4(u1, t+h/2, h/2, E, L)

	# u2 with one timestep
	u2 = rk4(u, t, h, E, L)

	lte = 2**p/(2**p-1)*np.abs(u1-u2) # Local truncation error (local error estimate)
	re = lte/(eps_rel*np.abs(u) + eps_abs)
	re = np.max(np.where(re==0, 1, re)) # Replace zeros with ones to avoid division by zero
	hnew = h/re**(1/(p+1)) # time step adjustment

	if np.max(re)>2:
		return rk4RE(u, t, hnew, E, L)
	else:
		return hnew, rk4(u, t, hnew, E, L)

# Using physics convention. Theta = polar angle [0,pi] (measured from z axis), Phi = Azimuthal angle [0,2*pi](measured AROUND z axis; in xy plane)
@njit
def cart2sph(x=0,y=0,z=0,vx=0,vy=0,vz=0):
	r = np.sqrt(x**2+y**2+z**2)
	theta = np.arccos(z/r)
	phi = np.arctan2(y,x)
	rho = np.sqrt(x**2+y**2)
	sinTheta = rho/r
	cosTheta = z/r
	sinPhi = y/rho
	cosPhi = x/rho
	vr = (x*vx + y*vy + z*vz)/r
	vtheta = (vx*cosTheta*cosPhi + vy*cosTheta*sinPhi - vz*sinTheta)/r
	vphi = (-vx*sinPhi + vy*cosPhi)/rho
	return r,theta,phi,vr,vtheta,vphi

@njit
def sph2cart(r=0,theta=0,phi=0,vr=0,vtheta=0,vphi=0):
	x = r*np.sin(theta)*np.cos(phi)
	y = r*np.sin(theta)*np.sin(phi)
	z = r*np.cos(theta)
	rho = r*np.sin(theta)
	vx = vr*np.sin(theta)*np.cos(phi) + r*vtheta*np.cos(theta)*np.cos(phi) - rho*vphi*np.sin(phi)
	vy = vr*np.sin(theta)*np.sin(phi) + r*vtheta*np.cos(theta)*np.sin(phi) + rho*vphi*np.cos(phi)
	vz = vr*np.cos(theta) - r*vtheta*np.sin(theta)
	return x,y,z,vx,vy,vz

@njit
def rotX(V,angle): # Rotate about x axis by angle. Takes in V=[x,y,z]
	xrot = V[0]
	yrot = V[1]*np.cos(angle)-V[2]*np.sin(angle)
	zrot = V[1]*np.sin(angle)+V[2]*np.cos(angle)
	return np.array([xrot, yrot, zrot], dtype = np.float64)

@njit
def A(r):
	return 1-(2*M/r)

# EOM. traj=0 keeps trajectory be default, traj=1 only keeps the last two points.
def integrate_EOM(r0=np.array([-100, 0, 0], dtype = np.float64), v0=np.array([1, 0, 0], dtype = np.float64), traj=0, Bound = np.array([200,200,200]),h=1): # Takes in CARTESIAN positions and velocities (also returns these in CARTESIAN)
	if traj !=0 and traj !=1:
		print("Invalid trajectory option! Please input 0 to save whole trajectory and 1 to keep the last two points.")
	t = 0
	# Re-frame problem to solve in the correct plane.
	uList = [[t, r0[0], r0[1], r0[2], v0[0], v0[1], v0[2]]]
	if r0[2] != 0:
		rotateBy = np.arctan2(r0[2],r0[1])#-(np.pi/2)
		r0rot = rotX(r0,-rotateBy)
	else:
		rotateBy = 0
		r0rot = r0

	sphICs = cart2sph(r0rot[0],r0rot[1],r0rot[2],v0[0],v0[1],v0[2]) # For FIXED ICs, [r, theta, phi, vr, vtheta, vphi]
	u = np.array(sphICs)
	counter = 0
	MaxCount = 10000
	L = (sphICs[0]**2)*(sphICs[5])
	E = np.sqrt(sphICs[3]**2 + A(sphICs[0])*((L/sphICs[0])**2))

	while (u[0] > Rs) and (np.abs(sph2cart(u[0],u[1],u[2])[0])<Bound[0]) and (np.abs(sph2cart(u[0],u[1],u[2])[1])<Bound[1]) and (np.abs(sph2cart(u[0],u[1],u[2])[2])<Bound[2]) and counter < MaxCount:
		counter += 1
		if traj == 1: # Save previous point
			uRotBackPosA = rotX(sph2cart(u[0],u[1],u[2],u[3],u[4],u[5])[0:3],rotateBy)
			uRotBackVelA = rotX(sph2cart(u[0],u[1],u[2],u[3],u[4],u[5])[3:6],rotateBy)
			uList[:] = [[t, uRotBackPosA[0], uRotBackPosA[1], uRotBackPosA[2], uRotBackVelA[0], uRotBackVelA[1], uRotBackVelA[2]]]

		h, u[:] = rk4RE(u, t, h, E, L)
		t += h

		uRotBackPosB = rotX(sph2cart(u[0],u[1],u[2],u[3],u[4],u[5])[0:3],rotateBy)
		uRotBackVelB = rotX(sph2cart(u[0],u[1],u[2],u[3],u[4],u[5])[3:6],rotateBy)
		uList.append(np.concatenate(([t],uRotBackPosB,uRotBackVelB)))

	uArr = np.transpose(np.array([uList])) # transposed to make positions easier to grab.
	return uArr # [t, x, y, z, vx, vy, vz]