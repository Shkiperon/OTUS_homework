Summary: Custom build of Asterisk for Company
Group: Applications/System
Name: asterisk
Release: 21%{?dist}
License: GPL v2
URL: http://asterisk.org/
Version: 14.7.6
BuildRoot: /home/vagrant/rpmbuild
Packager: Artiom Druz (aka Shkiperon)

Source0:	http://downloads.digium.com/pub/asterisk/releases/asterisk-%{version}.tar.gz

BuildRequires: autoconf, automake, gcc, gcc-c++, libedit-devel, jansson-devel, libuuid-devel, sqlite-devel, libxml2-devel, speex-devel, libogg-devel, libvorbis-devel, alsa-lib-devel, libcurl-devel, bison, flex, postgresql-devel, unixODBC-devel, neon-devel, lua-devel, uriparser-devel, libxslt-devel, openssl-devel, mysql-devel, bluez-libs-devel, net-snmp-devel, corosynclib-devel, newt-devel, popt-devel, libical-devel, binutils-devel, libsrtp-devel, gsm-devel, doxygen, graphviz, zlib-devel, openldap-devel, subversion, python-devel, portaudio-devel, xmlstarlet, gmime-devel, radcli-devel, freetds-devel, jack-audio-connection-kit-devel, iksemel-devel, spandsp-devel, uw-imap-devel, pjproject-devel


Requires(post,preun,postun): systemd-units >= 38
Requires: systemd-units >= 0.38
Requires(postun): /usr/sbin/groupdel
Requires(postun): /usr/sbin/userdel
Requires(pre): /bin/id
Requires(pre): /usr/sbin/groupadd
Requires(pre): /usr/sbin/useradd
Requires(pre): /usr/bin/getent
Provides: group(asterisk)
Provides: user(asterisk)

%define		skip_post_check_so	libasteriskssl.so.*
%define _noautoprovfiles %{_libdir}/asterisk/modules/.*
%define _unpackaged_files_terminate_build 0

%description
Custom build of Asterisk for Company without speexdsp-devel, libresample-devel and hoard which are in preinstall requirements. Other requirements are included.

%prep
%setup 

# Fixup makefile so sound archives aren't downloaded/installed
%{__sed} -i -e 's/^all:.*$/all:/' sounds/Makefile
%{__sed} -i -e 's/^install:.*$/install:/' sounds/Makefile


%build
%{__aclocal} -I autoconf $(find third-party/ -maxdepth 1 -type d -printf "-I %p ")
%{__autoheader}
%{__autoconf}

export WGET="/bin/true"

# be sure to invoke ./configure with our flags
cd menuselect
%{__aclocal} -I ../autoconf
%{__autoheader}
%{__autoconf}
# we need just plain cli for building
%configure \
	--without-newt \
	--without-gtk2 \
	--without-curses \
	--without-ncurses \
        %{__with pjsip pjproject}
cd ..

%configure \
	%{__without oss SDL_image} \
	%{__without bluetooth bluetooth} \
	--without-gtk2 \
	--with-gnu-ld \
	--with-gsm=/usr \
	%{__without ldap ldap} \
	%{__without oss oss} \

cp -f .cleancount .lastclean

%{__make} menuselect/menuselect
%{__make} menuselect-tree

menuselect/menuselect --disable chan_oss menuselect.makeopts
menuselect/menuselect --disable res_config_ldap menuselect.makeopts

%{__sed} -i -e 's/^MENUSELECT_OPTS_app_voicemail=.*$/MENUSELECT_OPTS_app_voicemail=FILE_STORAGE/' menuselect.makeopts
menuselect/menuselect --enable app_voicemail menuselect.makeopts

ln -s libasteriskssl.so.1 ./main/libasteriskssl.so

%{__make} DEBUG= \
	OPTIMIZE= \
	ASTVARRUNDIR=%{_localstatedir}/run/asterisk \
	ASTDATADIR=%{_datadir}/asterisk \
	ASTVARLIBDIR=%{_datadir}/asterisk \
	ASTDBDIR=%{_localstatedir}/spool/asterisk \
%{?with_verbose:NOISY_BUILD=yes} \

%if %{with apidocs}
%{__make} progdocs \
	DEBUG= \
	OPTIMIZE= \
	ASTVARRUNDIR=%{_localstatedir}/run/asterisk \
	ASTDATADIR=%{_datadir}/asterisk \
	ASTVARLIBDIR=%{_datadir}/asterisk \
	ASTDBDIR=%{_localstatedir}/spool/asterisk \
	%{?with_verbose:NOISY_BUILD=yes} \
%endif

%install
rm -rf %{buildroot}
install -d %{buildroot}{/var/{log/asterisk/cdr-csv,spool/asterisk/monitor},/etc/{sysconfig,logrotate.d}} \
	%{buildroot}%{_mandir}/man1


%{__make} -j1 install \
	DEBUG= \
	OPTIMIZE= \
	DESTDIR=%{buildroot} \
	ASTVARRUNDIR=%{_localstatedir}/run/asterisk \
	ASTDATADIR=%{_datadir}/asterisk \
	ASTVARLIBDIR=%{_datadir}/asterisk \
	ASTDBDIR=%{_localstatedir}/spool/asterisk

%{__make} -j1 samples \
	DEBUG= \
	OPTIMIZE= \
	DESTDIR=%{buildroot} \
	ASTVARRUNDIR=%{_localstatedir}/run/asterisk \
	ASTDATADIR=%{_datadir}/asterisk \
	ASTVARLIBDIR=%{_datadir}/asterisk \
	ASTDBDIR=%{_localstatedir}/spool/asterisk

# create some directories that need to be packaged
install -d %{buildroot}%{_datadir}/asterisk/moh
install -d %{buildroot}%{_datadir}/asterisk/sounds
ln -s %{_localstatedir}/lib/asterisk/licenses %{buildroot}%{_datadir}/asterisk/licenses

install -d %{buildroot}%{_localstatedir}/lib/asterisk/licenses
install -d %{buildroot}%{_localstatedir}/log/asterisk/cdr-custom
install -d %{buildroot}%{_localstatedir}/spool/asterisk/festival
install -d %{buildroot}%{_localstatedir}/spool/asterisk/monitor
install -d %{buildroot}%{_localstatedir}/spool/asterisk/outgoing
install -d %{buildroot}%{_localstatedir}/spool/asterisk/uploads

install utils/astman.1 %{buildroot}%{_mandir}/man1/astman.1

# Don't package the sample voicemail user
%{__rm} -r %{buildroot}%{_localstatedir}/spool/asterisk/voicemail/default

# Don't package example phone provision configs
%{__rm} -r %{buildroot}%{_datadir}/asterisk/phoneprov/*

# we're not using safe_asterisk
%{__rm} %{buildroot}%{_sbindir}/safe_asterisk
%{__rm} %{buildroot}%{_mandir}/man8/safe_asterisk.8*

%if %{with apidocs}
find doc/api -name '*.map' -size 0 -delete
%endif

# remove configuration files for components never built
%{__rm} %{buildroot}%{_sysconfdir}/asterisk/{app_skel,config_test,misdn,ooh323,test_sorcery,alsa,calendar,dbsep,hep,meetme,osp,res_curl,res_pktccops,res_snmp,unistim}.conf

# remove configuration files for disabled optional components
%{__rm} %{buildroot}%{_sysconfdir}/asterisk/oss.conf
%{__rm} %{buildroot}%{_sysconfdir}/asterisk/res_ldap.conf
%{__rm} %{buildroot}%{_sysconfdir}/asterisk/extensions.lua

%{__rm} %{buildroot}%{_libdir}/asterisk/modules/app_page.so
%{__rm} %{buildroot}%{_libdir}/asterisk/modules/chan_unistim.so
%{__rm} %{buildroot}%{_libdir}/asterisk/modules/codec_lpc10.so
%{__rm} %{buildroot}%{_libdir}/asterisk/modules/codec_resample.so
%{__rm} %{buildroot}%{_libdir}/asterisk/modules/res_calendar.so
%{__rm} %{buildroot}%{_libdir}/asterisk/modules/res_calendar_*.so
%{__rm} %{buildroot}%{_libdir}/asterisk/modules/res_format_attr_vp8.so

%{__rm} -f %{buildroot}%{_sbindir}/check_expr
%{__rm} -f %{buildroot}%{_sbindir}/check_expr2
%{__rm} %{buildroot}%{_sbindir}/rasterisk

%{__rm} -r %{buildroot}/usr/include/asterisk/doxygen

%clean
rm -rf %{buildroot}

%pre
/usr/bin/getent group asterisk || /usr/sbin/groupadd -g 188 asterisk
/usr/bin/getent passwd asterisk || /usr/sbin/useradd -g 188 -u 188 -r -d /var/lib/asterisk -s /sbin/nologin asterisk

%postun
if [ "$1" = 0 ]; then
	%userremove asterisk
	%groupremove asterisk
fi
%systemd_postun_with_restart %{name}.service

%post
/sbin/ldconfig
/sbin/chkconfig --add asterisk
# use -n (NOOP) as restart would be breaking all current calls.
%service -n asterisk restart "Asterisk daemon"
%systemd_post %{name}.service

%preun
if [ "$1" = "0" ]; then
	%service asterisk stop
	/sbin/chkconfig --del asterisk
fi
%systemd_preun %{name}.service

%triggerpostun -- %{name} < 1.6.1.12-0.1
# chown to asterisk previously root owned files
# loose one (not one that cames from rpm), as we're not trying to split the
# hair with file permission bits.
chown -R asterisk:asterisk /var/spool/asterisk
chown -R asterisk:asterisk /var/lib/asterisk

%triggerpostun -- %{name} < 12.0.0
%systemd_trigger %{name}.service

%files
%defattr(644,asterisk,asterisk,755)
%doc doc/asterisk.sgml

%attr(755,asterisk,asterisk) %{_sbindir}/astcanary
%attr(755,asterisk,asterisk) %{_sbindir}/astdb2bdb
%attr(755,asterisk,asterisk) %{_sbindir}/astdb2sqlite3
%attr(755,asterisk,asterisk) %{_sbindir}/asterisk
%attr(755,asterisk,asterisk) %{_sbindir}/astgenkey
%attr(755,asterisk,asterisk) %{_sbindir}/astversion
%attr(755,asterisk,asterisk) %{_sbindir}/autosupport
%{_mandir}/man8/astdb2bdb.8*
%{_mandir}/man8/astdb2sqlite3.8*
%{_mandir}/man8/asterisk.8*
%{_mandir}/man8/astgenkey.8*
%{_mandir}/man8/autosupport.8*
%{_mandir}/man1/astman.1.*

%attr(750,asterisk,asterisk) %dir %{_sysconfdir}/asterisk
%attr(640,asterisk,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/*.conf
%attr(640,asterisk,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/*.adsi
%attr(640,asterisk,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/*.ael
%attr(640,asterisk,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/*.timers

%{_libdir}/libasteriskssl.so.1

%{_prefix}/lib64/libasteriskssl.so

%dir %{_libdir}/asterisk
%dir %{_libdir}/asterisk/modules

%attr(755,asterisk,asterisk) %{_libdir}/asterisk/modules/app_*.so
%attr(755,asterisk,asterisk) %{_libdir}/asterisk/modules/bridge_*.so
%attr(755,asterisk,asterisk) %{_libdir}/asterisk/modules/cdr_*.so
%attr(755,asterisk,asterisk) %{_libdir}/asterisk/modules/cel_*.so
%attr(755,asterisk,asterisk) %{_libdir}/asterisk/modules/chan_*.so
%attr(755,asterisk,asterisk) %{_libdir}/asterisk/modules/codec_*.so
%attr(755,asterisk,asterisk) %{_libdir}/asterisk/modules/format_*.so
%attr(755,asterisk,asterisk) %{_libdir}/asterisk/modules/func_*.so
%attr(755,asterisk,asterisk) %{_libdir}/asterisk/modules/pbx_*.so
%attr(755,asterisk,asterisk) %{_libdir}/asterisk/modules/res_*.so

%dir %{_datadir}/asterisk
%dir %{_datadir}/asterisk/agi-bin
%dir %{_datadir}/asterisk/firmware
%dir %{_datadir}/asterisk/firmware/iax
%dir %{_datadir}/asterisk/images
%dir %{_datadir}/asterisk/moh
%dir %{_datadir}/asterisk/scripts
%dir %{_datadir}/asterisk/sounds
%dir %{_datadir}/asterisk/static-http
%dir %attr(750,asterisk,asterisk) %{_datadir}/asterisk/keys
%{_datadir}/asterisk/images/*.jpg
%{_datadir}/asterisk/phoneprov
%{_datadir}/asterisk/scripts/ast_*
%{_datadir}/asterisk/scripts/refcounter.*
%{_datadir}/asterisk/static-http/*.html
%{_datadir}/asterisk/static-http/*.js
%{_datadir}/asterisk/static-http/*.css
%{_datadir}/asterisk/static-http/*.xml
%{_datadir}/asterisk/static-http/*.xslt
%{_datadir}/asterisk/licenses

%attr(755,asterisk,asterisk) %{_includedir}/asterisk.h
%attr(755,asterisk,asterisk) %{_includedir}/asterisk/*.h

%dir %{_datadir}/asterisk/documentation
%{_datadir}/asterisk/documentation/appdocsxml.dtd
%{_datadir}/asterisk/documentation/appdocsxml.xslt
%{_datadir}/asterisk/documentation/core-en_US.xml

%dir %{_datadir}/asterisk/rest-api
%{_datadir}/asterisk/rest-api/*.json

%attr(770,asterisk,asterisk) %dir %{_localstatedir}/lib/asterisk
%dir %attr(750,asterisk,asterisk) %{_localstatedir}/lib/asterisk/licenses

%attr(770,asterisk,asterisk) %dir %{_localstatedir}/log/asterisk
%attr(770,asterisk,asterisk) %dir %{_localstatedir}/log/asterisk/cdr-csv
%attr(770,asterisk,asterisk) %dir %{_localstatedir}/log/asterisk/cdr-custom

%attr(770,asterisk,asterisk) %dir %{_localstatedir}/spool/asterisk
%attr(770,asterisk,asterisk) %dir %{_localstatedir}/spool/asterisk/monitor
%attr(770,asterisk,asterisk) %dir %{_localstatedir}/spool/asterisk/outgoing
%attr(770,asterisk,asterisk) %dir %{_localstatedir}/spool/asterisk/tmp
%attr(770,asterisk,asterisk) %dir %{_localstatedir}/spool/asterisk/uploads
%attr(770,asterisk,asterisk) %dir %{_localstatedir}/spool/asterisk/voicemail

%attr(775,asterisk,asterisk) %dir %{_localstatedir}/run/asterisk

%if %{with apidocs}
%files apidocs
%defattr(644,asterisk,asterisk,755)
%doc doc/api/*
%endif

%if %{with ilbc}
%files ilbc
%defattr(644,asterisk,asterisk,755)
%attr(755,asterisk,asterisk) %{_libdir}/asterisk/modules/codec_ilbc.so
%attr(755,asterisk,asterisk) %{_libdir}/asterisk/modules/format_ilbc.so
%endif

%if %{with pjsip}
%files pjsip
%defattr(644,asterisk,asterisk,755)
%attr(640,asterisk,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/pj*.conf
%attr(640,asterisk,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/hep.conf
%endif


%if %{with sqlite2}
%files sqlite2
%defattr(644,asterisk,asterisk,755)
%attr(640,asterisk,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/res_config_sqlite.conf
%attr(755,asterisk,asterisk) %{_libdir}/asterisk/modules/res_config_sqlite.so
%endif

