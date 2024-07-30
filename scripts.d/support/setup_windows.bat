@ECHO OFF

REM Synopsis
REM Name: setup_windows.bat
REM Description: Install servers.pvsc in %APPDATA%
REM Alternative: user can run the following commands a cmd terminal
REM              cd <SALOME installation directory>
REM              <SALOME installation directory>\W64\Python\python3.exe %out_dir_Path%\salome_hpc_visu_servers.py
REM

SET out_dir_Path=%~dp0

SET PYTHONIOENCODING=UTF_8
SET PYTHONPATH=
SET PYTHONPATH=%out_dir_Path%\W64\Python\lib;%PYTHONPATH%
SET PYTHONPATH=%out_dir_Path%\W64\Python\lib\site-packages;%PYTHONPATH%

SET PATH=%out_dir_Path%\W64\Python;%PATH%
SET PATH=%out_dir_Path%\W64\Python\libs;%PATH%
SET PATH=%out_dir_Path%\W64\Python\Scripts;%PATH%

START %out_dir_Path%\W64\Python\python3.exe %out_dir_Path%\salome_hpc_visu_servers.py
