from __future__ import print_function

import mceq_config as config
from MCEq.core import MCEqRun
import crflux.models as pm
import numpy as np

def format_8_digits(a_list):
    return ["%.8e" % member for member in a_list]

config.debug_level = 1
config.kernel_config = 'numpy'
config.cuda_gpu_id = 0
if config.has_mkl:
    config.set_mkl_threads(2)


mceq = MCEqRun(
    interaction_model='SIBYLL23C',
    theta_deg=0.,
    primary_model=(pm.HillasGaisser2012, 'H3a'))


def test_config_and_file_download():
    import mceq_config as config
    import os
    # Import of config triggers data download
    assert config.mceq_db_fname in os.listdir(config.data_dir)



def test_some_angles():

    nmu = []
    for theta in [0., 30., 60., 90]:
        mceq.set_theta_deg(theta)
        mceq.solve()
        nmu.append(
            np.sum(
                mceq.get_solution('mu+', mag=0, integrate=True) +
                mceq.get_solution('mu-', mag=0, integrate=True)))
    assert format_8_digits(nmu), ['5.62504370e-03', '4.20479234e-03', '1.36630552e-03', '8.20255259e-06']


def test_switch_interaction_models():
    mlist = [
        'DPMJETIII191',
        'DPMJETIII306',
        'QGSJET01C',
        'QGSJETII03',
        'QGSJETII04',
        'SIBYLL21',
        'SIBYLL23',
        'SIBYLL23C03',
        'SIBYLL23C',
        'SIBYLL23CPP']
    count_part = []
    for m in mlist:
        mceq.set_interaction_model(m)
        count_part.append(len(mceq._particle_list))
    assert(count_part == [64, 64, 58, 44, 44, 48, 62, 62, 62, 62])


def test_single_primary():
    energies = [1e3, 1e6, 1e9, 5e10]
    nmu, nnumu, nnue = [], [], []
    mceq.set_interaction_model('SIBYLL23C')
    mceq.set_theta_deg(0.)
    for e in energies:
        mceq.set_single_primary_particle(E=e, pdg_id=2212)
        mceq.solve()
        nmu.append(
            np.sum(
                mceq.get_solution('mu+', mag=0, integrate=True) +
                mceq.get_solution('mu-', mag=0, integrate=True)))
        nnumu.append(
            np.sum(
                mceq.get_solution('numu', mag=0, integrate=True) +
                mceq.get_solution('antinumu', mag=0, integrate=True)))
        nnue.append(
            np.sum(
                mceq.get_solution('nue', mag=0, integrate=True) +
                mceq.get_solution('antinue', mag=0, integrate=True)))
    assert format_8_digits(nmu) == ['2.03134720e+01', '1.20365838e+04', '7.09254150e+06', '2.63982133e+08']
    assert format_8_digits(nnumu) == ['6.80367347e+01', '2.53158948e+04', '1.20884925e+07', '4.14935240e+08']
    assert format_8_digits(nnue) == ['2.36908717e+01', '6.91213253e+03', '2.87396649e+06', '9.27683105e+07']

