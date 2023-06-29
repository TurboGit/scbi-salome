#!/bin/bash

export out_dir_Path=$(cd $(dirname ${BASH_SOURCE[0]});pwd)
export PRODUCT_ROOT_DIR="${out_dir_Path}"

# PRODUCT environment
export SALOME_trace="local"
export SALOME_MODULES="SHAPER,SHAPERSTUDY,GEOM,SMESH,PARAVIS,YACS,JOBMANAGER"
export PYTHONIOENCODING="UTF_8"
export SALOME_MODULES_ORDER="SHAPER:SHAPERSTUDY:GEOM:SMESH"
export ROOT_SALOME_INSTALL="$PRODUCT_ROOT_DIR"
export SALOME_ON_DEMAND="HIDE"

while read F; do
    source $F
done < <(find $out_dir_Path/extra.env.d/ -type f -name "[0-9]*.sh" | sort -V)
