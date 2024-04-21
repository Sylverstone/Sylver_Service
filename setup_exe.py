
from cx_Freeze import setup, Executable
import platform,os

# Obtenez le nom du système d'exploitation
system_name = platform.system()
# Define the executables
if system_name != "Windows":
    executables = [Executable("sylver_service.py", base=None, icon=os.path.join("Image", "Logo_app_3.ico"))]
else:
    executables = [Executable("sylver_service.py", base="Win32GUI",icon=os.path.join("Image", "Logo_app_3.ico"))] # le cmd ne s'ouvra pas

build_options = {
    "packages": ["pygame","os","datetime","sys","threading","keyboard","tkinter","pymysql","tkinter.filedialog","time","pyperclip","math","io"],
    "include_files": [
        ("Image", "Image"),
        ("Sylver_class_import.py", "Sylver_class_import.py"),
        ("img_base","img_base"),
        ("image_user","image_user"),
        ("font","font"),
        ("Ressource","Ressource"),
        ("Resize_image.py","Resize_image.py"),
        (".env", ".env"),
        ("font_import.py","font_import.py"),
        ("Exception.py","Exception.py"),
        ("Color.py","Color.py"),
        ("Animation.py","Animation.py"),
        ("FCP3","FCP3"),
        ("Sylver_fonction_usuelle.py","Sylver_fonction_usuelle.py"),
        ("Sylver_filedialog.py","Sylver_filedialog.py")
    ],
}

# Set up the setup function
setup(
    name="Sylver.Service",
    version='v1.8.5',
    options={"build_exe": build_options},
    author = "by Sylvio PELAGE MAXIME",
    executables=executables,
)