# -*- mode: ruby -*-
# vim: set ft=ruby :

MACHINES = {
  :otuslinux => {
        :box_name => "centos/7",
        :ip_addr => '192.168.11.101'
  },
}

Vagrant.configure("2") do |config|

  MACHINES.each do |boxname, boxconfig|

      config.vm.define boxname do |box|

          box.vm.box = boxconfig[:box_name]
          box.vm.host_name = boxname.to_s

          box.vm.network "private_network", ip: boxconfig[:ip_addr]

          box.vm.provider :virtualbox do |vb|
            if ! File.exist?("./.vagrant/machines/otuslinux/virtualbox/action_provision")
              vb.customize ["modifyvm", :id, "--memory", "1024"]
            end
          end
          if ! File.exist?("./.vagrant/machines/otuslinux/virtualbox/action_provision")
            box.vm.provision "shell", path: "ext-script.sh"
          end
      end
  end
end
