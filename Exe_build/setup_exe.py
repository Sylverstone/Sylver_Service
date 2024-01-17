import sys
from cx_Freeze import setup, Executable

# Define the executables
executables = [Executable("../sylver_service.py", base=None)]


build_options = {
    "packages": ["pygame","os","datetime","sys","threading","keyboard","tkinter","mysql.connector","tkinter.filedialog","time","pyperclip"],
    "include_files": [
        ("../Image", "Image"),
        ("../Sylver_class_import.py", "Sylver_class_import.py"),
        ("../img_base","img_base"),
        ("../img_center","img_center"),
        ("../font","font"),
        ("../Ressource","Ressource"),
        ("../Resize_image.py","Resize_image.py"),
        ("../.env", ".env"),
    ],
}

# Set up the setup function
setup(
    name="sylver_service",
    version='v0.1.2',
    options={"build_exe": build_options},
    author = "by Sylvio Pelage-Maxime",
    executables=executables,
)