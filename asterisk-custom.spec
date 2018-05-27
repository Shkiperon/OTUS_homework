Summary: Custom build of Asterisk for Company
%define version 13
Group: Infrastructure Server
Name: asterisk-custom
Prefix: /usr
Provides: asterisk-custom
Release: 21%{?dist}
License: GPLv2
Source: asterisk-%{version}-current.tar.gz
URL: http://downloads.asterisk.org/pub/telephony/asterisk
Version: %{version}
BuildRoot: /home/vagrant/rpmbuild
Packager: Artiom Druz (aka Shkiperon)

BuildRequires: gcc, gcc-c++, libedit-devel, jansson-devel, libuuid-devel, sqlite-devel, libxml2-devel, speex-devel, libogg-devel, libvorbis-devel, alsa-lib-devel, libcurl-devel, bison, flex, postgresql-devel, unixODBC-devel, neon-devel, lua-devel, uriparser-devel, libxslt-devel, openssl-devel, mysql-devel, bluez-libs-devel, net-snmp-devel, corosynclib-devel, newt-devel, popt-devel, libical-devel, binutils-devel, libsrtp-devel, gsm-devel, doxygen, graphviz, zlib-devel, openldap-devel, subversion, python-devel, portaudio-devel, xmlstarlet, gmime-devel, radcli-devel, freetds-devel, jack-audio-connection-kit-devel, iksemel-devel, spandsp-devel, uw-imap-devel

%description
Custom build of Asterisk for Company without speexdsp-devel, libresample-devel and hoard which are in preinstall requirements. Other requirements are included.

%prep
%setup -q -n asterisk-13.21.0

%build
%configure
make menuselect
make %{?_smp_mflags}
./contrib/scripts/get_mp3_source.sh

%install
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}
