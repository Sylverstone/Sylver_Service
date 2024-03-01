import sys
from cx_Freeze import setup, Executable
import platform,os

# Obtenez le nom du système d'exploitation
system_name = platform.system()

# Define the executables
if system_name != "Windows":
    executables = [Executable("sylver_service.py", base=None, icon=os.path.join("Image", "Logo_app.ico"))]
else:
    executables = [Executable("sylver_service.py", base="Win32GUI",icon=os.path.join("Image", "Logo_app.ico"))] # le cmd ne s'ouvra pas

build_options = {
    "packages": ["pygame","os","datetime","sys","threading","keyboard","tkinter","pymysql","tkinter.filedialog","time","pyperclip"],
    "include_files": [
        ("Image", "Image"),
        ("Sylver_class_import.py", "Sylver_class_import.py"),
        ("img_base","img_base"),
        ("img_center","img_center"),
        ("font","font"),
        ("Ressource","Ressource"),
        ("Resize_image.py","Resize_image.py"),
        (".env", ".env"),
        ("desktop.ini","desktop.ini")
    ],
}

# Set up the setup function
setup(
    name="sylver_service",
    version='v1.3',
    options={"build_exe": build_options},
    author = "by Sylvio PELAGE MAXIME | Elvann JOLIVEL | Deecleane CORALIE",
    executables=executables,
)