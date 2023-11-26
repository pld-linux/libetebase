Summary:	C library for Etebase
Summary(pl.UTF-8):	Biblioteka C do Etebase
Name:		libetebase
Version:	0.5.4
Release:	3
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/etesync/libetebase/tags
Source0:	https://github.com/etesync/libetebase/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	72adab5b63137fea914218e1247ad649
# cd %{name}-%{version}
# cargo vendor
# cd ..
# tar cJf %{name}-%{version}-vendor.tar.xz %{name}-%{version}/{vendor,Cargo.lock}
Source1:	%{name}-%{version}-vendor.tar.xz
# Source1-md5:	977ba8e9e648de63a92d3768b78219aa
URL:		https://www.etebase.com/
BuildRequires:	cargo
BuildRequires:	libsodium-devel >= 1.0.18
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	rust
# vendored too
#BuildRequires:	rust-cbindgen >= 0.14.2
Requires:	libsodium >= 1.0.18
ExclusiveArch:	%{x8664} %{ix86} x32 aarch64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_debugsource_packages	0

%description
C library for Etebase.

%description -l pl.UTF-8
Biblioteka C do Etebase.

%package devel
Summary:	Header files for Etebase library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Etebase
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for Etebase library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Etebase.

%prep
%setup -q -b1

%{__sed} -i -e '/^libdir=/ s,/lib$,/%{_lib},' etebase.pc.in

# use our offline registry
export CARGO_HOME="$(pwd)/.cargo"

mkdir -p "$CARGO_HOME"
cat >.cargo/config <<EOF
[source.crates-io]
replace-with = 'vendored-sources'

[source.vendored-sources]
directory = '$PWD/vendor'
EOF

%build
export CARGO_HOME="$(pwd)/.cargo"
export PKG_CONFIG_ALLOW_CROSS=1
export RUST_BACKTRACE=full
export SODIUM_USE_PKG_CONFIG=1

cargo -vv build --release --frozen \
%ifarch x32
	--target x86_64-unknown-linux-gnux32
%endif

%{__make} pkgconfig

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	DST_LIBRARY_DIR=$RPM_BUILD_ROOT%{_libdir} \
%ifarch x32
	MODE="x86_64-unknown-linux-gnux32/release"
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog.md LICENSE README.md
%attr(755,root,root) %{_libdir}/libetebase.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/etebase
%{_pkgconfigdir}/etebase.pc
%{_libdir}/cmake/Etebase
