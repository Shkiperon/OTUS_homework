# -*- mode: ruby -*-
# vim: set ft=ruby :

MACHINES = {
  :inetRouter => {
        :box_name => "centos/6",
        #:public => {adapter: 1},
        :net => [
                   {ip: '192.168.255.1', adapter: 2, netmask: "255.255.255.240", virtualbox__intnet: "router-net"},
                   {adapter: 3, auto_config: false, virtualbox__intnet: "router-net"},
                   {adapter: 4, auto_config: false, virtualbox__intnet: "router-net"},
                ]
  },

  :inetRouter2 => {
        :box_name => "centos/6",
        #:public => {adapter: 1},
        :net => [
                   {ip: '192.168.255.3', adapter: 2, netmask: "255.255.255.240", virtualbox__intnet: "router-net"},
                ]
  },

  :centralRouter => {
        :box_name => "centos/7",
        :net => [
                   {ip: '192.168.255.2', adapter: 2, netmask: "255.255.255.240", virtualbox__intnet: "router-net"},
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
        SHELL
        
        case boxname.to_s
        when "inetRouter"
          box.vm.provision "shell", run: "always", inline: <<-SHELL
            sysctl net.ipv4.conf.all.forwarding=1
            iptables -t nat -A POSTROUTING ! -d 192.168.0.0/16 -o eth0 -j MASQUERADE
            service network restart
            SHELL
        when "inetRouter2"
          box.vm.provision "shell", run: "always", inline: <<-SHELL
            sysctl net.ipv4.conf.all.forwarding=1
            nmcli connection modify "System eth0" ipv4.never-default yes
            nmcli connection modify "System eth1" ipv4.gateway "192.168.255.1"
            nmcli connection reload
            nmcli connection up "System eth0"
            nmcli connection up "System eth1"
            iptables -t nat -A POSTROUTING ! -d 192.168.0.0/16 -o eth0 -j MASQUERADE
            service network restart
            SHELL
        when "centralRouter"
          box.vm.provision "shell", run: "always", inline: <<-SHELL
            sysctl net.ipv4.conf.all.forwarding=1
            nmcli connection modify "System eth0" ipv4.never-default yes
            nmcli connection modify "System eth1" ipv4.gateway "192.168.255.1"
            nmcli connection reload
            nmcli connection up "System eth0"
            nmcli connection up "System eth1"
            iptables -t nat -A POSTROUTING ! -d 192.168.0.0/16 -o eth1 -j MASQUERADE
            SHELL
        end

      end

  end
  
  
end
