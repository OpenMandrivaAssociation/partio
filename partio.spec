%define major 1
%define libname %mklibname partio
%define devname %mklibname partio -d
%bcond tests 1

Name:		partio
Version:	1.20.0
Release:	2
Summary:	Library for particle IO and manipulation
License:	BSD-3-Clause-Modification
Group:		System/Libraries
URL:		https://github.com/wdas/partio
Source0:	https://github.com/wdas/partio/archive/v%{version}/%{name}-%{version}.tar.gz
Source100:	%{name}.rpmlintrc

BuildSystem:	cmake
BuildOption:	-DCMAKE_PREFIX_PATH="%{_prefix}"
BuildOption:	-DCMAKE_INSTALL_DOCDIR="%{_docdir}/%{name}"

BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	fdupes
BuildRequires:	help2man
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glut)
BuildRequires:	pkgconfig(gtest)
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	swig
%if %{with tests}
BuildRequires:	python%{pyver}dist(pytest)
%endif

%description
C++ (with python bindings) library for easily reading/writing/manipulating
common animation particle formats such as PDB, BGEO, PTC.

%package -n %{libname}
Summary:	Core %{name} libraries
Group:		System/Libraries

%description -n %{libname}
C++ (with python bindings) library for easily reading/writing/manipulating
common animation particle formats such as PDB, BGEO, PTC.

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
# Provide this to avoid using hardcoded lib/lib64 as BRs
Provides: %{name}-devel = %{EVRD}
Requires:	%{libname} = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

%package doc
Summary:	Documentation for %{name}
Requires:	%{name} = %{EVRD}
BuildArch:	noarch

%description doc
Documentation for %{name}.

%package -n python-%{name}
Summary:	Python bindings for %{libname}

%description -n python-%{name}
Pyhton bindings for %{libname}

%prep -a
# Fix shebangs
sed -i 's:^#!/usr/bin/env python:#!%{__python}:' src/tools/*.py

%install -a
# We dont want these
find %{buildroot} -name '*.la' -exec rm -f {} ';'

# Set executable bit on installed python scripts
chmod +x %{buildroot}%{python_sitearch}/*.py

# Remove all tests from buildroot
rm -rf %{buildroot}%{_datadir}/%{name}/test

# Generate and install man pages
install -d '%{buildroot}%{_mandir}/man1'
for cmd in %{buildroot}%{_bindir}/*
do
  PYTHONPATH='%{buildroot}%{python_sitearch}' \
  LD_LIBRARY_PATH='%{buildroot}%{_libdir}' \
      help2man \
      --no-info --no-discard-stderr --version-string='%{version}' \
      --output="%{buildroot}%{_mandir}/man1/$(basename "${cmd}").1" \
      "${cmd}"
done

%if %{with tests}
%check
export PYTHONPATH="%{buildroot}%{python_sitearch}"
export LD_LIBRARY_PATH="%{buildroot}%{_libdir}"
ctest --verbose --test-dir=_OMV_rpm_build
%endif

%files
%doc README.md
%license LICENSE
%{_bindir}/part{attr,convert,edit,info,inspect,json,view}
%{_datadir}/swig/%{name}.i
%{_mandir}/man1/part{attr,convert,edit,info,inspect,json,view}.1*

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

%files -n %{devname}
%{_includedir}/Partio{,Attribute,Iterator,Vec3}.h
%{_libdir}/lib%{name}.so

%files doc
%doc %{_docdir}/%{name}/html

%files -n python-%{name}
%{python_sitearch}/_%{name}.so
%{python_sitearch}/part{edit,inspect,io,json}.py
