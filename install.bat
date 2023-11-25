@echo off

REM Télécharger get-pip.py
echo Téléchargement de get-pip.py...
powershell -Command "Invoke-WebRequest https://bootstrap.pypa.io/get-pip.py -OutFile get-pip.py"

REM Installer pip
echo Installation de pip...
python get-pip.py

REM Vérifier si pip a été installé avec succès
pip --version
if %ERRORLEVEL% neq 0 (
    echo L'installation de pip a échoué.
    exit /b %ERRORLEVEL%
)
