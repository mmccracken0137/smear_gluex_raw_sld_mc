#!/usr/bin/env python
'''
This code smears the raw MC generated in Lottie block form.
Run as
     python mc_smear.py <raw_mc_dir>

The final-state momentum 3-vectors are smeared by generating a multiplicative
magnitude factor from a gaussian with mean 1.0 and a width set with the
smear_fac variable below.

Theta and phi angles are smeared by 10 mrad.

The initial-state photon momentum is smeared with a separate gamma_smear
variable.
'''

import sys, os
import math
import numpy as np
from ROOT import TVector3

smear_fac = 0.02
theta_smear_fac = 0.010 # rad
phi_smear_fac = 0.010 # rad
gamma_smear = 0.03

files = os.listdir(sys.argv[1])

dname = sys.argv[1]
#odname = sys.argv[2]
#for i in range(len(odname)):
#    if odname[i] == "raw":
#        odname[i] = "smear"

#odname = '_'.join(str(e) for e in odname)

odname = "../smeared_mc/"

pvec = TVector3()

print(odname)

for f in files:
    #if "000" not in f:
    #    continue

    of = odname + "/p" + str(smear_fac) + "::g" + str(gamma_smear) + "_" + f
    of = of.split("_")
    for i in range(len(of)):
        if of[i] == "raw":
            of[i] = "smear"
    of = '_'.join(str(e) for e in of)

    print(dname + "/" + f, "r")
    print(of)
    fil  = open(dname + "/" + f, "r")
    #ofil = open(odname + "/" + of, "w")
    ofil = open("./" + of, "w")
    lin = fil.readline()
    lin_list = lin.split(None)

    while len(lin) > 0:
        if len(lin_list) == 4:
            fac = np.random.randn()*gamma_smear + 1
            lin_list[2] = round(float(lin_list[2])*fac,5)
            lin = ' '.join(str(e) for e in lin_list) + "\n"
        elif len(lin_list) == 8:
            fac = np.random.randn()*smear_fac + 1
            pvec.SetXYZ(float(lin_list[5])*fac, float(lin_list[6])*fac, float(lin_list[7])*fac)
            theta_term = np.random.randn()*theta_smear_fac
            phi_term = np.random.randn()*phi_smear_fac
            pvec.SetTheta(pvec.Theta() + theta_smear_fac)
            pvec.SetPhi(pvec.Theta() + phi_smear_fac)
            lin_list[5] = round(pvec.X(),5)
            lin_list[6] = round(pvec.Y(),5)
            lin_list[7] = round(pvec.Z(),5)

            lin = ' '.join(str(e) for e in lin_list) + "\n"

        ofil.write(lin)

        lin = fil.readline()
        lin_list = lin.split(None)

    fil.close()
    ofil.close()
