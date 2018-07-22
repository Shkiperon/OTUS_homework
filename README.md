My spared 14th and 16th homeworks in OTUS online school on course "Linux system administrator".
After 'vagrant up' you can:
1) Connect to centralRouter, and run command:
   '/home/vagrant/knock.sh 192.168.255.1 7777 5555 3333 && ssh vagrant@192.168.255.1'
   It will open for you access via SSH to inetRouter (port-knocking), and authorize you on it via SSH-key
2) Connect to inetRouter2, and look at IPv4 address on eth2, and open in your host browser link http://$IPv4:8080. It will be open nginx web-site, which run on centralServer on 80/TCP.
