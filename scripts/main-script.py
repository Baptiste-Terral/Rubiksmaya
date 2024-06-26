import sys
import importlib

# Add the path to your scripts folder
script_path = r"C:\Users\bapti\Desktop\Documents\Scolarite\EiCnam\1ere_annee\scripts-python-animation\Rubiksmaya\scripts"
sys.path.append(script_path)

modules_to_reload = ['rotations', 'ui_generation', 'cubie_generation']
for module_name in modules_to_reload:
    if module_name in sys.modules:
        importlib.reload(sys.modules[module_name])
    else:
        importlib.import_module(module_name)	    
	    
from ui_generation import show_ui

# Call the function to show the UI
show_ui()
