# git describe --tags HEAD
%define		gitrev	3.5.357

Summary:	DAW and MIDI sequencer
Name:		ardour3
Version:	3.5.357
Release:	1
License:	GPL v2
Group:		Libraries
# git clone git://git.ardour.org/ardour/ardour.git
# git archive --format=tar --prefix=ardour-3.2/ HEAD | xz -c > ardour-3.2.tar.xz
Source0:	ardour-%{version}.tar.xz
# Source0-md5:	8cc62ed2ea7fb3c5a66b5078c69d1faf
Patch0:		%{name}-libs.patch
Patch1:		%{name}-wscript.patch
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
%patch1 -p1

%{__sed} -i "s|debug_by_default=True|debug_by_default=False|" wscript

cat > libs/ardour/revision.cc << EOF
#include "ardour/revision.h"
namespace ARDOUR { const char* revision = "%{version}"; }
EOF

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
%dir %{_libdir}/ardour3/backends
%dir %{_libdir}/ardour3/engines
%dir %{_libdir}/ardour3/panners
%dir %{_libdir}/ardour3/surfaces
%dir %{_libdir}/ardour3/vamp
%attr(755,root,root) %{_libdir}/ardour3/ardour-%{version}
%attr(755,root,root) %{_libdir}/ardour3/sanityCheck
%attr(755,root,root) %{_libdir}/ardour3/lib*.so*
%attr(755,root,root) %{_libdir}/ardour3/*/lib*.so*
%{_datadir}/ardour3

%dir %{_libdir}/lv2/reasonablesynth.lv2
%attr(755,root,root) %{_libdir}/lv2/reasonablesynth.lv2/reasonablesynth.so
%{_libdir}/lv2/reasonablesynth.lv2/manifest.ttl
%{_libdir}/lv2/reasonablesynth.lv2/reasonablesynth.ttl

