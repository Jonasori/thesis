"""Scratch code for Section 3"""

import os
import numpy as np
import subprocess as sp
import astropy.units as u
import astropy.constants as const
from pathlib2 import Path


# Constants
h = 6.626 * 1e-27 # erg s
c = 3e10 # cm/s
k = 1.38 * 1e-16 # erg/K
g2mearth = 5.92 * 1e27 # g/mEarth
g2mjup = 1.898 * 1e30 # g/mEarth
g2msol = 2 * 1e33   # g/mSol

Path.cwd()




def get_fluxed():
    os.chdir('/Volumes/disks/jonas/modeling')
    from tools import imstat_single

    im = 'data/hco/hco-short110_moment0'
    rms = imstat_single(im)[1] # 0.0294
    call_str = "cgcurs in={},{} device=/xs type=both slev=a,{} levs=3 options=stats region=arcsec,box'(-2,-2,2,2)'".format(im + '.cm', im + '.cm', rms)
    def miriad_caller(call_str):
        call_list = call_str.split(' ')
        l = sp.check_output(call_list)
        # l2 = list(filter(None, l.decode("utf-8").split('\n')))
        l2 = filter(None, l.split('\n'))
        stats = []
        for row in l2:
            if list(filter(None, row.split(' ')))[0] == 'Sum':
                stats.append(list(filter(None, row.split(' '))))

        # nums = []
        # for stat in stats:
        #     try:
        #         nums.append(int(stat))
        #     except ValueError:
        #         pass

        return stats

print(rms)

get_fluxed()

h = const.h.decompose()
c = const.c.decompose()
k = const.k_B.decompose()
hbar = const.hbar.decompose()




def get_mass():
    """
    Calculate gas mass of a disk from its flux in cgs.
            Sources:
                - F: Convert cgcurs output (6.x) from Jy km/s by multiplying by
                        [1e-23 erg/(cm2 s Hz) Hz][nu0/(c km/s) * 1e5 (cm s-1/km s-1)] (nu0/c)
                - A_ul: Einstein A, HCO+(4-3) (listed as 5-4 trans bc indexing is bad)
                        https://home.strw.leidenuniv.nl/~moldata/datafiles/hco+@xpol.dat
                - T: Excitation temperature from Factor et al (2017)
                - B0: From wiki: B = k = E/(hbar c = hc/2pi) -> k (hc) = 2pi E
                    - Unclear whether this should use E = (E0 = 0.0297) or E = (E_43 = 29.75) cm-1
                        - Both from hcoplus.dat and
                        https://home.strw.leidenuniv.nl/~moldata/datafiles/hco+@xpol.dat
                - m: molecular weight (g/mol), divided by Avagadro -> g
                    - weight: 29, from https://home.strw.leidenuniv.nl/~moldata/datafiles/hco+@xpol.dat
        """

    # Disk-specifics
    Aul = 3.63 * 1e-3 # Hz
    B0 = 2 * np.pi * 0.0297 # 29.75
    B0 = 1.488  # cm s-1
    T = 27 # K
    # T = 32 # K
    d = 389 * 3.086e+18 # cm

    # Line-specifics
    proton_mass = 1.67e-24 # g, from http://www.astro.wisc.edu/~dolan/constants.html
    m = 29. * proton_mass  #g
    nu0 = 356.73 * 1e9 # Hz
    J = 4

    F_integrated = 4.13 # Jy km s-1
    F = F_integrated * (10**-23) * (1e5) * (nu0/c) # erg cm-2 s-1 Hz-1 Hz


    Xu_exp = ((-B0 * J * (J + 1) * h * c) /(k * T))
    Xu_coeff = ((2 * J + 1) / (k * T/(h * c * B0)))

    Xu = Xu_coeff * np.exp(Xu_exp)

    m_gas = (4 * np.pi/(h * nu0) ) * (F * m * d**2 / (Aul * Xu))
    # m_gas /= 1e-8   # Scale by X_hco to get total mass
    m_gas_mearth = m_gas/g2mearth
    m_gas_mjup = m_gas/g2mjup
    m_gas_msol = m_gas/g2msol

    m_gas_msol
    m_gas_mearth

    print("M (mSol): ", m_gas_msol)
    print("M (mJup): ", m_gas_mjup)
    print("M (mEarth): ", m_gas_mearth)
    print("Using X_HCO = 1e-8.2, inferred total disk mass (mSol): ", m_gas_msol /(2 * 10**(-10)))
    # return m_gas_msol


get_mass()

m_williams = 0.072

1.7187e-11 / m_williams


1.81e-8/(10**(-8.2))







def list_to_latex(s):
    l = list(filter(None, s.split(" ")))
    s = '$ ' + l[0] + '_{' + l[1] + '}^{+' + l[2] + '}$  & $' + l[3]
    return s


list_to_latex('134 -17  17   134')







# The End
