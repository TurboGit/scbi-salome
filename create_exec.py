#!/usr/bin/python3
import sys
import paramiko

version_salome = sys.argv[1]
print("version_salome = %s"%version_salome)
exec_script = """
#!/bin/bash

salome="singularity exec /gpfsgaia/container/singularity/shared/salome/salome-%s-s11.sif /opt/salome/salome"
$salome $@"""%version_salome

with open("salome_remote_launcher", 'w') as f:
    f.writelines(exec_script)
