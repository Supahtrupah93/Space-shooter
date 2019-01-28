import cx_Freeze
import os.path

executables = [cx_Freeze.Executable("Space Shooter.py")]

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

options = {
    'build_exe': {
        'include_files':[
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
         ],
    },
}


cx_Freeze.setup(
    name="Space shooter",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["Assets/enemy1 - 128.png", "Assets/enemy2 - 128.png",
                                            "Assets/enemy3 - 128.png", "Assets/quit prompt.png",
                                            "Assets/Shield.png","Assets/space.png","Assets/SpaceShip - 128.png"]}},
    executables = executables

    )