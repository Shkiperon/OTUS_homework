# -*- mode: ruby -*-
# vim: set ft=ruby :

MACHINES = {

  :srv1 => {
        :box_name => "centos/7",
        #:public => {adapter: 4},
        :net => [
                   {adapter: 2, auto_config: false, virtualbox__intnet: "ospf-net"},
                   {ip: '192.168.0.1', adapter: 3, netmask: "255.255.255.0", virtualbox__intnet: "area-net"},
                ]
  },

  :srv2 => {
        :box_name => "centos/7",
        :net => [
                   {adapter: 2, auto_config: false, virtualbox__intnet: "ospf-net"},
                   {ip: '192.168.1.1', adapter: 3, netmask: "255.255.255.0", virtualbox__intnet: "area-net"},
                ]
  },

  :srv3 => {
        :box_name => "centos/7",
        :net => [
                   {adapter: 2, auto_config: false, virtualbox__intnet: "ospf-net"},
                   {ip: '192.168.2.1', adapter: 3, netmask: "255.255.255.0", virtualbox__intnet: "area-net"},
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
          yum install -y quagga
          setenforce 0
          touch /etc/quagga/ospfd.conf
          chown quagga:quagga /etc/quagga/ospfd.conf
          systemctl enable ospfd
          systemctl enable zebra
          systemctl start ospfd
          systemctl start zebra
        SHELL

        case boxname.to_s
        when "srv1"
          box.vm.provision "shell", inline: <<-SHELL
            nmcli c add type vlan con-name eth1.10 dev eth1 ifname eth1.10 id 10 ip4 10.0.10.1/30
            nmcli c add type vlan con-name eth1.20 dev eth1 ifname eth1.20 id 20 ip4 10.0.20.1/30
            nmcli c reload
            nmcli connection up eth1.10
            nmcli connection up eth1.20
            SHELL
        when "srv2"
          box.vm.provision "shell", inline: <<-SHELL
            nmcli c add type vlan con-name eth1.10 dev eth1 ifname eth1.10 id 10 ip4 10.0.10.2/30
            nmcli c add type vlan con-name eth1.30 dev eth1 ifname eth1.30 id 30 ip4 10.0.30.1/30
            nmcli c reload
            nmcli connection up eth1.10
            nmcli connection up eth1.30
            SHELL
        when "srv3"
          box.vm.provision "shell", inline: <<-SHELL
            nmcli c add type vlan con-name eth1.20 dev eth1 ifname eth1.20 id 20 ip4 10.0.20.2/30
            nmcli c add type vlan con-name eth1.30 dev eth1 ifname eth1.30 id 30 ip4 10.0.30.2/30
            nmcli c reload
            nmcli connection up eth1.20
            nmcli connection up eth1.30
            SHELL
        end

      end

  end

end

