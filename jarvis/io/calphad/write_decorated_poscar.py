"""
CALPHAD requies to fix symmetry during IBRION = 7 optimization
This module writes the POSCAR accordingly.
"""


from jarvis.analysis.structure.spacegroup import get_wyckoff_position_operators
from jarvis.io.vasp.inputs import Poscar
from jarvis.analysis.structure.spacegroup import Spacegroup3D
from collections import defaultdict
import numpy as np
from jarvis.core.atoms import Atoms
import glob
import os


def decorate_T_F(options=[], coord=[], tol=0.01):
    arr = []
    for ii, i in enumerate(coord):
        tmp = "T"
        for j in options:
            if isinstance(j[ii], float):
                if abs(float(j[ii]) - float(i)) < tol:
                    tmp = "F"
        #          print (j[ii], i, coord, 'F')
        arr.append(tmp)
    arr = " ".join(arr)
    # print ('def arr',arr)
    return arr


def get_selective_dyn_decorated_atoms(atoms):
    spg = Spacegroup3D(atoms=atoms)  # .spacegroup_data()
    frac_coords = atoms.frac_coords
    hall_number = spg._dataset["hall_number"]
    wdata = get_wyckoff_position_operators(hall_number)["wyckoff"]
    wsymbols = spg._dataset["wyckoffs"]
    info = defaultdict()
    for i in wdata:
        info[i["letter"]] = i["positions"]

    props = []
    count = 0
    for i, j in zip(wsymbols, frac_coords):
        ops = info[i]
        # print ('ops,j',ops, j)

        arr = ops
        new_arr = []
        for ii in arr:
            a = ii.split(",")
            b = []
            for jj in a:
                ind = jj
                if "(" in jj:
                    ind = jj.split("(")[1]  # .split(')')[0]
                if ")" in jj:
                    ind = jj.split(")")[0]  # .split(')')[0]
                # print (a,ind,j)
                if "/" in ind:
                    try:
                        ind = float(ind.split("/")[0]) / float(ind.split("/")[1])
                    except:
                        pass
                try:
                    ind = float(ind)
                except:
                    pass
                b.append(ind)

            new_arr.append(b)
        # print ('arr',arr)
        # print ('coord',j)
        # print ()
        arr_T_F = decorate_T_F(options=new_arr, coord=j)
        props.append(arr_T_F)
        # print ('new_arr',new_arr,j, arr_T_F)
        # print ()
        # print ()
        # print ()
    decorated_atoms = Atoms(
        lattice_mat=atoms.lattice_mat,
        elements=atoms.elements,
        coords=frac_coords,
        cartesian=False,
        props=props,
    )
    return decorated_atoms, hall_number, wsymbols

"""
if __name__ == "__main__":
    atoms = Poscar.from_file(
        "/rk2/knc6/ZenGen/VASP-CALCS/C14EndMembersCalculationSetup/AlAlAl/CONTCAR"
    ).atoms
    atoms = Poscar.from_file(
        "/rk2/knc6/ZenGen/VASP-CALCS/C14EndMembersCalculationSetup/TiTiFe/CONTCAR"
    ).atoms
    decorated_atoms, hall_number, wsymbols = get_selective_dyn_decorated_atoms(atoms)
    print(decorated_atoms, wsymbols, hall_number)
    # import sys
    # sys.exit()
    x = []
    for i in glob.glob(
        "/rk2/knc6/ZenGen/VASP-CALCS/C14EndMembersCalculationSetup/*/CONTCAR"
    ):
        print(i)
        atoms = Poscar.from_file(i).atoms
        decorated_atoms, hall_number, wsymbols = get_selective_dyn_decorated_atoms(
            atoms
        )
        print(decorated_atoms, hall_number, wsymbols)
        comm = str("bulk@") + str(i.split("/")[-3]) + "_" + str(i.split("/")[-2])
        back_cmd = str("cp ") + str(i) + str(" ") + str(i) + str("/CONTCAR.back")
        x.append(i)
        print(back_cmd, comm)
        print()

    for i in glob.glob(
        "/rk2/knc6/ZenGen/VASP-CALCS/Ti-Al-FeTau2NewRound_11-13-2019/*/CONTCAR"
    ):
        print(i)
        atoms = Poscar.from_file(i).atoms
        decorated_atoms, hall_number, wsymbols = get_selective_dyn_decorated_atoms(
            atoms
        )
        print(decorated_atoms, hall_number, wsymbols)
        comm = str("bulk@") + str(i.split("/")[-3]) + "_" + str(i.split("/")[-2])
        back_cmd = str("cp ") + str(i) + str(" ") + str(i) + str("/CONTCAR.back")
        print(back_cmd, comm)
        print()
        x.append(i)
    # print (hall_number, wdata)
    print(len(x))
"""
