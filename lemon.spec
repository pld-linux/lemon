# TODO: coin support
#
# Conditional build:
%bcond_with	coin		# COIN solver backend
%bcond_with	cplex		# ILOG (CPLEX) solver backend [IBM proprietary]
%bcond_without	glpk		# GLPK solver backend
%bcond_with	soplex		# SoPlex solver backend
#
Summary:	Library of Efficient Models and Optimization in Networks
Summary(pl.UTF-8):	Biblioteka wydajnych modeli i optymalizacji w sieciach
Name:		lemon
Version:	1.3.1
Release:	1
License:	Boost v1.0
Group:		Libraries
Source0:	http://lemon.cs.elte.hu/pub/sources/%{name}-%{version}.tar.gz
# Source0-md5:	e89f887559113b68657eca67cf3329b5
Patch0:		%{name}-libdir.patch
URL:		http://lemon.cs.elte.hu/
%if %{with coin}
BuildRequires:	CoinCbc-devel
BuildRequires:	CoinCbcSolver-devel
BuildRequires:	CoinCgl-devel
BuildRequires:	CoinClp-devel
BuildRequires:	CoinOsi-devel
BuildRequires:	CoinOsiCbc-devel
BuildRequires:	CoinOsiClp-devel
BuildRequires:	CoinUtils-devel
%endif
BuildRequires:	cmake >= 2.8
BuildRequires:	doxygen
BuildRequires:	ghostscript
%{?with_glpk:BuildRequires:	glpk-devel >= 4.33}
BuildRequires:	libstdc++-devel
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
Requires:	libstdc++-devel
Obsoletes:	lemon-static

%description devel
Header files for LEMON library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki LEMON.

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
%patch -P0 -p1

%build
install -d build
cd build
%cmake .. \
	%{!?with_coin:-DLEMON_ENABLE_COIN=OFF} \
	%{!?with_glpk:-DLEMON_ENABLE_GLPK=OFF} \
	%{!?with_cplex:-DLEMON_ENABLE_ILOG=OFF} \
	%{!?with_soplex:-DLEMON_ENABLE_SOPLEX=OFF}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

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
%attr(755,root,root) %{_libdir}/libemon.so.%{version}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libemon.so
%{_includedir}/lemon
%{_pkgconfigdir}/lemon.pc
%dir %{_datadir}/lemon
%{_datadir}/lemon/cmake

%files apidocs
%defattr(644,root,root,755)
%{_docdir}/lemon
