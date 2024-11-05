# Install MSYS2

   Go to: https://www.msys2.org/

   Download installer, run it and use all default values
   for installation.

# Setup MSYS2

   - Start a Bash shell `MSYS2 MINGW64`

   - Set proxy

```
     $ export http_proxy=
     $ export https_proxy=$http_proxy
     $ export no_proxy=
```

   - Add `$HOME/.local/bin` into the `PATH` variable

   - Those settings can be added at the bottom of ~/.bachrc
     later when an editor is installed.

# Package support with pacman

Some minimal examples to work with SALOME Windows.

- List all installed packages

```
  $ pacman --query
```

- List a package version

```
  $ pacman --query sed
```

- List packages version for all matching name

```
  $ pacman --query --search "perl*"
```

- Install a package

```
  $ pacman --sync sed
```

- Search some available packages

```
  $ pacman --sync --search sed
```

  This command will list all matches for <str>, we need to install
  only packages on the mingw64/ namespace.

# Install minimal toolset

```
   $ pacman --sync git
   $ pacman --sync vim
   $ pacman --sync make
   $ pacman --sync rsync
   $ pacman --sync patch
   $ pacman --sync diffutils
   $ pacman --sync mingw-w64-x86_64-emacs
   $ pacman --sync mingw-w64-x86_64-cmake
   $ pacman --sync mingw-w64-x86_64-gcc
   $ pacman --sync mingw-w64-x86_64-7zip
```

# Install scbi-salome

```
   $ cd $HOME
   $ mkdir dev
   $ cd dev
   $ git clone --recurse-submodule https://github.com/TurboGit/scbi-salome.git
   $ cd scbi-salome
   $ make
```

# Build SALOME

```
   $ scbi --env=mingw --color:dark --deps --flat s-salome
```

The needed MINGW packages will be displayed while building and will
require their installation.

To list all the needed OS dependencies and installing them first if
needed:

```
   $ scbi show --env=mingw --depends:full --externals:only s-salome
```

Only a limited set of modules are built at this point. The paraview
application is built and the modules LIBBATCH and KERNEL.
