Summary:	DAW and MIDI sequencer
Name:		ardour3
Version:	3.0
Release:	1
License:	GPL v2
Group:		Libraries
Source0:	ardour-%{version}.tar.bz2
# Source0-md5:	23297b15cb541e0b3c5c05a2fdd9bcca
Patch0:		%{name}-libs.patch
BuildRequires:	alsa-lib-devel
BuildRequires:	aubio-devel
BuildRequires:	aubio-devel
BuildRequires:	boost-devel
BuildRequires:	curl-devel
BuildRequires:	gtkmm-devel
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	libgnomecanvasmm-devel
BuildRequires:	liblilv-devel
BuildRequires:	liblo-devel
BuildRequires:	liblrdf-devel
BuildRequires:	libsamplerate-devel
BuildRequires:	libserd-devel
BuildRequires:	libsndfile-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libsuil-devel
BuildRequires:	libxml2-devel
BuildRequires:	lv2-devel
BuildRequires:	pkg-config
Requires:	jack-audio-connection-kit
Requires:	libsuil-gui-support
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		skip_post_check_so	libardour.so.*

%description
Digital Audio Workstation and MIDI sequencer.

%prep
%setup -qn ardour-%{version}
%patch0 -p1

%{__sed} -i "s|debug_by_default=True|debug_by_default=False|" wscript

%build
export CC="%{__cc}"
export CXX="%{__cxx}"
export CFLAGS="%{rpmcflags}"
export CXXFLAGS="%{rpmcxxflags}"
export LDFLAGS="%{rpmldflags}"
./waf configure \
	--configdir=%{_datadir}	\
	--prefix=%{_prefix}	\
	--libdir=%{_libdir}	\
	--mandir=%{_mandir}	\
	--freedesktop		\
	--nocache		\
	--noconfirm		\
	--no-phone-home
./waf -v build

%install
rm -rf $RPM_BUILD_ROOT

./waf -v install	\
	--destdir=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/ardour3
%dir %{_libdir}/ardour3
%dir %{_libdir}/ardour3/engines
%dir %{_libdir}/ardour3/panners
%dir %{_libdir}/ardour3/surfaces
%dir %{_libdir}/ardour3/vamp
%attr(755,root,root) %{_libdir}/ardour3/ardour-3.0
%attr(755,root,root) %{_libdir}/ardour3/sanityCheck
%attr(755,root,root) %{_libdir}/ardour3/lib*.so*
%attr(755,root,root) %{_libdir}/ardour3/*/lib*.so*
%{_datadir}/ardour3

