# scbi-salome

Setup Configure Build Install - Scripts for building SALOME

# Pre-requisite

  First you need to install the scbi driver.

  https://github.com/TurboGit/scbi

# Install

```
$ git clone https://gitlab.pleiade.edf.fr/pascal.obry/scbi-salome.git
$ cd ./scbi-salome.git
$ make
```

# A simple tutorial to build SALOME

  This is still work-in-progress and only Paraview can be built at this
  stage. The other scripts are not yet done.

```
$ scbi -p --deps salome
```
