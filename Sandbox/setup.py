from cx_Freeze import setup, Executable

base = None    

executables = [Executable("MANTABrowser.py", base=base)]

packages = ["idna", "cv2", "numpy", "json", "os"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "MANTABrowser",
    options = options,
    version = "0.1",
    description = 'Browse MANTA images',
    executables = executables
)