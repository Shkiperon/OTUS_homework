# -*- mode: ruby -*-
# vim: set ft=ruby :
# -*- mode: ruby -*-
# vim: set ft=ruby :

MACHINES = {
:inetRouter => {
        :box_name => "centos/6",
        #:public => {adapter: 1},
        :net => [
                   {ip: '192.168.255.1', adapter: 2, netmask: "255.255.255.252", virtualbox__intnet: "router-net"},
                ]
  },

  :centralRouter => {
        :box_name => "centos/7",
        :net => [
                   {ip: '192.168.255.2', adapter: 2, netmask: "255.255.255.252", virtualbox__intnet: "router-net"},
                   {ip: '192.168.0.1', adapter: 3, netmask: "255.255.255.240", virtualbox__intnet: "dir-net"},
                   {ip: '192.168.0.33', adapter: 4, netmask: "255.255.255.240", virtualbox__intnet: "hw-net"},
                   {ip: '192.168.0.65', adapter: 5, netmask: "255.255.255.192", virtualbox__intnet: "wifi-net"},
                   {ip: '192.168.254.1', adapter: 6, netmask: "255.255.255.252", virtualbox__intnet: "gate1-net"},
                   {ip: '192.168.253.1', adapter: 7, netmask: "255.255.255.252", virtualbox__intnet: "gate2-net"},
                ]
  },
  
  :centralServer => {
        :box_name => "centos/7",
        :net => [
                   {ip: '192.168.0.2', adapter: 2, netmask: "255.255.255.240", virtualbox__intnet: "dir-net"},
                   {adapter: 3, auto_config: false, virtualbox__intnet: true},
                   {adapter: 4, auto_config: false, virtualbox__intnet: true},
                ]
  },

  :office1Router => {
        :box_name => "centos/7",
        :net => [
                   {ip: '192.168.2.1', adapter: 2, netmask: "255.255.255.192", virtualbox__intnet: "dev-net"},
                   {ip: '192.168.2.65', adapter: 3, netmask: "255.255.255.192", virtualbox__intnet: "test-net"},
                   {ip: '192.168.2.129', adapter: 4, netmask: "255.255.255.192", virtualbox__intnet: "mgmt-net"},
                   {ip: '192.168.2.193', adapter: 5, netmask: "255.255.255.192", virtualbox__intnet: "hw-net"},
                   {ip: '192.168.254.2', adapter: 6, netmask: "255.255.255.252", virtualbox__intnet: "gate1-net"},
                ]
  },

  :office1Server => {
        :box_name => "centos/7",
        :net => [
                   {ip: '192.168.2.194', adapter: 2, netmask: "255.255.255.192", virtualbox__intnet: "hw-net"},
                   {adapter: 3, auto_config: false, virtualbox__intnet: true},
                   {adapter: 4, auto_config: false, virtualbox__intnet: true},
                ]
  },

  :office2Router => {
        :box_name => "centos/7",
        :net => [
                   {ip: '192.168.1.1', adapter: 2, netmask: "255.255.255.128", virtualbox__intnet: "dev-net"},
                   {ip: '192.168.1.129', adapter: 3, netmask: "255.255.255.192", virtualbox__intnet: "test-net"},
                   {ip: '192.168.1.193', adapter: 4, netmask: "255.255.255.192", virtualbox__intnet: "hw-net"},
                   {ip: '192.168.253.2', adapter: 5, netmask: "255.255.255.252", virtualbox__intnet: "gate2-net"},
                ]
  },

  :office2Server => {
        :box_name => "centos/7",
        :net => [
                   {ip: '192.168.1.194', adapter: 2, netmask: "255.255.255.192", virtualbox__intnet: "hw-net"},
                   {adapter: 3, auto_config: false, virtualbox__intnet: true},
                   {adapter: 4, auto_config: false, virtualbox__intnet: true},
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

        box.vm.provision "shell", inline: <<-SHELL
          mkdir -p ~root/.ssh
                cp ~vagrant/.ssh/auth* ~root/.ssh
        SHELL
        
        case boxname.to_s
        when "inetRouter"
          box.vm.provision "shell", run: "always", inline: <<-SHELL
            sysctl net.ipv4.conf.all.forwarding=1
            iptables -t nat -A POSTROUTING ! -d 192.168.0.0/16 -o eth0 -j MASQUERADE
            SHELL
        when "centralRouter"
          box.vm.provision "shell", run: "always", inline: <<-SHELL
            sysctl net.ipv4.conf.all.forwarding=1
            nmcli connection modify "System eth0" ipv4.never-default yes
            nmcli connection modify "System eth1" ipv4.gateway "192.168.255.1"
            nmcli connection modify "System eth5" +ipv4.routes "192.168.2.0/24 192.168.254.2"
            nmcli connection modify "System eth6" +ipv4.routes "192.168.1.0/24 192.168.253.2"
            nmcli connection reload
            nmcli connection up "System eth0"
            nmcli connection up "System eth1"
            nmcli connection up "System eth5"
            nmcli connection up "System eth6"
            iptables -t nat -A POSTROUTING ! -d 192.168.0.0/16 -o eth1 -j MASQUERADE
            SHELL
        when "centralServer"
          box.vm.provision "shell", run: "always", inline: <<-SHELL
            nmcli connection modify "System eth0" ipv4.never-default yes
            nmcli connection modify "System eth1" ipv4.gateway "192.168.0.1"
            nmcli connection reload
            nmcli connection up "System eth0"
            nmcli connection up "System eth1"
            SHELL
        when "office1Router"
          box.vm.provision "shell", run: "always", inline: <<-SHELL
            sysctl net.ipv4.conf.all.forwarding=1
            nmcli connection modify "System eth0" ipv4.never-default yes
            nmcli connection modify "System eth5" ipv4.gateway "192.168.254.1"
            nmcli connection modify "System eth5" +ipv4.routes "192.168.0.0/24 192.168.254.1"
            nmcli connection modify "System eth5" +ipv4.routes "192.168.1.0/24 192.168.254.1"
            nmcli connection reload
            nmcli connection up "System eth0"
            nmcli connection up "System eth5"
            SHELL
        when "office1Server"
          box.vm.provision "shell", run: "always", inline: <<-SHELL
            nmcli connection modify "System eth0" ipv4.never-default yes
            nmcli connection modify "System eth1" ipv4.gateway "192.168.2.193"
            nmcli connection reload
            nmcli connection up "System eth0"
            nmcli connection up "System eth1"
            SHELL
        when "office2Router"
          box.vm.provision "shell", run: "always", inline: <<-SHELL
            sysctl net.ipv4.conf.all.forwarding=1
            nmcli connection modify "System eth0" ipv4.never-default yes
            nmcli connection modify "System eth4" ipv4.gateway "192.168.253.1"
            nmcli connection modify "System eth4" +ipv4.routes "192.168.0.0/24 192.168.253.1"
            nmcli connection modify "System eth4" +ipv4.routes "192.168.2.0/24 192.168.253.1"
            nmcli connection reload
            nmcli connection up "System eth0"
            nmcli connection up "System eth4"
            SHELL
        when "office2Server"
          box.vm.provision "shell", run: "always", inline: <<-SHELL
            nmcli connection modify "System eth0" ipv4.never-default yes
            nmcli connection modify "System eth1" ipv4.gateway "192.168.1.193"
            nmcli connection reload
            nmcli connection up "System eth0"
            nmcli connection up "System eth1"
            SHELL
        end

      end

  end
  
  
end

