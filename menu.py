# MagicTools
toolbar = nuke.menu('Nodes')
MagicMenu = toolbar.addMenu('MagicTools', icon='MagicTools.png')
MagicMenu.addCommand('MagicDefocus', 'nuke.createNode("MagicDefocus")')

PluginsMenu = toolbar.addMenu('PluginsMenu')
PluginsMenu.addCommand('Expoglow', 'nuke.createNode("expoglow")')
PluginsMenu.addCommand('aPMatte', 'nuke.createNode("aPMatte")')
PluginsMenu.addCommand('ReProject3D', 'nuke.createNode("ReProject3D")')
PluginsMenu.addCommand('ArriLensDistortion', 'nuke.createNode("ArriLensDistortion")')
PluginsMenu.addCommand('apChroma', 'nuke.createNode("apChroma")')

import nuke
import sys
from PySide2.QtWidgets import QApplication

# Ajouter le chemin vers ton script PySide2
script_path = r'C:\Users\Elie\.nuke\ElieAssistant_v001.py'

def show_script_manager():
    # Initialiser l'application Qt
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    # Importer et exécuter le script
    import importlib.util
    spec = importlib.util.spec_from_file_location("NukeScriptManager", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Créer et afficher la fenêtre
    window = module.NukeScriptManager()
    window.show()



# Ajouter une entrée de menu dans Nuke
nuke.menu('Nuke').addCommand('Custom/Eli-ssistant', show_script_manager)

# Importer la fonction show_elie_stockshot depuis ElieStockshot.py
from ElieStockshot import open_mytool
nuke.menu('Nuke').addCommand('Custom/Eli-brary', 'open_mytool()')

# Importer la fonction show_elie_stockshot depuis ElieStockshot.py
from Elissimo import open_mytool_Elissimo
nuke.menu('Nuke').addCommand('Custom/Eli-ssimo', 'open_mytool_Elissimo()')



''' Add this to your menu.py '''


toolbar = nuke.menu("Nodes")
m = toolbar.addMenu("GS_Tools", icon="GS_Icon.png")
m_Caustics = m.addMenu("Caustics",icon="Caustics_Icon.png")

m_Caustics.addCommand("Caustics", "nuke.createNode(\"GS_Caustics\")", icon="Caustics_Icon.png")
