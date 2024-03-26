@ECHO OFF

REM Synopsis
REM Name: run_salome_shell.bat
REM Options: SALOME arguments if any
REM Description: runs the SALOME launcher shell session
REM Alternative: user can run the following commands a cmd terminal
REM              cd <SALOME installation directory>
REM              <SALOME installation directory>\W64\Python\python3.exe salome shell
REM

SET out_dir_Path=%~dp0

SET PYTHONIOENCODING=UTF_8
SET PYTHONPATH=
SET PYTHONPATH=%out_dir_Path%\W64\Python\lib;%PYTHONPATH%
SET PYTHONPATH=%out_dir_Path%\W64\Python\lib\site-packages;%PYTHONPATH%
SET PYTHONPATH=%out_dir_Path%\W64\sip\Lib\site-packages;%PYTHONPATH%
SET PYTHONPATH=%out_dir_Path%\W64\PyQt;%PYTHONPATH%
SET PYTHONPATH=%out_dir_Path%\W64\PyQt\lib\site-packages;%PYTHONPATH%

SET PATH=%out_dir_Path%\W64\Python;%PATH%
SET PATH=%out_dir_Path%\W64\Python\libs;%PATH%
SET PATH=%out_dir_Path%\W64\Python\Scripts;%PATH%
SET PATH=%out_dir_Path%\W64\pthreads\lib;%PATH%
SET PATH=%out_dir_Path%\W64\EXT\bin;%PATH%
SET PATH=%out_dir_Path%\W64\EXT\lib;%PATH%
SET PATH=%out_dir_Path%\W64\qt\bin;%PATH%
SET PATH=%out_dir_Path%\W64\sip\scripts;%PATH%
SET PATH=%out_dir_Path%\W64\PyQt\bin;%PATH%

START %out_dir_Path%\W64\Python\python3.exe %out_dir_Path%\salome shell %*
