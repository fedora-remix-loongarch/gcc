%global DATE 20101112
%global SVNREV 166681
%global gcc_version 4.5.1
# Note, gcc_release must be integer, if you want to add suffixes to
# %{release}, append them after %{gcc_release} on Release: line.
%global gcc_release 5
%global _unpackaged_files_terminate_build 0
%global multilib_64_archs sparc64 ppc64 s390x x86_64
%ifarch %{ix86} x86_64 ia64 ppc ppc64 alpha
%global build_ada 1
%else
%global build_ada 0
%endif
%global build_java 1
%global build_cloog 1
%global build_libstdcxx_docs 1
# If you don't have already a usable gcc-java and libgcj for your arch,
# do on some arch which has it rpmbuild -bc --with java_tar gcc41.spec
# which creates libjava-classes-%{version}-%{release}.tar.bz2
# With this then on the new arch do rpmbuild -ba -v --with java_bootstrap gcc41.spec
%global bootstrap_java %{?_with_java_bootstrap:%{build_java}}%{!?_with_java_bootstrap:0}
%global build_java_tar %{?_with_java_tar:%{build_java}}%{!?_with_java_tar:0}
%ifarch s390x
%global multilib_32_arch s390
%endif
%ifarch sparc64
%global multilib_32_arch sparcv9
%endif
%ifarch ppc64
%global multilib_32_arch ppc
%endif
%ifarch x86_64
%global multilib_32_arch i686
%endif
Summary: Various compilers (C, C++, Objective-C, Java, ...)
Name: gcc
Version: %{gcc_version}
Release: %{gcc_release}%{?dist}
# libgcc, libgfortran, libmudflap, libgomp, libstdc++ and crtstuff have
# GCC Runtime Exception.
License: GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions
Group: Development/Languages
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# svn export svn://gcc.gnu.org/svn/gcc/branches/redhat/gcc-4_4-branch@%{SVNREV} gcc-%{version}-%{DATE}
# tar cf - gcc-%{version}-%{DATE} | bzip2 -9 > gcc-%{version}-%{DATE}.tar.bz2
Source0: gcc-%{version}-%{DATE}.tar.bz2
Source1: libgcc_post_upgrade.c
%global fastjar_ver 0.97
Source4: http://download.savannah.nongnu.org/releases/fastjar/fastjar-%{fastjar_ver}.tar.gz
URL: http://gcc.gnu.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Need binutils with -pie support >= 2.14.90.0.4-4
# Need binutils which can omit dot symbols and overlap .opd on ppc64 >= 2.15.91.0.2-4
# Need binutils which handle -msecure-plt on ppc >= 2.16.91.0.2-2
# Need binutils which support .weakref >= 2.16.91.0.3-1
# Need binutils which support --hash-style=gnu >= 2.17.50.0.2-7
# Need binutils which support mffgpr and mftgpr >= 2.17.50.0.2-8
# Need binutils which support --build-id >= 2.17.50.0.17-3
# Need binutils which support %gnu_unique_object >= 2.19.51.0.14
# Need binutils which support .cfi_sections >= 2.19.51.0.14-33
# Need binutils which support --no-add-needed >= 2.20.51.0.2-12
BuildRequires: binutils >= 2.20.51.0.2-12
# While gcc doesn't include statically linked binaries, during testing
# -static is used several times.
BuildRequires: glibc-static
BuildRequires: zlib-devel, gettext, dejagnu, bison, flex, texinfo, sharutils
# For VTA guality testing
BuildRequires: gdb
%if %{build_java}
BuildRequires: /usr/share/java/eclipse-ecj.jar, zip, unzip
%if %{bootstrap_java}
Source10: libjava-classes-%{version}-%{release}.tar.bz2
%else
BuildRequires: gcc-java, libgcj
%endif
%endif
# Make sure pthread.h doesn't contain __thread tokens
# Make sure glibc supports stack protector
# Make sure glibc supports DT_GNU_HASH
BuildRequires: glibc-devel >= 2.4.90-13
BuildRequires: elfutils-devel >= 0.147
BuildRequires: elfutils-libelf-devel >= 0.147
%ifarch ppc ppc64 s390 s390x sparc sparcv9 alpha
# Make sure glibc supports TFmode long double
BuildRequires: glibc >= 2.3.90-35
%endif
%ifarch %{multilib_64_archs} sparcv9 ppc
# Ensure glibc{,-devel} is installed for both multilib arches
BuildRequires: /lib/libc.so.6 /usr/lib/libc.so /lib64/libc.so.6 /usr/lib64/libc.so
%endif
%if %{build_ada}
# Ada requires Ada to build
BuildRequires: gcc-gnat >= 3.1, libgnat >= 3.1
%endif
%ifarch ia64
BuildRequires: libunwind >= 0.98
%endif
%if %{build_cloog}
BuildRequires: ppl >= 0.10, ppl-devel >= 0.10, cloog-ppl >= 0.15, cloog-ppl-devel >= 0.15
%endif
%if %{build_libstdcxx_docs}
BuildRequires: doxygen
BuildRequires: graphviz
%endif
Requires: cpp = %{version}-%{release}
# Need .eh_frame ld optimizations
# Need proper visibility support
# Need -pie support
# Need --as-needed/--no-as-needed support
# On ppc64, need omit dot symbols support and --non-overlapping-opd
# Need binutils that owns /usr/bin/c++filt
# Need binutils that support .weakref
# Need binutils that supports --hash-style=gnu
# Need binutils that support mffgpr/mftgpr
# Need binutils that support --build-id
# Need binutils that support %gnu_unique_object
# Need binutils that support .cfi_sections
# Need binutils that support --no-add-needed
Requires: binutils >= 2.20.51.0.2-12
# Make sure gdb will understand DW_FORM_strp
Conflicts: gdb < 5.1-2
Requires: glibc-devel >= 2.2.90-12
%ifarch ppc ppc64 s390 s390x sparc sparcv9 alpha
# Make sure glibc supports TFmode long double
Requires: glibc >= 2.3.90-35
%endif
Requires: libgcc >= %{version}-%{release}
Requires: libgomp = %{version}-%{release}
%if !%{build_ada}
Obsoletes: gcc-gnat < %{version}-%{release}
Obsoletes: libgnat < %{version}-%{release}
%endif
%if %{build_cloog}
Requires: cloog-ppl >= 0.15
%endif
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
AutoReq: true

Patch0: gcc45-hack.patch
Patch2: gcc45-c++-builtin-redecl.patch
Patch4: gcc45-java-nomulti.patch
Patch5: gcc45-ppc32-retaddr.patch
Patch6: gcc45-pr33763.patch
Patch7: gcc45-rh330771.patch
Patch8: gcc45-i386-libgomp.patch
Patch9: gcc45-sparc-config-detection.patch
Patch10: gcc45-libgomp-omp_h-multilib.patch
Patch11: gcc45-libtool-no-rpath.patch
Patch12: gcc45-cloog-dl.patch
Patch14: gcc45-pr38757.patch
Patch15: gcc45-libstdc++-docs.patch
Patch17: gcc45-no-add-needed.patch

Patch1000: fastjar-0.97-segfault.patch
Patch1001: fastjar-0.97-len1.patch
Patch1002: fastjar-0.97-filename0.patch
Patch1003: fastjar-CVE-2010-0831.patch
Patch1004: fastjar-man.patch

# On ARM EABI systems, we do want -gnueabi to be part of the
# target triple.
%ifnarch %{arm}
%global _gnu %{nil}
%endif
%ifarch sparcv9
%global gcc_target_platform sparc64-%{_vendor}-%{_target_os}
%endif
%ifarch ppc
%global gcc_target_platform ppc64-%{_vendor}-%{_target_os}
%endif
%ifnarch sparcv9 ppc
%global gcc_target_platform %{_target_platform}
%endif

%description
The gcc package contains the GNU Compiler Collection version 4.5.
You'll need this package in order to compile C code.

%package -n libgcc
Summary: GCC version 4.5 shared support library
Group: System Environment/Libraries
Autoreq: false

%description -n libgcc
This package contains GCC shared support library which is needed
e.g. for exception handling support.

%package c++
Summary: C++ support for GCC
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libstdc++ = %{version}-%{release}
Requires: libstdc++-devel = %{version}-%{release}
Autoreq: true

%description c++
This package adds C++ support to the GNU Compiler Collection.
It includes support for most of the current C++ specification,
including templates and exception handling.

%package -n libstdc++
Summary: GNU Standard C++ Library
Group: System Environment/Libraries
Autoreq: true
Requires: glibc >= 2.10.90-7

%description -n libstdc++
The libstdc++ package contains a rewritten standard compliant GCC Standard
C++ Library.

%package -n libstdc++-devel
Summary: Header files and libraries for C++ development
Group: Development/Libraries
Requires: libstdc++%{?_isa} = %{version}-%{release}
Autoreq: true

%description -n libstdc++-devel
This is the GNU implementation of the standard C++ libraries.  This
package includes the header files and libraries needed for C++
development. This includes rewritten implementation of STL.

%package -n libstdc++-static
Summary: Static libraries for the GNU standard C++ library
Group: Development/Libraries
Requires: libstdc++-devel = %{version}-%{release}
Autoreq: true

%description -n libstdc++-static
Static libraries for the GNU standard C++ library. 

%package -n libstdc++-docs
Summary: Documentation for the GNU standard C++ library
Group: Development/Libraries
Autoreq: true

%description -n libstdc++-docs
Manual, doxygen generated API information and Frequently Asked Questions
for the GNU standard C++ library.

%package objc
Summary: Objective-C support for GCC
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libobjc = %{version}-%{release}
Autoreq: true

%description objc
gcc-objc provides Objective-C support for the GCC.
Mainly used on systems running NeXTSTEP, Objective-C is an
object-oriented derivative of the C language.

%package objc++
Summary: Objective-C++ support for GCC
Group: Development/Languages
Requires: gcc-c++ = %{version}-%{release}, gcc-objc = %{version}-%{release}
Autoreq: true

%description objc++
gcc-objc++ package provides Objective-C++ support for the GCC.

%package -n libobjc
Summary: Objective-C runtime
Group: System Environment/Libraries
Autoreq: true

%description -n libobjc
This package contains Objective-C shared library which is needed to run
Objective-C dynamically linked programs.

%package gfortran
Summary: Fortran support
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libgfortran = %{version}-%{release}
BuildRequires: gmp-devel >= 4.1.2-8, mpfr-devel >= 2.2.1, libmpc-devel >= 0.8.1
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Autoreq: true

%description gfortran
The gcc-gfortran package provides support for compiling Fortran
programs with the GNU Compiler Collection.

%package -n libgfortran
Summary: Fortran runtime
Group: System Environment/Libraries
Autoreq: true

%description -n libgfortran
This package contains Fortran shared library which is needed to run
Fortran dynamically linked programs.

%package -n libgomp
Summary: GCC OpenMP v3.0 shared support library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libgomp
This package contains GCC shared support library which is needed
for OpenMP v3.0 support.

%package -n libmudflap
Summary: GCC mudflap shared support library
Group: System Environment/Libraries

%description -n libmudflap
This package contains GCC shared support library which is needed
for mudflap support.

%package -n libmudflap-devel
Summary: GCC mudflap support
Group: Development/Libraries
Requires: libmudflap = %{version}-%{release}
Requires: gcc = %{version}-%{release}

%description -n libmudflap-devel
This package contains headers for building mudflap-instrumented programs.

To instrument a non-threaded program, add -fmudflap
option to GCC and when linking add -lmudflap, for threaded programs
also add -fmudflapth and -lmudflapth.

%package -n libmudflap-static
Summary: Static libraries for mudflap support
Group: Development/Libraries
Requires: libmudflap-devel = %{version}-%{release}

%description -n libmudflap-static
This package contains static libraries for building mudflap-instrumented
programs.

%package java
Summary: Java support for GCC
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libgcj = %{version}-%{release}
Requires: libgcj-devel = %{version}-%{release}
Requires: /usr/share/java/eclipse-ecj.jar
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Autoreq: true

%description java
This package adds support for compiling Java(tm) programs and
bytecode into native code.

%package -n libgcj
Summary: Java runtime library for gcc
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Requires: zip >= 2.1
Requires: gtk2 >= 2.4.0
Requires: glib2 >= 2.4.0
Requires: libart_lgpl >= 2.1.0
%if %{build_java}
BuildRequires: gtk2-devel >= 2.4.0
BuildRequires: glib2-devel >= 2.4.0
BuildRequires: libart_lgpl-devel >= 2.1.0
BuildRequires: alsa-lib-devel
BuildRequires: libXtst-devel
BuildRequires: libXt-devel
%endif
Autoreq: true

%description -n libgcj
The Java(tm) runtime library. You will need this package to run your Java
programs compiled using the Java compiler from GNU Compiler Collection (gcj).

%package -n libgcj-devel
Summary: Libraries for Java development using GCC
Group: Development/Languages
Requires: libgcj%{?_isa} = %{version}-%{release}
Requires: zlib-devel%{?_isa}
Requires: /bin/awk
Autoreq: false
Autoprov: false

%description -n libgcj-devel
The Java(tm) static libraries and C header files. You will need this
package to compile your Java programs using the GCC Java compiler (gcj).

%package -n libgcj-src
Summary: Java library sources from GCC4 preview
Group: System Environment/Libraries
Requires: libgcj = %{version}-%{release}
Autoreq: true

%description -n libgcj-src
The Java(tm) runtime library sources for use in Eclipse.

%package -n cpp
Summary: The C Preprocessor
Group: Development/Languages
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Autoreq: true

%description -n cpp
Cpp is the GNU C-Compatible Compiler Preprocessor.
Cpp is a macro processor which is used automatically
by the C compiler to transform your program before actual
compilation. It is called a macro processor because it allows
you to define macros, abbreviations for longer
constructs.

The C preprocessor provides four separate functionalities: the
inclusion of header files (files of declarations that can be
substituted into your program); macro expansion (you can define macros,
and the C preprocessor will replace the macros with their definitions
throughout the program); conditional compilation (using special
preprocessing directives, you can include or exclude parts of the
program according to various conditions); and line control (if you use
a program to combine or rearrange source files into an intermediate
file which is then compiled, you can use line control to inform the
compiler about where each source line originated).

You should install this package if you are a C programmer and you use
macros.

%package gnat
Summary: Ada 95 support for GCC
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libgnat = %{version}-%{release}, libgnat-devel = %{version}-%{release}
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Autoreq: true

%description gnat
GNAT is a GNU Ada 95 front-end to GCC. This package includes development tools,
the documents and Ada 95 compiler.

%package -n libgnat
Summary: GNU Ada 95 runtime shared libraries
Group: System Environment/Libraries
Autoreq: true

%description -n libgnat
GNAT is a GNU Ada 95 front-end to GCC. This package includes shared libraries,
which are required to run programs compiled with the GNAT.

%package -n libgnat-devel
Summary: GNU Ada 95 libraries
Group: System Environment/Libraries
Autoreq: true

%description -n libgnat-devel
GNAT is a GNU Ada 95 front-end to GCC. This package includes libraries,
which are required to compile with the GNAT.

%package -n libgnat-static
Summary: GNU Ada 95 static libraries
Group: System Environment/Libraries
Requires: libgnat-devel = %{version}-%{release}
Autoreq: true

%description -n libgnat-static
GNAT is a GNU Ada 95 front-end to GCC. This package includes static libraries.

%prep
%setup -q -n gcc-%{version}-%{DATE}
%patch0 -p0 -b .hack~
%patch2 -p0 -b .c++-builtin-redecl~
%patch4 -p0 -b .java-nomulti~
%patch5 -p0 -b .ppc32-retaddr~
%patch6 -p0 -b .pr33763~
%patch7 -p0 -b .rh330771~
%patch8 -p0 -b .i386-libgomp~
%patch9 -p0 -b .sparc-config-detection~
%patch10 -p0 -b .libgomp-omp_h-multilib~
%patch11 -p0 -b .libtool-no-rpath~
%if %{build_cloog}
%patch12 -p0 -b .cloog-dl~
%endif
%patch14 -p0 -b .pr38757~
%if %{build_libstdcxx_docs}
%patch15 -p0 -b .libstdc++-docs~
%endif
%patch17 -p0 -b .no-add-needed~

# This testcase doesn't compile.
rm libjava/testsuite/libjava.lang/PR35020*

tar xzf %{SOURCE4}

%patch1000 -p0 -b .fastjar-0.97-segfault~
%patch1001 -p0 -b .fastjar-0.97-len1~
%patch1002 -p0 -b .fastjar-0.97-filename0~
%patch1003 -p0 -b .fastjar-CVE-2010-0831~
%patch1004 -p0 -b .fastjar-man~

%if %{bootstrap_java}
tar xjf %{SOURCE10}
%endif

sed -i -e 's/4\.5\.2/4.5.1/' gcc/BASE-VER
echo 'Red Hat %{version}-%{gcc_release}' > gcc/DEV-PHASE
%if 0%{?fedora} <= 14
sed -i -e 's/#define EMIT_IMPLICIT_PTR 1/#define EMIT_IMPLICIT_PTR 0/' gcc/cfgexpand.c
%endif

# Default to -gdwarf-3 rather than -gdwarf-2
sed -i '/UInteger Var(dwarf_version)/s/Init(2)/Init(3)/' gcc/common.opt
sed -i 's/\(may be either 2, 3 or 4; the default version is \)2\./\13./' gcc/doc/invoke.texi

cp -a libstdc++-v3/config/cpu/i{4,3}86/atomicity.h

# Hack to avoid building multilib libjava
perl -pi -e 's/^all: all-redirect/ifeq (\$(MULTISUBDIR),)\nall: all-redirect\nelse\nall:\n\techo Multilib libjava build disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^install: install-redirect/ifeq (\$(MULTISUBDIR),)\ninstall: install-redirect\nelse\ninstall:\n\techo Multilib libjava install disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^check: check-redirect/ifeq (\$(MULTISUBDIR),)\ncheck: check-redirect\nelse\ncheck:\n\techo Multilib libjava check disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^all: all-recursive/ifeq (\$(MULTISUBDIR),)\nall: all-recursive\nelse\nall:\n\techo Multilib libjava build disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^install: install-recursive/ifeq (\$(MULTISUBDIR),)\ninstall: install-recursive\nelse\ninstall:\n\techo Multilib libjava install disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^check: check-recursive/ifeq (\$(MULTISUBDIR),)\ncheck: check-recursive\nelse\ncheck:\n\techo Multilib libjava check disabled\nendif/' libjava/Makefile.in

./contrib/gcc_update --touch

LC_ALL=C sed -i -e 's/\xa0/ /' gcc/doc/options.texi

%ifarch ppc
if [ -d libstdc++-v3/config/abi/post/powerpc64-linux-gnu ]; then
  mkdir -p libstdc++-v3/config/abi/post/powerpc64-linux-gnu/64
  mv libstdc++-v3/config/abi/post/powerpc64-linux-gnu/{,64/}baseline_symbols.txt
  mv libstdc++-v3/config/abi/post/powerpc64-linux-gnu/{32/,}baseline_symbols.txt
  rm -rf libstdc++-v3/config/abi/post/powerpc64-linux-gnu/32
fi
%endif
%ifarch sparc
if [ -d libstdc++-v3/config/abi/post/sparc64-linux-gnu ]; then
  mkdir -p libstdc++-v3/config/abi/post/sparc64-linux-gnu/64
  mv libstdc++-v3/config/abi/post/sparc64-linux-gnu/{,64/}baseline_symbols.txt
  mv libstdc++-v3/config/abi/post/sparc64-linux-gnu/{32/,}baseline_symbols.txt
  rm -rf libstdc++-v3/config/abi/post/sparc64-linux-gnu/32
fi
%endif

%build

%if %{build_java}
export GCJ_PROPERTIES=jdt.compiler.useSingleThread=true
# gjar isn't usable, so even when GCC source tree no longer includes
# fastjar, build it anyway.
mkdir fastjar-%{fastjar_ver}/obj-%{gcc_target_platform}
cd fastjar-%{fastjar_ver}/obj-%{gcc_target_platform}
../configure CFLAGS="%{optflags}" --prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir}
make %{?_smp_mflags}
export PATH=`pwd`${PATH:+:$PATH}
cd ../../
%endif

rm -fr obj-%{gcc_target_platform}
mkdir obj-%{gcc_target_platform}
cd obj-%{gcc_target_platform}

%if %{build_java}
%if !%{bootstrap_java}
# If we don't have gjavah in $PATH, try to build it with the old gij
mkdir java_hacks
cd java_hacks
cp -a ../../libjava/classpath/tools/external external
mkdir -p gnu/classpath/tools
cp -a ../../libjava/classpath/tools/gnu/classpath/tools/{common,javah,getopt} gnu/classpath/tools/
cp -a ../../libjava/classpath/tools/resource/gnu/classpath/tools/common/Messages.properties gnu/classpath/tools/common
cp -a ../../libjava/classpath/tools/resource/gnu/classpath/tools/getopt/Messages.properties gnu/classpath/tools/getopt
cd external/asm; for i in `find . -name \*.java`; do gcj --encoding ISO-8859-1 -C $i -I.; done; cd ../..
for i in `find gnu -name \*.java`; do gcj -C $i -I. -Iexternal/asm/; done
gcj -findirect-dispatch -O2 -fmain=gnu.classpath.tools.javah.Main -I. -Iexternal/asm/ `find . -name \*.class` -o gjavah.real
cat > gjavah <<EOF
#!/bin/sh
export CLASSPATH=`pwd`${CLASSPATH:+:$CLASSPATH}
exec `pwd`/gjavah.real "\$@"
EOF
chmod +x `pwd`/gjavah
cat > ecj1 <<EOF
#!/bin/sh
exec gij -cp /usr/share/java/eclipse-ecj.jar org.eclipse.jdt.internal.compiler.batch.GCCMain "\$@"
EOF
chmod +x `pwd`/ecj1
export PATH=`pwd`${PATH:+:$PATH}
cd ..
%endif
%endif

CC=gcc
OPT_FLAGS=`echo %{optflags}|sed -e 's/\(-Wp,\)\?-D_FORTIFY_SOURCE=[12]//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-m64//g;s/-m32//g;s/-m31//g'`
%ifarch sparc
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-mcpu=ultrasparc/-mtune=ultrasparc/g;s/-mcpu=v[78]//g'`
%endif
%ifarch %{ix86}
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-march=i.86//g'`
%endif
%ifarch sparc64
cat > gcc64 <<"EOF"
#!/bin/sh
exec /usr/bin/gcc -m64 "$@"
EOF
chmod +x gcc64
CC=`pwd`/gcc64
%endif
%ifarch ppc64
if gcc -m64 -xc -S /dev/null -o - > /dev/null 2>&1; then
  cat > gcc64 <<"EOF"
#!/bin/sh
exec /usr/bin/gcc -m64 "$@"
EOF
  chmod +x gcc64
  CC=`pwd`/gcc64
fi
%endif
OPT_FLAGS=`echo "$OPT_FLAGS" | sed -e 's/[[:blank:]]\+/ /g'`
case "$OPT_FLAGS" in
  *-fasynchronous-unwind-tables*)
    sed -i -e 's/-fno-exceptions /-fno-exceptions -fno-asynchronous-unwind-tables/' \
      ../gcc/Makefile.in
    ;;
esac
CC="$CC" CFLAGS="$OPT_FLAGS" CXXFLAGS="`echo $OPT_FLAGS | sed 's/ -Wall / /g'`" \
	XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" GCJFLAGS="$OPT_FLAGS" \
	../configure --prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
	--with-bugurl=http://bugzilla.redhat.com/bugzilla --enable-bootstrap \
	--enable-shared --enable-threads=posix --enable-checking=release \
	--with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions \
	--enable-gnu-unique-object --enable-linker-build-id \
%if !%{build_ada}
	--enable-languages=c,c++,objc,obj-c++,java,fortran,lto \
%else
	--enable-languages=c,c++,objc,obj-c++,java,fortran,ada,lto \
%endif
	--enable-plugin \
%if !%{build_java}
	--disable-libgcj \
%else
	--enable-java-awt=gtk --disable-dssi \
	--with-java-home=%{_prefix}/lib/jvm/java-1.5.0-gcj-1.5.0.0/jre \
	--enable-libgcj-multifile \
%if !%{bootstrap_java}
	--enable-java-maintainer-mode \
%endif
	--with-ecj-jar=/usr/share/java/eclipse-ecj.jar \
	--disable-libjava-multilib \
%endif
%if %{build_cloog}
	--with-ppl --with-cloog \
%endif
%ifarch %{arm}
	--disable-sjlj-exceptions \
%endif
%ifarch ppc ppc64
	--enable-secureplt \
%endif
%ifarch sparc sparcv9 sparc64 ppc ppc64 s390 s390x alpha
	--with-long-double-128 \
%endif
%ifarch sparc
	--disable-linux-futex \
%endif
%ifarch sparc64
	--with-cpu=ultrasparc \
%endif
%ifarch sparc sparcv9
	--host=%{gcc_target_platform} --build=%{gcc_target_platform} --target=%{gcc_target_platform} --with-cpu=v7
%endif
%if 0%{?rhel} >= 6
%ifarch ppc ppc64
	--with-cpu-32=power4 --with-tune-32=power6 --with-cpu-64=power4 --with-tune-64=power6 \
%endif
%endif
%ifarch ppc
	--build=%{gcc_target_platform} --target=%{gcc_target_platform} --with-cpu=default32
%endif
%ifarch %{ix86} x86_64
	--with-tune=generic \
%endif
%ifarch %{ix86}
	--with-arch=i686 \
%endif
%ifarch x86_64
	--with-arch_32=i686 \
%endif
%ifarch s390 s390x
	--with-arch=z9-109 --with-tune=z10 --enable-decimal-float \
%endif
%ifnarch sparc sparcv9 ppc
	--build=%{gcc_target_platform}
%endif

#GCJFLAGS="$OPT_FLAGS" make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" bootstrap
GCJFLAGS="$OPT_FLAGS" make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" profiledbootstrap

# Make generated man pages even if Pod::Man is not new enough
perl -pi -e 's/head3/head2/' ../contrib/texi2pod.pl
for i in ../gcc/doc/*.texi; do
  cp -a $i $i.orig; sed 's/ftable/table/' $i.orig > $i
done
make -C gcc generated-manpages
for i in ../gcc/doc/*.texi; do mv -f $i.orig $i; done

# Make generated doxygen pages.
%if %{build_libstdcxx_docs}
cd %{gcc_target_platform}/libstdc++-v3
make doc-html-doxygen
make doc-man-doxygen
cd ../..
%endif

# Copy various doc files here and there
cd ..
mkdir -p rpm.doc/gfortran rpm.doc/objc
mkdir -p rpm.doc/boehm-gc rpm.doc/fastjar rpm.doc/libffi rpm.doc/libjava
mkdir -p rpm.doc/changelogs/{gcc/cp,gcc/java,gcc/ada,libstdc++-v3,libobjc,libmudflap,libgomp}

for i in {gcc,gcc/cp,gcc/java,gcc/ada,libstdc++-v3,libobjc,libmudflap,libgomp}/ChangeLog*; do
	cp -p $i rpm.doc/changelogs/$i
done

(cd gcc/fortran; for i in ChangeLog*; do
	cp -p $i ../../rpm.doc/gfortran/$i
done)
(cd libgfortran; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/gfortran/$i.libgfortran
done)
(cd gcc/objc; for i in README*; do
	cp -p $i ../../rpm.doc/objc/$i.objc
done)
(cd libobjc; for i in README*; do
	cp -p $i ../rpm.doc/objc/$i.libobjc
done)
(cd boehm-gc; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/boehm-gc/$i.gc
done)
(cd fastjar-%{fastjar_ver}; for i in ChangeLog* README*; do
	cp -p $i ../rpm.doc/fastjar/$i.fastjar
done)
(cd libffi; for i in ChangeLog* README* LICENSE; do
	cp -p $i ../rpm.doc/libffi/$i.libffi
done)
(cd libjava; for i in ChangeLog* README*; do
	cp -p $i ../rpm.doc/libjava/$i.libjava
done)
cp -p libjava/LIBGCJ_LICENSE rpm.doc/libjava/

rm -f rpm.doc/changelogs/gcc/ChangeLog.[1-9]
find rpm.doc -name \*ChangeLog\* | xargs bzip2 -9

%if %{build_java_tar}
find libjava -name \*.h -type f | xargs grep -l '// DO NOT EDIT THIS FILE - it is machine generated' > libjava-classes.list
find libjava -name \*.class -type f >> libjava-classes.list
find libjava/testsuite -name \*.jar -type f >> libjava-classes.list
tar cf - -T libjava-classes.list | bzip2 -9 > $RPM_SOURCE_DIR/libjava-classes-%{version}-%{release}.tar.bz2
%endif

%install
rm -fr %{buildroot}

cd obj-%{gcc_target_platform}

%if %{build_java}
export GCJ_PROPERTIES=jdt.compiler.useSingleThread=true
export PATH=`pwd`/../fastjar-%{fastjar_ver}/obj-%{gcc_target_platform}${PATH:+:$PATH}
%if !%{bootstrap_java}
export PATH=`pwd`/java_hacks${PATH:+:$PATH}
%endif
%endif

TARGET_PLATFORM=%{gcc_target_platform}

# There are some MP bugs in libstdc++ Makefiles
make -C %{gcc_target_platform}/libstdc++-v3

make prefix=%{buildroot}%{_prefix} mandir=%{buildroot}%{_mandir} \
  infodir=%{buildroot}%{_infodir} install
%if %{build_java}
make DESTDIR=%{buildroot} -C %{gcc_target_platform}/libjava install-src.zip
%endif
%if %{build_ada}
chmod 644 %{buildroot}%{_infodir}/gnat*
%endif

FULLPATH=%{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
FULLEPATH=%{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}

# fix some things
ln -sf gcc %{buildroot}%{_prefix}/bin/cc
mkdir -p %{buildroot}/lib
ln -sf ..%{_prefix}/bin/cpp %{buildroot}/lib/cpp
ln -sf gfortran %{buildroot}%{_prefix}/bin/f95
rm -f %{buildroot}%{_infodir}/dir
gzip -9 %{buildroot}%{_infodir}/*.info*
ln -sf gcc %{buildroot}%{_prefix}/bin/gnatgcc

cxxconfig="`find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h`"
for i in `find %{gcc_target_platform}/[36]*/libstdc++-v3/include -name c++config.h 2>/dev/null`; do
  if ! diff -up $cxxconfig $i; then
    cat > %{buildroot}%{_prefix}/include/c++/%{gcc_version}/%{gcc_target_platform}/bits/c++config.h <<EOF
#ifndef _CPP_CPPCONFIG_WRAPPER
#define _CPP_CPPCONFIG_WRAPPER 1
#include <bits/wordsize.h>
#if __WORDSIZE == 32
%ifarch %{multilib_64_archs}
`cat $(find %{gcc_target_platform}/32/libstdc++-v3/include -name c++config.h)`
%else
`cat $(find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h)`
%endif
#else
%ifarch %{multilib_64_archs}
`cat $(find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h)`
%else
`cat $(find %{gcc_target_platform}/64/libstdc++-v3/include -name c++config.h)`
%endif
#endif
#endif
EOF
    break
  fi
done

for f in `find %{buildroot}%{_prefix}/include/c++/%{gcc_version}/%{gcc_target_platform}/ -name c++config.h`; do
  for i in 1 2 4 8; do
    sed -i -e 's/#define _GLIBCXX_ATOMIC_BUILTINS_'$i' 1/#ifdef __GCC_HAVE_SYNC_COMPARE_AND_SWAP_'$i'\
&\
#endif/' $f
  done
done

# Nuke bits/stdc++.h.gch dirs
# 1) there is no bits/stdc++.h header installed, so when gch file can't be
#    used, compilation fails
# 2) sometimes it is hard to match the exact options used for building
#    libstdc++-v3 or they aren't desirable
# 3) there are multilib issues, conflicts etc. with this
# 4) it is huge
# People can always precompile on their own whatever they want, but
# shipping this for everybody is unnecessary.
rm -rf %{buildroot}%{_prefix}/include/c++/%{gcc_version}/%{gcc_target_platform}/bits/stdc++.h.gch

%if %{build_libstdcxx_docs}
libstdcxx_doc_builddir=%{gcc_target_platform}/libstdc++-v3/doc/doxygen
mkdir -p ../rpm.doc/libstdc++-v3
cp -r -p ../libstdc++-v3/doc/html ../rpm.doc/libstdc++-v3/html
cp -r -p $libstdcxx_doc_builddir/html ../rpm.doc/libstdc++-v3/html/api
mkdir -p %{buildroot}%{_mandir}
cp -r -p $libstdcxx_doc_builddir/man/man3 %{buildroot}%{_mandir}/man3/
find ../rpm.doc/libstdc++-v3 -name \*~ | xargs rm
%endif

%ifarch sparcv9 sparc64
ln -f %{buildroot}%{_prefix}/bin/%{gcc_target_platform}-gcc \
  %{buildroot}%{_prefix}/bin/sparc-%{_vendor}-%{_target_os}-gcc
%endif
%ifarch ppc ppc64
ln -f %{buildroot}%{_prefix}/bin/%{gcc_target_platform}-gcc \
  %{buildroot}%{_prefix}/bin/ppc-%{_vendor}-%{_target_os}-gcc
%endif

%ifarch sparcv9 ppc
FULLLPATH=$FULLPATH/lib32
%endif
%ifarch sparc64 ppc64
FULLLPATH=$FULLPATH/lib64
%endif
if [ -n "$FULLLPATH" ]; then
  mkdir -p $FULLLPATH
else
  FULLLPATH=$FULLPATH
fi

find %{buildroot} -name \*.la | xargs rm -f
%if %{build_java}
# gcj -static doesn't work properly anyway, unless using --whole-archive
# and saving 35MB is not bad.
find %{buildroot} -name libgcj.a -o -name libgtkpeer.a \
		     -o -name libgjsmalsa.a -o -name libgcj-tools.a -o -name libjvm.a \
		     -o -name libgij.a -o -name libgcj_bc.a -o -name libjavamath.a \
  | xargs rm -f

mv %{buildroot}%{_prefix}/lib/libgcj.spec $FULLPATH/
sed -i -e 's/lib: /&%%{static:%%eJava programs cannot be linked statically}/' \
  $FULLPATH/libgcj.spec
%endif

mkdir -p %{buildroot}/%{_lib}
mv -f %{buildroot}%{_prefix}/%{_lib}/libgcc_s.so.1 %{buildroot}/%{_lib}/libgcc_s-%{gcc_version}-%{DATE}.so.1
chmod 755 %{buildroot}/%{_lib}/libgcc_s-%{gcc_version}-%{DATE}.so.1
ln -sf libgcc_s-%{gcc_version}-%{DATE}.so.1 %{buildroot}/%{_lib}/libgcc_s.so.1
ln -sf /%{_lib}/libgcc_s.so.1 $FULLPATH/libgcc_s.so
%ifarch sparcv9 ppc
ln -sf /lib64/libgcc_s.so.1 $FULLPATH/64/libgcc_s.so
%endif
%ifarch %{multilib_64_archs}
ln -sf /lib/libgcc_s.so.1 $FULLPATH/32/libgcc_s.so
%endif
%ifarch ppc
rm -f $FULLPATH/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
OUTPUT_FORMAT(elf32-powerpc)
GROUP ( /lib/libgcc_s.so.1 libgcc.a )' > $FULLPATH/libgcc_s.so
%endif
%ifarch ppc64
rm -f $FULLPATH/32/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
OUTPUT_FORMAT(elf32-powerpc)
GROUP ( /lib/libgcc_s.so.1 libgcc.a )' > $FULLPATH/32/libgcc_s.so
%endif

mv -f %{buildroot}%{_prefix}/%{_lib}/libgomp.spec $FULLPATH/

%if %{build_ada}
mv -f $FULLPATH/adalib/libgnarl-*.so %{buildroot}%{_prefix}/%{_lib}/
mv -f $FULLPATH/adalib/libgnat-*.so %{buildroot}%{_prefix}/%{_lib}/
rm -f $FULLPATH/adalib/libgnarl.so* $FULLPATH/adalib/libgnat.so*
%endif

mkdir -p %{buildroot}%{_prefix}/libexec/getconf
if gcc/xgcc -B gcc/ -E -dD -xc /dev/null | grep __LONG_MAX__.*2147483647; then
  ln -sf POSIX_V6_ILP32_OFF32 %{buildroot}%{_prefix}/libexec/getconf/default
else
  ln -sf POSIX_V6_LP64_OFF64 %{buildroot}%{_prefix}/libexec/getconf/default
fi

%if %{build_java}
pushd ../fastjar-%{fastjar_ver}/obj-%{gcc_target_platform}
make install DESTDIR=%{buildroot}
popd

if [ "%{_lib}" != "lib" ]; then
  mkdir -p %{buildroot}%{_prefix}/%{_lib}/pkgconfig
  sed '/^libdir/s/lib$/%{_lib}/' %{buildroot}%{_prefix}/lib/pkgconfig/libgcj-*.pc \
    > %{buildroot}%{_prefix}/%{_lib}/pkgconfig/`basename %{buildroot}%{_prefix}/lib/pkgconfig/libgcj-*.pc`
fi
%endif

mkdir -p %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++*gdb.py* \
      %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/
pushd ../libstdc++-v3/python
for i in `find . -name \*.py`; do
  touch -r $i %{buildroot}%{_prefix}/share/gcc-%{gcc_version}/python/$i
done
touch -r hook.in %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/libstdc++*gdb.py
popd

pushd $FULLPATH
if [ "%{_lib}" = "lib" ]; then
ln -sf ../../../libobjc.so.2 libobjc.so
ln -sf ../../../libstdc++.so.6.*[0-9] libstdc++.so
ln -sf ../../../libgfortran.so.3.* libgfortran.so
ln -sf ../../../libgomp.so.1.* libgomp.so
ln -sf ../../../libmudflap.so.0.* libmudflap.so
ln -sf ../../../libmudflapth.so.0.* libmudflapth.so
%if %{build_java}
ln -sf ../../../libgcj.so.11.* libgcj.so
ln -sf ../../../libgcj-tools.so.11.* libgcj-tools.so
ln -sf ../../../libgij.so.11.* libgij.so
%endif
else
ln -sf ../../../../%{_lib}/libobjc.so.2 libobjc.so
ln -sf ../../../../%{_lib}/libstdc++.so.6.*[0-9] libstdc++.so
ln -sf ../../../../%{_lib}/libgfortran.so.3.* libgfortran.so
ln -sf ../../../../%{_lib}/libgomp.so.1.* libgomp.so
ln -sf ../../../../%{_lib}/libmudflap.so.0.* libmudflap.so
ln -sf ../../../../%{_lib}/libmudflapth.so.0.* libmudflapth.so
%if %{build_java}
ln -sf ../../../../%{_lib}/libgcj.so.11.* libgcj.so
ln -sf ../../../../%{_lib}/libgcj-tools.so.11.* libgcj-tools.so
ln -sf ../../../../%{_lib}/libgij.so.11.* libgij.so
%endif
fi
%if %{build_java}
mv -f %{buildroot}%{_prefix}/%{_lib}/libgcj_bc.so $FULLLPATH/
%endif
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libsupc++.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libgfortran.*a .
mv -f %{buildroot}%{_prefix}/%{_lib}/libobjc.*a .
mv -f %{buildroot}%{_prefix}/%{_lib}/libgomp.*a .
mv -f %{buildroot}%{_prefix}/%{_lib}/libmudflap{,th}.*a $FULLLPATH/

%if %{build_ada}
%ifarch sparcv9 ppc
rm -rf $FULLPATH/64/ada{include,lib}
%endif
%ifarch %{multilib_64_archs}
rm -rf $FULLPATH/32/ada{include,lib}
%endif
if [ "$FULLPATH" != "$FULLLPATH" ]; then
mv -f $FULLPATH/ada{include,lib} $FULLLPATH/
pushd $FULLLPATH/adalib
if [ "%{_lib}" = "lib" ]; then
ln -sf ../../../../../libgnarl-*.so libgnarl.so
ln -sf ../../../../../libgnarl-*.so libgnarl-4.5.so
ln -sf ../../../../../libgnat-*.so libgnat.so
ln -sf ../../../../../libgnat-*.so libgnat-4.5.so
else
ln -sf ../../../../../../%{_lib}/libgnarl-*.so libgnarl.so
ln -sf ../../../../../../%{_lib}/libgnarl-*.so libgnarl-4.5.so
ln -sf ../../../../../../%{_lib}/libgnat-*.so libgnat.so
ln -sf ../../../../../../%{_lib}/libgnat-*.so libgnat-4.5.so
fi
popd
else
pushd $FULLPATH/adalib
if [ "%{_lib}" = "lib" ]; then
ln -sf ../../../../libgnarl-*.so libgnarl.so
ln -sf ../../../../libgnarl-*.so libgnarl-4.5.so
ln -sf ../../../../libgnat-*.so libgnat.so
ln -sf ../../../../libgnat-*.so libgnat-4.5.so
else
ln -sf ../../../../../%{_lib}/libgnarl-*.so libgnarl.so
ln -sf ../../../../../%{_lib}/libgnarl-*.so libgnarl-4.5.so
ln -sf ../../../../../%{_lib}/libgnat-*.so libgnat.so
ln -sf ../../../../../%{_lib}/libgnat-*.so libgnat-4.5.so
fi
popd
fi
%endif

%ifarch sparcv9 ppc
ln -sf ../../../../../lib64/libobjc.so.2 64/libobjc.so
ln -sf ../`echo ../../../../lib/libstdc++.so.6.*[0-9] | sed s~/lib/~/lib64/~` 64/libstdc++.so
ln -sf ../`echo ../../../../lib/libgfortran.so.3.* | sed s~/lib/~/lib64/~` 64/libgfortran.so
ln -sf ../`echo ../../../../lib/libgomp.so.1.* | sed s~/lib/~/lib64/~` 64/libgomp.so
rm -f libmudflap.so libmudflapth.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libmudflap.so.0.* | sed 's,^.*libm,libm,'`' )' > libmudflap.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libmudflapth.so.0.* | sed 's,^.*libm,libm,'`' )' > libmudflapth.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libmudflap.so.0.* | sed 's,^.*libm,libm,'`' )' > 64/libmudflap.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libmudflapth.so.0.* | sed 's,^.*libm,libm,'`' )' > 64/libmudflapth.so
%if %{build_java}
ln -sf ../`echo ../../../../lib/libgcj.so.11.* | sed s~/lib/~/lib64/~` 64/libgcj.so
ln -sf ../`echo ../../../../lib/libgcj-tools.so.11.* | sed s~/lib/~/lib64/~` 64/libgcj-tools.so
ln -sf ../`echo ../../../../lib/libgij.so.11.* | sed s~/lib/~/lib64/~` 64/libgij.so
ln -sf lib32/libgcj_bc.so libgcj_bc.so
ln -sf ../lib64/libgcj_bc.so 64/libgcj_bc.so
%endif
mv -f %{buildroot}%{_prefix}/lib64/libgfortran.*a 64/
mv -f %{buildroot}%{_prefix}/lib64/libobjc.*a 64/
mv -f %{buildroot}%{_prefix}/lib64/libgomp.*a 64/
ln -sf lib32/libstdc++.a libstdc++.a
ln -sf ../lib64/libstdc++.a 64/libstdc++.a
ln -sf lib32/libsupc++.a libsupc++.a
ln -sf ../lib64/libsupc++.a 64/libsupc++.a
ln -sf lib32/libmudflap.a libmudflap.a
ln -sf ../lib64/libmudflap.a 64/libmudflap.a
ln -sf lib32/libmudflapth.a libmudflapth.a
ln -sf ../lib64/libmudflapth.a 64/libmudflapth.a
%if %{build_ada}
ln -sf lib32/adainclude adainclude
ln -sf ../lib64/adainclude 64/adainclude
ln -sf lib32/adalib adalib
ln -sf ../lib64/adalib 64/adalib
%endif
%endif
%ifarch %{multilib_64_archs}
mkdir -p 32
ln -sf ../../../../libobjc.so.2 32/libobjc.so
ln -sf ../`echo ../../../../lib64/libstdc++.so.6.*[0-9] | sed s~/../lib64/~/~` 32/libstdc++.so
ln -sf ../`echo ../../../../lib64/libgfortran.so.3.* | sed s~/../lib64/~/~` 32/libgfortran.so
ln -sf ../`echo ../../../../lib64/libgomp.so.1.* | sed s~/../lib64/~/~` 32/libgomp.so
rm -f libmudflap.so libmudflapth.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libmudflap.so.0.* | sed 's,^.*libm,libm,'`' )' > libmudflap.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libmudflapth.so.0.* | sed 's,^.*libm,libm,'`' )' > libmudflapth.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libmudflap.so.0.* | sed 's,^.*libm,libm,'`' )' > 32/libmudflap.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libmudflapth.so.0.* | sed 's,^.*libm,libm,'`' )' > 32/libmudflapth.so
%if %{build_java}
ln -sf ../`echo ../../../../lib64/libgcj.so.11.* | sed s~/../lib64/~/~` 32/libgcj.so
ln -sf ../`echo ../../../../lib64/libgcj-tools.so.11.* | sed s~/../lib64/~/~` 32/libgcj-tools.so
ln -sf ../`echo ../../../../lib64/libgij.so.11.* | sed s~/../lib64/~/~` 32/libgij.so
%endif
mv -f %{buildroot}%{_prefix}/lib/libgfortran.*a 32/
mv -f %{buildroot}%{_prefix}/lib/libobjc.*a 32/
mv -f %{buildroot}%{_prefix}/lib/libgomp.*a 32/
%endif
%ifarch sparc64 ppc64
ln -sf ../lib32/libstdc++.a 32/libstdc++.a
ln -sf lib64/libstdc++.a libstdc++.a
ln -sf ../lib32/libsupc++.a 32/libsupc++.a
ln -sf lib64/libsupc++.a libsupc++.a
ln -sf ../lib32/libmudflap.a 32/libmudflap.a
ln -sf lib64/libmudflap.a libmudflap.a
ln -sf ../lib32/libmudflapth.a 32/libmudflapth.a
ln -sf lib64/libmudflapth.a libmudflapth.a
%if %{build_java}
ln -sf ../lib32/libgcj_bc.so 32/libgcj_bc.so
ln -sf lib64/libgcj_bc.so libgcj_bc.so
%endif
%if %{build_ada}
ln -sf ../lib32/adainclude 32/adainclude
ln -sf lib64/adainclude adainclude
ln -sf ../lib32/adalib 32/adalib
ln -sf lib64/adalib adalib
%endif
%else
%ifarch %{multilib_64_archs}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libstdc++.a 32/libstdc++.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libsupc++.a 32/libsupc++.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libmudflap.a 32/libmudflap.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libmudflapth.a 32/libmudflapth.a
%if %{build_java}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libgcj_bc.so 32/libgcj_bc.so
%endif
%if %{build_ada}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/adainclude 32/adainclude
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/adalib 32/adalib
%endif
%endif
%endif

# Strip debug info from Fortran/ObjC/Java static libraries
strip -g `find . \( -name libgfortran.a -o -name libobjc.a -o -name libgomp.a \
		    -o -name libmudflap.a -o -name libmudflapth.a \
		    -o -name libgcc.a -o -name libgcov.a \) -a -type f`
popd
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgfortran.so.3.*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgomp.so.1.*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libmudflap{,th}.so.0.*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libobjc.so.2.*

%if %{build_ada}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgnarl*so*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgnat*so*
%endif

mv $FULLPATH/include-fixed/syslimits.h $FULLPATH/include/syslimits.h
mv $FULLPATH/include-fixed/limits.h $FULLPATH/include/limits.h
for h in `find $FULLPATH/include -name \*.h`; do
  if grep -q 'It has been auto-edited by fixincludes from' $h; then
    rh=`grep -A2 'It has been auto-edited by fixincludes from' $h | tail -1 | sed 's|^.*"\(.*\)".*$|\1|'`
    diff -up $rh $h || :
    rm -f $h
  fi
done

cat > %{buildroot}%{_prefix}/bin/c89 <<"EOF"
#!/bin/sh
fl="-std=c89"
for opt; do
  case "$opt" in
    -ansi|-std=c89|-std=iso9899:1990) fl="";;
    -std=*) echo "`basename $0` called with non ANSI/ISO C option $opt" >&2
	    exit 1;;
  esac
done
exec gcc $fl ${1+"$@"}
EOF
cat > %{buildroot}%{_prefix}/bin/c99 <<"EOF"
#!/bin/sh
fl="-std=c99"
for opt; do
  case "$opt" in
    -std=c99|-std=iso9899:1999) fl="";;
    -std=*) echo "`basename $0` called with non ISO C99 option $opt" >&2
	    exit 1;;
  esac
done
exec gcc $fl ${1+"$@"}
EOF
chmod 755 %{buildroot}%{_prefix}/bin/c?9

mkdir -p %{buildroot}%{_prefix}/sbin
gcc -static -Os %{SOURCE1} -o %{buildroot}%{_prefix}/sbin/libgcc_post_upgrade
strip %{buildroot}%{_prefix}/sbin/libgcc_post_upgrade

cd ..
%find_lang %{name}
%find_lang cpplib

# Remove binaries we will not be including, so that they don't end up in
# gcc-debuginfo
rm -f %{buildroot}%{_prefix}/%{_lib}/{libffi*,libiberty.a}
rm -f $FULLEPATH/install-tools/{mkheaders,fixincl}
rm -f %{buildroot}%{_prefix}/lib/{32,64}/libiberty.a
rm -f %{buildroot}%{_prefix}/%{_lib}/libssp*
rm -f %{buildroot}%{_prefix}/bin/gnative2ascii

%ifarch %{multilib_64_archs}
# Remove libraries for the other arch on multilib arches
rm -f %{buildroot}%{_prefix}/lib/lib*.so*
rm -f %{buildroot}%{_prefix}/lib/lib*.a
%else
%ifarch sparcv9 ppc
rm -f %{buildroot}%{_prefix}/lib64/lib*.so*
rm -f %{buildroot}%{_prefix}/lib64/lib*.a
%endif
%endif

%if %{build_java}
mkdir -p %{buildroot}%{_prefix}/share/java/gcj-endorsed \
	 %{buildroot}%{_prefix}/%{_lib}/gcj-%{version}/classmap.db.d
chmod 755 %{buildroot}%{_prefix}/share/java/gcj-endorsed \
	  %{buildroot}%{_prefix}/%{_lib}/gcj-%{version} \
	  %{buildroot}%{_prefix}/%{_lib}/gcj-%{version}/classmap.db.d
touch %{buildroot}%{_prefix}/%{_lib}/gcj-%{version}/classmap.db
%endif

%check
cd obj-%{gcc_target_platform}

%if %{build_java}
export PATH=`pwd`/../fastjar-%{fastjar_ver}/obj-%{gcc_target_platform}${PATH:+:$PATH}
%if !%{bootstrap_java}
export PATH=`pwd`/java_hacks${PATH:+:$PATH}
%endif
%endif

# run the tests.
make %{?_smp_mflags} -k check ALT_CC_UNDER_TEST=gcc ALT_CXX_UNDER_TEST=g++ RUNTESTFLAGS="--target_board=unix/'{,-fstack-protector}'" || :
echo ====================TESTING=========================
( LC_ALL=C ../contrib/test_summary || : ) 2>&1 | sed -n '/^cat.*EOF/,/^EOF/{/^cat.*EOF/d;/^EOF/d;/^LAST_UPDATED:/d;p;}'
echo ====================TESTING END=====================
mkdir testlogs-%{_target_platform}-%{version}-%{release}
for i in `find . -name \*.log | grep -F testsuite/ | grep -v 'config.log\|acats.*/tests/'`; do
  ln $i testlogs-%{_target_platform}-%{version}-%{release}/ || :
done
tar cf - testlogs-%{_target_platform}-%{version}-%{release} | bzip2 -9c \
  | uuencode testlogs-%{_target_platform}.tar.bz2 || :
rm -rf testlogs-%{_target_platform}-%{version}-%{release}

%clean
rm -rf %{buildroot}

%post
if [ -f %{_infodir}/gcc.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/gcc.info.gz || :
fi

%preun
if [ $1 = 0 -a -f %{_infodir}/gcc.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gcc.info.gz || :
fi

%post -n cpp
if [ -f %{_infodir}/cpp.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/cpp.info.gz || :
fi

%preun -n cpp
if [ $1 = 0 -a -f %{_infodir}/cpp.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/cpp.info.gz || :
fi

%post gfortran
if [ -f %{_infodir}/gfortran.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/gfortran.info.gz || :
fi

%preun gfortran
if [ $1 = 0 -a -f %{_infodir}/gfortran.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gfortran.info.gz || :
fi

%post java
if [ -f %{_infodir}/gcj.info.gz ]; then
/sbin/install-info \
  --info-dir=%{_infodir} %{_infodir}/gcj.info.gz || :
fi

%preun java
if [ $1 = 0 -a -f %{_infodir}/gcj.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gcj.info.gz || :
fi

%post gnat
if [ -f %{_infodir}/gnat_rm.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/gnat_rm.info.gz || :
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/gnat_ugn.info.gz || :
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/gnat-style.info.gz || :
fi

%preun gnat
if [ $1 = 0 -a -f %{_infodir}/gnat_rm.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gnat_rm.info.gz || :
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gnat_ugn.info.gz || :
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gnat-style.info.gz || :
fi

# Because glibc Prereq's libgcc and /sbin/ldconfig
# comes from glibc, it might not exist yet when
# libgcc is installed
%post -n libgcc -p %{_prefix}/sbin/libgcc_post_upgrade

%post -n libstdc++ -p /sbin/ldconfig

%postun -n libstdc++ -p /sbin/ldconfig

%post -n libobjc -p /sbin/ldconfig

%postun -n libobjc -p /sbin/ldconfig

%post -n libgcj
/sbin/ldconfig
if [ -f %{_infodir}/cp-tools.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/cp-tools.info.gz || :
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/fastjar.info.gz || :
fi

%preun -n libgcj
if [ $1 = 0 -a -f %{_infodir}/cp-tools.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/cp-tools.info.gz || :
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/fastjar.info.gz || :
fi

%postun -n libgcj -p /sbin/ldconfig

%post -n libgfortran -p /sbin/ldconfig

%postun -n libgfortran -p /sbin/ldconfig

%post -n libgnat -p /sbin/ldconfig

%postun -n libgnat -p /sbin/ldconfig

%post -n libgomp
/sbin/ldconfig
if [ -f %{_infodir}/libgomp.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/libgomp.info.gz || :
fi

%preun -n libgomp
if [ $1 = 0 -a -f %{_infodir}/libgomp.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/libgomp.info.gz || :
fi

%postun -n libgomp -p /sbin/ldconfig

%post -n libmudflap -p /sbin/ldconfig

%postun -n libmudflap -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%{_prefix}/bin/cc
%{_prefix}/bin/c89
%{_prefix}/bin/c99
%{_prefix}/bin/gcc
%{_prefix}/bin/gcov
%ifarch ppc
%{_prefix}/bin/%{_target_platform}-gcc
%endif
%ifarch sparc64 sparcv9
%{_prefix}/bin/sparc-%{_vendor}-%{_target_os}-gcc
%endif
%ifarch ppc64
%{_prefix}/bin/ppc-%{_vendor}-%{_target_os}-gcc
%endif
%{_prefix}/bin/%{gcc_target_platform}-gcc
%{_mandir}/man1/gcc.1*
%{_mandir}/man1/gcov.1*
%{_infodir}/gcc*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/lto1
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/lto-wrapper
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stddef.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdarg.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdfix.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/varargs.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/float.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/limits.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdbool.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/iso646.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/syslimits.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/unwind.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/omp.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdint.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdint-gcc.h
%ifarch %{ix86} x86_64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/emmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/pmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/tmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ammintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/smmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/nmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/bmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/wmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/immintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/x86intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/fma4intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xopintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/lwpintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/abmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/popcntintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ia32intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mm_malloc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mm3dnow.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/cpuid.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/cross-stdarg.h
%endif
%ifarch ia64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ia64intrin.h
%endif
%ifarch ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ppc-asm.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/altivec.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/spe.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/paired.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ppu_intrinsics.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/si2vmx.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/spu2vmx.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/vec_types.h
%endif
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/collect2
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.spec
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.so
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgomp.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libmudflapth.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libmudflap.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libmudflapth.so
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgomp.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmudflapth.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmudflap.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmudflapth.so
%endif
%ifarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflapth.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflap.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflapth.so
%endif
%dir %{_prefix}/libexec/getconf
%{_prefix}/libexec/getconf/default
%doc gcc/README* rpm.doc/changelogs/gcc/ChangeLog* gcc/COPYING*

%files -n cpp -f cpplib.lang
%defattr(-,root,root,-)
/lib/cpp
%{_prefix}/bin/cpp
%{_mandir}/man1/cpp.1*
%{_infodir}/cpp*
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1

%files -n libgcc
%defattr(-,root,root,-)
/%{_lib}/libgcc_s-%{gcc_version}-%{DATE}.so.1
/%{_lib}/libgcc_s.so.1
%{_prefix}/sbin/libgcc_post_upgrade
%doc gcc/COPYING.LIB

%files c++
%defattr(-,root,root,-)
%{_prefix}/bin/%{gcc_target_platform}-*++
%{_prefix}/bin/g++
%{_prefix}/bin/c++
%{_mandir}/man1/g++.1*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1plus
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libsupc++.a
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libsupc++.a
%endif
%ifarch sparcv9 ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.so
%endif
%ifarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libsupc++.a
%endif
%doc rpm.doc/changelogs/gcc/cp/ChangeLog*

%files -n libstdc++
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libstdc++.so.6*
%dir %{_datadir}/gdb
%dir %{_datadir}/gdb/auto-load
%dir %{_datadir}/gdb/auto-load/%{_prefix}
%dir %{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/
%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/libstdc*gdb.py*
%dir %{_prefix}/share/gcc-%{gcc_version}
%{_prefix}/share/gcc-%{gcc_version}/python

%files -n libstdc++-devel
%defattr(-,root,root,-)
%dir %{_prefix}/include/c++
%dir %{_prefix}/include/c++/%{gcc_version}
%{_prefix}/include/c++/%{gcc_version}/[^gjos]*
%{_prefix}/include/c++/%{gcc_version}/os*
%{_prefix}/include/c++/%{gcc_version}/s[^u]*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%if 0%{?fedora} < 14
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libsupc++.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libsupc++.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libsupc++.a
%endif
%endif
%ifnarch sparcv9 ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.so
%endif
%doc rpm.doc/changelogs/libstdc++-v3/ChangeLog* libstdc++-v3/README*

%files -n libstdc++-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libsupc++.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libsupc++.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libsupc++.a
%endif

%if %{build_libstdcxx_docs}
%files -n libstdc++-docs
%defattr(-,root,root)
%{_mandir}/man3/*
%doc rpm.doc/libstdc++-v3/html
%endif

%files objc
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/objc
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1obj
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libobjc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libobjc.so
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libobjc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libobjc.so
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libobjc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libobjc.so
%endif
%doc rpm.doc/objc/*
%doc libobjc/THREADS* rpm.doc/changelogs/libobjc/ChangeLog*

%files objc++
%defattr(-,root,root,-)
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1objplus

%files -n libobjc
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libobjc.so.2*

%files gfortran
%defattr(-,root,root,-)
%{_prefix}/bin/gfortran
%{_prefix}/bin/f95
%{_mandir}/man1/gfortran.1*
%{_infodir}/gfortran*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/omp_lib.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/omp_lib.f90
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/omp_lib.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/omp_lib_kinds.mod
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/f951
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortranbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortran.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortran.so
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgfortranbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgfortran.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgfortran.so
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgfortranbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgfortran.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgfortran.so
%endif
%doc rpm.doc/gfortran/*

%files -n libgfortran
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libgfortran.so.3*

%if %{build_java}
%files java
%defattr(-,root,root,-)
%{_prefix}/bin/gcj
%{_prefix}/bin/gjavah
%{_prefix}/bin/gcjh
%{_prefix}/bin/jcf-dump
%{_mandir}/man1/gcj.1*
%{_mandir}/man1/jcf-dump.1*
%{_mandir}/man1/gjavah.1*
%{_mandir}/man1/gcjh.1*
%{_infodir}/gcj*
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/jc1
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/ecj1
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/jvgenmain
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcj.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcj-tools.so
%ifarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcj_bc.so
%endif
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgij.so
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcj.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcj-tools.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcj_bc.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgij.so
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcj.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcj-tools.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcj_bc.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgij.so
%endif
%doc rpm.doc/changelogs/gcc/java/ChangeLog*

%files -n libgcj
%defattr(-,root,root,-)
%{_prefix}/bin/jv-convert
%{_prefix}/bin/gij
%{_prefix}/bin/gjar
%{_prefix}/bin/fastjar
%{_prefix}/bin/grepjar
%{_prefix}/bin/grmic
%{_prefix}/bin/grmid
%{_prefix}/bin/grmiregistry
%{_prefix}/bin/gtnameserv
%{_prefix}/bin/gkeytool
%{_prefix}/bin/gorbd
%{_prefix}/bin/gserialver
%{_prefix}/bin/gcj-dbtool
%{_prefix}/bin/gjarsigner
%{_mandir}/man1/fastjar.1*
%{_mandir}/man1/grepjar.1*
%{_mandir}/man1/gjar.1*
%{_mandir}/man1/gjarsigner.1*
%{_mandir}/man1/jv-convert.1*
%{_mandir}/man1/gij.1*
%{_mandir}/man1/grmic.1*
%{_mandir}/man1/grmiregistry.1*
%{_mandir}/man1/gcj-dbtool.1*
%{_mandir}/man1/gkeytool.1*
%{_mandir}/man1/gorbd.1*
%{_mandir}/man1/grmid.1*
%{_mandir}/man1/gserialver.1*
%{_mandir}/man1/gtnameserv.1*
%{_infodir}/fastjar.info*
%{_infodir}/cp-tools.info*
%{_prefix}/%{_lib}/libgcj.so.*
%{_prefix}/%{_lib}/libgcj-tools.so.*
%{_prefix}/%{_lib}/libgcj_bc.so.*
%{_prefix}/%{_lib}/libgij.so.*
%dir %{_prefix}/%{_lib}/gcj-%{version}
%{_prefix}/%{_lib}/gcj-%{version}/libgtkpeer.so
%{_prefix}/%{_lib}/gcj-%{version}/libgjsmalsa.so
%{_prefix}/%{_lib}/gcj-%{version}/libjawt.so
%{_prefix}/%{_lib}/gcj-%{version}/libjvm.so
%{_prefix}/%{_lib}/gcj-%{version}/libjavamath.so
%dir %{_prefix}/share/java
%{_prefix}/share/java/[^sl]*
%{_prefix}/share/java/libgcj-%{version}.jar
%dir %{_prefix}/%{_lib}/security
%config(noreplace) %{_prefix}/%{_lib}/security/classpath.security
%{_prefix}/%{_lib}/logging.properties
%dir %{_prefix}/%{_lib}/gcj-%{version}/classmap.db.d
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_prefix}/%{_lib}/gcj-%{version}/classmap.db

%files -n libgcj-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/gcj
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/jawt.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/jawt_md.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/jni.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/jni_md.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/jvmpi.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcj.spec
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libgcj_bc.so
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libgcj_bc.so
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcj_bc.so
%endif
%dir %{_prefix}/include/c++
%dir %{_prefix}/include/c++/%{gcc_version}
%{_prefix}/include/c++/%{gcc_version}/[gj]*
%{_prefix}/include/c++/%{gcc_version}/org
%{_prefix}/include/c++/%{gcc_version}/sun
%{_prefix}/%{_lib}/pkgconfig/libgcj-*.pc
%doc rpm.doc/boehm-gc/* rpm.doc/fastjar/* rpm.doc/libffi/*
%doc rpm.doc/libjava/*

%files -n libgcj-src
%defattr(-,root,root,-)
%dir %{_prefix}/share/java
%{_prefix}/share/java/src*.zip
%{_prefix}/share/java/libgcj-tools-%{version}.jar
%endif

%if %{build_ada}
%files gnat
%defattr(-,root,root,-)
%{_prefix}/bin/gnat*
%{_infodir}/gnat*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/adalib
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/adalib
%endif
%ifarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adalib
%endif
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/gnat1
%doc rpm.doc/changelogs/gcc/ada/ChangeLog*

%files -n libgnat
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libgnat-*.so
%{_prefix}/%{_lib}/libgnarl-*.so

%files -n libgnat-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/adalib
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/adalib/libgnat.a
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/adalib/libgnarl.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/adalib
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/adalib/libgnat.a
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/adalib/libgnarl.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adalib
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adalib/libgnat.a
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adalib/libgnarl.a
%endif

%files -n libgnat-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/adalib
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/adalib/libgnat.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/adalib/libgnarl.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/adalib
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/adalib/libgnat.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/adalib/libgnarl.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adalib
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adalib/libgnat.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adalib/libgnarl.a
%endif
%endif

%files -n libgomp
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libgomp.so.1*
%{_infodir}/libgomp.info*
%doc rpm.doc/changelogs/libgomp/ChangeLog*

%files -n libmudflap
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libmudflap.so.0*
%{_prefix}/%{_lib}/libmudflapth.so.0*

%files -n libmudflap-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mf-runtime.h
%if 0%{?fedora} < 14
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libmudflapth.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libmudflapth.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflapth.a
%endif
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflap.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflapth.so
%endif
%doc rpm.doc/changelogs/libmudflap/ChangeLog*

%files -n libmudflap-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libmudflapth.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libmudflapth.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflapth.a
%endif

%changelog
* Fri Nov 12 2010 Jakub Jelinek <jakub@redhat.com> 4.5.1-5
- update from gcc-4_5-branch
  - PRs bootstrap/44455, bootstrap/44621, c++/45894, c++/45983, c++/46024,
	c++/46160, c/44772, c/45969, debug/42487, debug/44832, debug/45656,
	debug/45939, fortran/42169, fortran/45748, fortran/46007,
	fortran/46140, fortran/46152, java/43839, libffi/45677,
	libfortran/45710, libgfortran/46010, libgfortran/46373,
	libstdc++/45403, libstdc++/45711, libstdc++/45924, libstdc++/45999,
	middle-end/43690, middle-end/44569, middle-end/45569,
	middle-end/45869, middle-end/46019, middle-end/46419,
	rtl-opt/46226, rtl-optimization/43358, rtl-optimization/44691,
	rtl-optimization/46237, target/42070, target/43715, target/43764,
	target/44452, target/45820, target/45843, target/45946, target/46098,
	target/46153, target/46419, tree-optimization/45314,
	tree-optimization/45752, tree-optimization/45854,
	tree-optimization/45902, tree-optimization/45982,
	tree-optimization/46099, tree-optimization/46107,
	tree-optimization/46165, tree-optimization/46167,
	tree-optimization/46177, tree-optimization/46355
- -Wunused-but-set* fix for computed goto (PR c/46015)
- fix -Wunused-but-set* for ObjC and ObjC++
- VTA backports
  - PRs bootstrap/43994, bootstrap/45630, debug/43478, debug/44023,
	debug/46171, debug/46252, debug/46255, rtl-optimization/45162,
	tree-optimization/46066
%if 0%{?fedora} > 14
- DW_OP_GNU_implicit_pointer support
%endif

* Fri Sep 24 2010 Jakub Jelinek <jakub@redhat.com> 4.5.1-4
- update from gcc-4_5-branch
  - PRs bootstrap/43847, debug/43628, fortran/45081, fortran/45595,
	java/44095, libfortran/45532, libstdc++/45398, middle-end/40386,
	middle-end/44554, middle-end/44763, middle-end/45312,
	middle-end/45567, middle-end/45678, middle-end/45704, other/45443,
	rtl-optimization/41085, rtl-optimization/41087,
	rtl-optimization/42775, rtl-optimization/44919,
	rtl-optimization/45051, rtl-optimization/45593,
	rtl-optimization/45728, target/35664, target/36502, target/40959,
	target/42313, target/44651, target/45694, target/45726,
	tree-optimization/45623, tree-optimization/45709
  - fix ICE in dwarf2out_finish (#632847, PR debug/45660)
  - fix combiner (#634757, PR rtl-optimization/45695)
- yet another -Wunused-but-set* fix for C++ consts in
  templates (PR c++/45588)
- emit slightly more compact .eh_frame

* Tue Sep  7 2010 Jakub Jelinek <jakub@redhat.com> 4.5.1-3
- update from gcc-4_5-branch
  - PRs c++/44991, c++/45315, debug/45500, fortran/45019, fortran/45186,
	fortran/45344, fortran/45489, fortran/45530, libstdc++/45283,
	lto/45496, middle-end/44632, middle-end/45292, middle-end/45423,
	middle-end/45458, middle-end/45484, rtl-optimization/44858,
	rtl-optimization/45353, rtl-optimization/45400, target/41484,
	target/45070, target/45296, target/45327, tree-optimization/45241,
	tree-optimization/45260, tree-optimization/45393
  - fix TYPENAME_TYPE handling (#620095, PRs c++/45200, c++/45293, c++/45558)

* Tue Aug 31 2010 Dennis Gilmore <dennis@ausil.us> 4.5.1-2
- enable cloog on sparc arches

* Thu Aug 12 2010 Jakub Jelinek <jakub@redhat.com> 4.5.1-1
- update from gcc-4_5-branch
  - GCC 4.5.1 release
  - PRs boehm-gc/34544, c++/45112, fortran/31588, fortran/42051,
	fortran/43954, fortran/44064, fortran/44660, fortran/44929,
	fortran/45151, libstdc++/44963, middle-end/44133, middle-end/45034,
	middle-end/45262, target/41089, target/43698, target/44805,
	testsuite/43283, tree-optimization/44914, tree-optimization/45052,
	tree-optimization/45109
  - fix VTA ICE in caller-save.c (#622060, PR debug/45259)
- fix up gdb libstdc++ pretty printing (#621717)
- fix up libgcj.so, libgij.so and libgcj-tools.so symlinks (#619156)

* Fri Jul 30 2010 Jakub Jelinek <jakub@redhat.com> 4.5.0-4
- update from gcc-4_5-branch
  - PRs c++/43016, c++/44996, c++/45008, c/45079, debug/45015, fortran/30668,
	fortran/31346, fortran/34260, fortran/40011, testsuite/38946,
	tree-optimization/44900, tree-optimization/44977
  - fix vectorizer ICE (#617492, PR tree-optimization/45047)
- use --enable-linker-build-id in configury instead of patching
  --build-id support in
- VTA backports
  - PRs debug/45055, rtl-optimization/45137, debug/45003,
	debug/45006, bootstrap/45028

* Fri Jul 16 2010 Jakub Jelinek <jakub@redhat.com> 4.5.0-3
- update from gcc-4_5-branch
  - PRs ada/43731, fortran/44773, pch/14940, testsuite/44325
  - fix vectorizer (#614375, #614814, PR tree-optimization/44886)
- fix fortran CHARACTER type SELECT CASE handling (PR fortran/40206)
- fix inline-asm check for auto-inc-dec operands (PR testsuite/44701)
- fix va_start on x86_64 (PR target/44942)

* Fri Jul  9 2010 Jakub Jelinek <jakub@redhat.com> 4.5.0-2
- update from gcc-4_5-branch
  - PRs c++/44703, fortran/44847, middle-end/41355, middle-end/44828,
	target/43888, tree-optimization/44284
- use DW_OP_const[48]u instead of DW_OP_addr before DW_OP_GNU_push_tls_address
- fix a multilib issue with *.py[oc] files in libstdc++ (#612742)
- fix up libgcj_bc.so

* Wed Jul  7 2010 Jakub Jelinek <jakub@redhat.com> 4.5.0-1
- initial 4.5 package, using newly created redhat/gcc-4_5-branch
