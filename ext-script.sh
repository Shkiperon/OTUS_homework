#!/bin/bash
mkdir -p ~root/.ssh; cp ~vagrant/.ssh/auth* ~root/.ssh

echo "Start provision script of RPMBuilder VM for Asterisk 13"

yum update
yum -y install rpmdevtools rpm-build wget
wget https://downloads.asterisk.org/pub/telephony/asterisk/asterisk-13-current.tar.gz
mv ./asterisk-13-current.tar.gz /home/vagrant/
yum install -y epel-release
yum install -y --skip-broken --assumeyes gcc gcc-c++ libedit-devel jansson-devel libuuid-devel sqlite-devel libxml2-devel speex-devel speexdsp-devel libogg-devel libvorbis-devel alsa-lib-devel portaudio-devel libcurl-devel xmlstarlet bison flex postgresql-devel unixODBC-devel neon-devel gmime-devel lua-devel uriparser-devel libxslt-devel openssl-devel mysql-devel bluez-libs-devel radcli-devel freetds-devel jack-audio-connection-kit-devel net-snmp-devel iksemel-devel corosynclib-devel newt-devel popt-devel libical-devel spandsp-devel libresample-devel uw-imap-devel binutils-devel libsrtp-devel gsm-devel doxygen graphviz zlib-devel openldap-devel hoard subversion python-devel kobo-rpmlib
echo "Run 'rpmdev-setuptree' after connecting via SSH"

echo "Configuration has been finished. Enjoy :-)"
