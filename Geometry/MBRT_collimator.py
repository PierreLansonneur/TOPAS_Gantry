#########################################################
# 	write the MBRT collimator TOPAS file 
#########################################################

import numpy as np

Rmax 	= 52	# Collimator radius in mm (= Ge/Snout/BrassCone3/RMin1 cm)
TTransZ = -140 	# true Z position in mm  (= -DCI)
TransZ 	= 129 	# Z position in mm  (= Ge/Snout/BrassCone3/TransZ cm)
slit 	= 0.1 	# slit width in mm
ctc 	= 4. 	# c-t-c in mm

def create_colliMBRT(Rmax,TransZ,TTransZ,slit,ctc):
        """
        create the collimator file
        """
	DMC = np.abs(-2000-TTransZ) 	                # Distance Magnets center to Collimator MBRT in mm. Magnets at -200 cm, collimator at TransZ
	N = int(2*(Rmax-1)/ctc)-2	                # Number of slits
	Displacement = np.linspace(-N*ctc/2,N*ctc/2,N+1)# slits position in mm
	thetas = np.degrees(np.arctan(Displacement/DMC))# slits angle in deg
	h=0.9*Rmax*np.sin(np.arccos(Displacement/Rmax)) # slits height in mm

	with open('./Aperture_MBRT_ctc{0}mm_width{1}um.txt'.format(ctc,1000*slit), 'w') as f:
		f.write('##################################################\n')
		f.write('# Collimator MBRT\n')
		f.write('##################################################\n\n')

		f.write('s:Ge/Aperture/Parent 	= "Snout"\n')
		f.write('s:Ge/Aperture/Type   	= "TsCylinder"\n')
		f.write('b:Ge/Aperture/IsParallel = "True"\n')
		f.write('s:Ge/Aperture/Material 	= "Brass"\n')
		f.write('d:Ge/Aperture/RMax  	= {0} cm \n'.format(0.1*Rmax))
		f.write('d:Ge/Aperture/thickness	= 6.5 cm\n')
		f.write('d:Ge/Aperture/HL    	= 0.5 * Ge/Aperture/thickness cm\n')
		f.write('d:Ge/Aperture/TransZ	= {0} cm\n'.format(0.1*TransZ))
		f.write('d:Ge/Aperture/RotZ	= 90 deg\n')
		f.write('#######\n\n')

		for i in range(N+1):
			f.write('s:Ge/H{0}/Parent   	= "Aperture"\n'.format(i))
			f.write('s:Ge/H{0}/Type     	= "G4Para"\n'.format(i))
			f.write('s:Ge/H{0}/Material 	= "Air"\n'.format(i))
			f.write('b:Ge/H{0}/IsParallel 	= "True"\n'.format(i))
			f.write('d:Ge/H{0}/TransX 		= {1} mm\n'.format(i,Displacement[i]))
			f.write('d:Ge/H{0}/HLX 	 	= {1:.2f} mm\n'.format(i,slit/2.))
			f.write('d:Ge/H{0}/HLY 	 	= {1} mm\n'.format(i,h[i]))
			f.write('d:Ge/H{0}/HLZ 	 	= 0.5 * Ge/Aperture/thickness cm\n'.format(i))
			f.write('d:Ge/H{0}/Alpha 	 	= 0 deg\n'.format(i))
			f.write('d:Ge/H{0}/Theta 	 	= {1} deg\n'.format(i,thetas[i]))
			f.write('d:Ge/H{0}/Phi 	 	= 0 deg\n\n'.format(i))

	print 'file saved succesfully!'

create_colliMBRT(Rmax,TransZ,TTransZ,slit,ctc)

