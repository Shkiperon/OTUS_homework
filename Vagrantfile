# -*- mode: ruby -*-
# vim: set ft=ruby :

MACHINES = {
 :web => {
        :box_name => "centos/7",
        :ip_addr => '192.168.0.2'
  },
  :log => {
        :box_name => "centos/7",
        :ip_addr => '192.168.0.3'
  },
}

Vagrant.configure("2") do |config|

  MACHINES.each do |boxname, boxconfig|

    config.vm.define boxname do |box|

        box.vm.box = boxconfig[:box_name]
        box.vm.host_name = boxname.to_s

        box.vm.network "private_network", ip: boxconfig[:ip_addr]
       
        box.vm.provider :virtualbox do |vb|
          vb.memory = 256
        end

	box.vm.provision :shell do |s|
	  s.inline = 'mkdir -p ~root/.ssh; cp ~vagrant/.ssh/auth* ~root/.ssh'
	end
    end
  end
end

