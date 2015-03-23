from i2clibraries import i2c_hmc5883l

import time

while True:
	HMC = i2c_hmc5883l.i2c_hmc5883l(1)

	HMC.setContinuousMode()
	HMC.setDeclination(2,6)

	print (HMC)
	print (HMC.getDeclination())
	print (HMC.getHeading())
	print


	time.sleep(1)
