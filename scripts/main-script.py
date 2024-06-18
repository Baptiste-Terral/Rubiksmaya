import sys
import importlib

# Add the path to your scripts folder
script_path = r"C:\Users\bapti\Desktop\Documents\Scolarite\EiCnam\1ere_annee\scripts-python-animation\Rubiksmaya\scripts"
if script_path not in sys.path:
    sys.path.append(script_path)

# Reload the module if it is already loaded
module_name = 'ui_generation'
if module_name in sys.modules:
    importlib.reload(sys.modules[module_name])
else:
    from ui_generation import show_ui

# Call the function to show the UI
show_ui()
