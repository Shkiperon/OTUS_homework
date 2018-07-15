# -*- mode: ruby -*-
# vim: set ft=ruby :

MACHINES = {
  :inetRouter => {
        :box_name => "centos/6",
        #:public => {adapter: 1},
        :net => [
                   {ip: '192.168.255.1', adapter: 2, netmask: "255.255.255.240", virtualbox__intnet: "router-net"},
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

        box.vm.provision "ansible" do |ansible|
          ansible.verbose = "vvv"
          ansible.playbook = "playbook.yml"
        end

      end

  end
  
  
end

