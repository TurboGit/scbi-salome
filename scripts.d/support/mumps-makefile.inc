#
#  This file is part of MUMPS 4.10.0, built on Tue May 10 12:56:32 UTC 2011
#
#Begin orderings

# NOTE that PORD is distributed within MUMPS by default. If you would like to
# use other orderings, you need to obtain the corresponding package and modify
# the variables below accordingly.
# For example, to have Metis available within MUMPS:
#          1/ download Metis and compile it
#          2/ uncomment (suppress # in first column) lines
#             starting with LMETISDIR,  LMETIS
#          3/ add -Dmetis in line ORDERINGSF
#             ORDERINGSF  = -Dpord -Dmetis
#          4/ Compile and install MUMPS
#             make clean; make   (to clean up previous installation)
#
#          Metis/ParMetis and SCOTCH/PT-SCOTCH (ver 5.1 and later) orderings are now available for MUMPS.
#

#SCOTCHDIR  = ${HOME}/scotch_5.1_esmumps
#ISCOTCH    = -I$(SCOTCHDIR)/include
# You have to choose one among the following two lines depending on
# the type of analysis you want to perform. If you want to perform only
# sequential analysis choose the first (remember to add -Dscotch in the ORDERINGSF
# variable below); for both parallel and sequential analysis choose the second
# line (remember to add -Dptscotch in the ORDERINGSF variable below)

#LSCOTCH    = -L$(SCOTCHDIR)/lib -lesmumps -lscotch -lscotcherr
#LSCOTCH    = -L$(SCOTCHDIR)/lib -lptesmumps -lptscotch -lptscotcherr


LPORDDIR = $(topdir)/PORD/lib/
IPORD    = -I$(topdir)/PORD/include/
LPORD    = -L$(LPORDDIR) -lpord

#LMETISDIR = /local/metis/
#IMETIS    = # Should be provided if you use parmetis

# You have to choose one among the following two lines depending on
# the type of analysis you want to perform. If you want to perform only
# sequential analysis choose the first (remember to add -Dmetis in the ORDERINGSF
# variable below); for both parallel and sequential analysis choose the second
# line (remember to add -Dparmetis in the ORDERINGSF variable below)

#LMETIS    = -L$(LMETISDIR) -lmetis
#LMETIS    = -L$(LMETISDIR) -lparmetis -lmetis

# The following variables will be used in the compilation process.
# Please note that -Dptscotch and -Dparmetis imply -Dscotch and -Dmetis respectively.
#ORDERINGSF = -Dscotch -Dmetis -Dpord -Dptscotch -Dparmetis
ORDERINGSF  = -Dpord
ORDERINGSC  = $(ORDERINGSF)

LORDERINGS = $(LMETIS) $(LPORD) $(LSCOTCH)
IORDERINGSF = $(ISCOTCH)
IORDERINGSC = $(IMETIS) $(IPORD) $(ISCOTCH)

#End orderings
########################################################################
################################################################################

PLAT    =
LIBEXT  = .so
OUTC    = -o
OUTF    = -o
RM = /bin/rm -f
CC = mpicc -fPIC
FC = mpif90 -fPIC
FL = mpif90 -fPIC
AR = mpif90 -shared -o
#RANLIB = ranlib
RANLIB  = echo
SCALAP  = -L${SCALAPACKDIR}/lib -lscalapack
#INCPAR = -I/usr/include
INCPAR = -I/usr/include
LIBPAR = $(SCALAP)  -L/usr/local/lib/
# See point 17 in the FAQ to have more details on the compilation of mpich with gfortran
INCSEQ = -I$(topdir)/libseq
LIBSEQ  =  -L$(topdir)/libseq -lmpiseq
#LIBBLAS = -L/usr/lib/xmm/ -lf77blas -latlas
LIBBLAS = -L/local/BLAS -lblas
LIBOTHERS = -lpthread
#Preprocessor defs for calling Fortran from C (-DAdd_ or -DAdd__ or -DUPPER)
CDEFS   = -DAdd_

#Begin Optimized options
OPTF    = -O -DALLOW_NON_INIT
OPTL    = -O
OPTC    = -O
#End Optimized options
INCS = $(INCPAR)
LIBS = $(LIBPAR)
LIBSEQNEEDED =
