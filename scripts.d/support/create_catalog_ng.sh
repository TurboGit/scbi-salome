#! /bin/bash

function addToCatalog()
{
    local xml=$1
    local name=$2
    local hostname=$3
    local appliPath=$4
    local workingDirectory=$5

    local Catalog

    case $name in
        localhost)
            declare -A Catalog=(["name"]=\"$name\"
                                ["hostname"]=\"$name\")
            ;;
        *)
            declare -A Catalog=(["name"]=\"$name\"
                                ["hostname"]=\"$hostname\"
                                ["appliPath"]=\"$appliPath\"
                                ["workingDirectory"]=\"$workingDirectory\"
                                ["type"]=\""cluster"\"
                                ["protocol"]=\""ssh"\"
                                ["iprotocol"]=\""srun"\"
                                ["canLaunchBatchJobs"]=\""true"\"
                                ["canRunContainers"]=\""false"\"
                                ["batch"]=\""slurm"\"
                                ["mpi"]=\""no mpi"\"
                                ["userName"]=\""$USER"\")
            ;;
    esac

    {
        echo -n "<machine"
        for att in ${!Catalog[@]}; do
            echo -n " $att=${Catalog[$att]}"
        done
        echo "/>"
    } >> $xml
}

SALOME_ROOT=$(cd $(dirname ${BASH_SOURCE[0]});pwd)
XMLFILE=$SALOME_ROOT/CatalogResources.xml
VERSION="<salome_version>"

declare -A SERVER=(["gaia"]="/projets/salome/logiciels/salome/$VERSION"
                   ["cronos"]="/software/rd/salome/logiciels/salome/$VERSION")

declare -A USERHOME=(["gaia"]="/scratch/$USER"
                     ["cronos"]="/scratch/users/$USER")

echo "<resources>" > $XMLFILE

for name in ${!SERVER[@]}; do
    VIRTUAL_APPLI="${USERHOME[$name]}/$VERSION"
    ORIG_APPLI="${SERVER[$name]}/"

    ssh -o StrictHostKeyChecking=no $USER@$name.hpc.edf.fr \
        "mkdir -p $VIRTUAL_APPLI && \
         rm -rf $VIRTUAL_APPLI/* && \
         ln -sr $ORIG_APPLI/salome $VIRTUAL_APPLI/salome" >/dev/null 2>&1

    if [[ $? = 0 ]]; then
        addToCatalog $XMLFILE "$name" "$name.hpc.edf.fr" \
                     "$VIRTUAL_APPLI/salome" "${USERHOME[$name]}/workingdir"
    else
        echo "CREATE_CATALOG - WARNING - $name configuration failed!"
        echo "Verify your acces rights to $name.hpc.edf.fr and try again."
    fi
done

addToCatalog $XMLFILE "localhost"
echo "</resources>" >> $XMLFILE

BINDIR=$(basename $(ls -1d $SALOME_ROOT/BINARIES-*))
[[ -d $SALOME_ROOT/$BINDIR/KERNEL/share/salome/resources/kernel ]] &&
    cp $XMLFILE $SALOME_ROOT/$BINDIR/KERNEL/share/salome/resources/kernel
