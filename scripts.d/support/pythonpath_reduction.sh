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
    file_list=$(ls $p/ 2>/dev/null)

    for f in ${file_list[*]};do
        f_name=$f
        f=$p/$f
        if [[ $f_name == "easy-install.pth" ]]; then
            cat $f >>$PYTHONPATH_COMMON/easy-install.pth
        elif [[ $f_name == "salome" ]] && [[ -d $f ]]; then
            salome_file_list=$(ls $f/ 2>/dev/null)
            mkdir -p $PYTHONPATH_COMMON/salome

            for ff in ${salome_file_list[*]}; do
                ff_name=$ff
                ff=$f/$ff
                create_link $ff $PYTHONPATH_COMMON/salome/$ff_name
            done
        else
            create_link $f $PYTHONPATH_COMMON/$f_name
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

sed -i '/runSalome/i \    context.setVariable(r\"PYTHONPATH\", r\"'$PYTHONPATH_COMMON'\", overwrite=True)' $APPLI_DIR/salome
