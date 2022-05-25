#! /bin/bash

function remove()
{
    local OLDPATH=$1

    [[ -L $OLDPATH ]] && unlink $OLDPATH
    [[ -e $OLDPATH ]] && rm -rf $OLDPATH
}

function create_link()
{
    local SRC=$1
    local DST=$2

    remove $DST
    ln -s $SRC $DST
}

PYTHONPATH_COMMON=$1
APPLI_DIR=$2

mkdir -p $PYTHONPATH_COMMON

PYTHONPATHS_SRC=()

while read P; do
    PYTHONPATHS_SRC+=($P)
done < <(source $APPLI_DIR/env_launch.sh; echo $PYTHONPATH |tr ':' '\n')

for p in ${PYTHONPATHS_SRC[*]}; do
    file_list=($p/*)

    for f in ${file_list[*]};do
        if [[ $f == *"easy-install.pth"* ]]; then
            cat $f >>$PYTHONPATH_COMMON/easy-install.pth
        else
            create_link $f $PYTHONPATH_COMMON/$(echo $f | awk -F "/" '{print $NF}' )
        fi
    done
done

read SP< <(source $APPLI_DIR/env_launch.sh;python -c "import setuptools,os
try:
  setup_tools_path = os.path.dirname(setuptools.__file__)
except AttributeError:
  setup_tools_path = os.path.dirname(setuptools.__path__._path[0])
del setuptools
site_patch = os.path.join(setup_tools_path, 'site-patch.py')
print(site_patch)")

remove $PYTHONPATH_COMMON/site.py
cp $SP $PYTHONPATH_COMMON/site.py

cp $APPLI_DIR/salome $APPLI_DIR/salome_init

sed -i '/addToPythonPath/d' $APPLI_DIR/salome

sed -i '/runSalome/i \    context.setVariable(r\"PYTHONPATH\", r\"'$PYTHONPATH_COMMON'\", overwrite=True)' $APPLI_DIR/salome
