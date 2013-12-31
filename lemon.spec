# TODO: coin support
#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
%bcond_with	cplex		# CPLEX support [IBM proprietary]
%bcond_without	glpk		# GLPK support
%bcond_with	soplex		# SoPlex support
#
Summary:	Library of Efficient Models and Optimization in Networks
Summary(pl.UTF-8):	Biblioteka wydajnych modeli i optymalizacji w sieciach
Name:		lemon
Version:	1.2.4
Release:	1
License:	Boost v1.0
Group:		Libraries
Source0:	http://lemon.cs.elte.hu/pub/sources/%{name}-%{version}.tar.gz
# Source0-md5:	fd89e8bf5035b02e2622a48ac7fe0641
Patch0:		%{name}-glpk.patch
URL:		http://lemon.cs.elte.hu/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	doxygen
BuildRequires:	ghostscript
%{?with_glpk:BuildRequires:	glpk-devel >= 4.33}
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	python
%{?with_soplex:BuildRequires:	soplex-devel}
%{?with_glpk:Requires:	glpk >= 4.33}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LEMON stands for Library for Efficient Modeling and Optimization in
Networks. It is a C++ template library providing efficient
implementations of common data structures and algorithms with focus on
combinatorial optimization tasks connected mainly with graphs and
networks.

%description -l pl.UTF-8
LEMON to skrót od Library for Efficient Modeling and Optimization in
Networks (biblioteka do wydajnego modelowania i optymalizacji w
sieciach). Jest to biblioteka szablonów C++ udostępniająca wydajne
implementacje popularnych struktur danych i algorytmów przeznaczonych
do zadań optymalizacji kombinatorycznej, związanych głównie z grafami
i sieciami.

%package devel
Summary:	Header files for LEMON library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki LEMON
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%{?with_glpk:Requires:	glpk-devel >= 4.33}
Requires:	libstdc++-devel
%{?with_soplex:Requires:	soplex-devel}

%description devel
Header files for LEMON library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki LEMON.

%package static
Summary:	Static LEMON library
Summary(pl.UTF-8):	Statyczna biblioteka LEMON
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static LEMON library.

%description static -l pl.UTF-8
Statyczna biblioteka LEMON.

%package apidocs
Summary:	LEMON API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki LEMON
Group:		Documentation

%description apidocs
API documentation for LEMON library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki LEMON.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-shared \
	%{!?with_static_libs:--disable-static} \
	%{!?with_cplex:--without-cplex} \
	%{!?with_glpk:--without-glpk} \
	%{!?with_soplex:--without-soplex} \
	%{?with_soplex:--with-soplex-includedir=/usr/include/soplex}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE NEWS README
%attr(755,root,root) %{_bindir}/dimacs-solver
%attr(755,root,root) %{_bindir}/dimacs-to-lgf
%attr(755,root,root) %{_bindir}/lemon-0.x-to-1.x.sh
%attr(755,root,root) %{_bindir}/lgf-gen
%attr(755,root,root) %{_libdir}/libemon.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libemon.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libemon.so
%{_includedir}/lemon
%{_pkgconfigdir}/lemon.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libemon.a
%endif

%files apidocs
%defattr(644,root,root,755)
%doc doc/html/*
