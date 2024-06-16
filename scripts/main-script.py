import sys

sys.path.append(r"E:\Scolarite\EiCnam\1ere_annee\scripting-python-animation\projet")

for mod in list(sys.modules.keys()):
    if "scripts" in mod:
	    del sys.modules[mod]

from scripts.cubie_generation import main

# Size of the cube
cube_size = 3

cube_names = main(cube_size)
