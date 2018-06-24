# -*- mode: ruby -*-
# vim: set ft=ruby :

MACHINES = {

  :server => {
        :box_name => "centos/7",
        :public => {adapter: 4},
        :net => [
                   {ip: '192.168.240.1', adapter: 2, netmask: "255.255.255.0", virtualbox__intnet: "dir-net"},
                   {ip: '192.168.250.1', adapter: 3, netmask: "255.255.255.0", virtualbox__intnet: "hw-net"},
                ]
  },

  :client => {
        :box_name => "centos/7",
        :net => [
                   {ip: '192.168.240.2', adapter: 2, netmask: "255.255.255.0", virtualbox__intnet: "dir-net"},
                   {ip: '192.168.250.2', adapter: 3, netmask: "255.255.255.0", virtualbox__intnet: "hw-net"},
                ]
  },

}

Vagrant.configure("2") do |config|

  MACHINES.each do |boxname, boxconfig|

    config.vm.define boxname do |box|

        box.vm.box = boxconfig[:box_name]
        box.vm.host_name = boxname.to_s

        boxconfig[:net].each do |ipconf|
          box.vm.network "private_network", ipconf
        end

        if boxconfig.key?(:public)
          box.vm.network "public_network", boxconfig[:public]
        end

        box.vm.provider :virtualbox do |vb|
          vb.memory = 256
        end

        box.vm.provision "shell", inline: <<-SHELL
          mkdir -p ~root/.ssh
          cp ~vagrant/.ssh/auth* ~root/.ssh
          sysctl net.ipv4.conf.all.forwarding=1
          sysctl net.ipv4.ip_forward=1
          nmcli connection reload
          yum install -y epel-release
          echo "First phase"
          yum install -y openvpn easy-rsa
          mkdir -p /home/vagrant/.ssh/
          cp /vagrant/vagrant_ovpn /home/vagrant/.ssh/id_rsa && chmod 0600 /home/vagrant/.ssh/id_rsa
          chown -R vagrant:vagrant /home/vagrant/.ssh
          mkdir -p ~/.ssh && cat /vagrant/vagrant_ovpn.pub >> ~/.ssh/authorized_keys && chmod 0600 ~/.ssh/authorized_keys
          cp /vagrant/vagrant_ovpn /root/.ssh/id_rsa && chmod 0600 /root/.ssh/id_rsa
          chown -R root:root /root/.ssh
          setenforce 0
          systemctl stop firewalld && systemctl disable firewalld
        SHELL

        case boxname.to_s
        when "server"
          box.vm.provision "shell", run: "always", inline: <<-SHELL
            cd /etc/openvpn/
            mkdir keys
            /usr/share/easy-rsa/3.0.3/easyrsa init-pki
            /usr/share/easy-rsa/3.0.3/easyrsa --batch build-ca nopass
            /usr/share/easy-rsa/3.0.3/easyrsa gen-dh
            openvpn --genkey --secret tun.key
            openvpn --genkey --secret tap.key
            mv tun.key keys/
            mv tap.key keys/
            cp pki/ca.crt keys/
            cp pki/dh.pem keys/
            cp /vagrant/server-tun.conf server/
            cp /vagrant/server-out.conf server/
            cp /vagrant/server-tap.conf server/
            mkdir ccd
            echo "iroute 192.168.240.0 255.255.255.0" > ccd/client-tun
            echo "iroute 192.168.240.0 255.255.255.0" > ccd/host-tun
            echo "iroute 192.168.250.0 255.255.255.0" > ccd/client-tap
            systemctl start openvpn-server@server-tun && systemctl enable openvpn-server@server-tun
            systemctl start openvpn-server@server-out && systemctl enable openvpn-server@server-out
            systemctl start openvpn-server@server-tap && systemctl enable openvpn-server@server-tap
            SHELL
        when "client"
          box.vm.provision "shell", run: "always", inline: <<-SHELL
            mkdir -p /etc/openvpn/keys
            mkdir -p /etc/openvpn/client/
            cp /vagrant/client-tun.conf /etc/openvpn/client/
            ssh-keyscan -H 192.168.240.1 >> /root/.ssh/known_hosts
            scp -o "StrictHostKeyChecking no" root@192.168.240.1:/etc/openvpn/pki/ca.crt /etc/openvpn/keys/
            scp -o "StrictHostKeyChecking no" root@192.168.240.1:/etc/openvpn/keys/tun.key /etc/openvpn/keys/
            systemctl start openvpn-client@client-tun && systemctl enable openvpn-client@client-tun
            cp /vagrant/client-tap.conf /etc/openvpn/client/
            ssh-keyscan -H 192.168.250.1 >> /root/.ssh/known_hosts
            scp -o "StrictHostKeyChecking no" root@192.168.250.1:/etc/openvpn/keys/tap.key /etc/openvpn/keys/
            systemctl start openvpn-client@client-tap && systemctl enable openvpn-client@client-tap
            ssh -o "StrictHostKeyChecking no" root@192.168.240.1 "/sbin/ip a show eth3"
            echo "ca.crt"
            ssh -o "StrictHostKeyChecking no" root@192.168.240.1 "/bin/cat /etc/openvpn/pki/ca.crt"
            echo "tun.key"
            ssh -o "StrictHostKeyChecking no" root@192.168.240.1 "/bin/cat /etc/openvpn/keys/tun.key"
            SHELL
        end

      end

  end

end

