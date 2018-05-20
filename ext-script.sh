#!/bin/bash
mkdir -p ~root/.ssh; cp ~vagrant/.ssh/auth* ~root/.ssh

echo "Start provision script"

#Phase 1
mv /vagrant/shkiperonsvc-env /etc/sysconfig/shkiperonsvc
mv /vagrant/shkiperonsvc.sh /usr/local/bin/
mv /vagrant/shkiperonsvc-unit /lib/systemd/system/shkiperonsvc.service
mv /vagrant/test-file-for-shkiperonsvc.log /var/log/
systemctl enable shkiperonsvc; systemctl start shkiperonsvc; systemctl status shkiperonsvc

#Phase 2
yum -y install epel-release
yum -y install spawn-fcgi
mv /vagrant/spawn-fcgi.service /lib/systemd/system/
echo "Changing spawn-fscgi to unit-script instead init.d"
mv /etc/init.d/spawn-fcgi /root/spawn-fcgi.init-bck
{
  echo 'SOCKET=/var/run/php-fcgi.sock';
  echo 'OPTIONS="-u apache -g apache -s $SOCKET -S -M 0600 -C 32 -F 1 -P /var/run/spawn-fcgi.pid -- /usr/bin/php-cgi"';
} >> /etc/sysconfig/spawn-fcgi
systemctl enable spawn-fcgi

#Phase 3
yum -y install httpd
mv /etc/httpd/conf/httpd.conf /etc/httpd/conf/httpd-main.conf
systemctl stop httpd; systemctl disable httpd; mv /lib/systemd/system/httpd.service /root/httpd.service-bck
mv /vagrant/httpd.service.modified /lib/systemd/system/httpd@.service; systemctl enable httpd@main; systemctl start httpd@main;
systemctl status httpd@main

echo "Configuration has been finished. Enjoy :-)"
