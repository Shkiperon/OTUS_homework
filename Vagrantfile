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

          file_to_disk1 = "sdb.vmdk"
          file_to_disk2 = "sdc.vmdk"
          file_to_disk3 = "sdd.vmdk"
          file_to_disk4 = "sde.vmdk"
          file_to_disk5 = "sdf.vmdk"

          box.vm.provider :virtualbox do |vb|
            if ! File.exist?("./.vagrant/machines/otuslinux/virtualbox/action_provision")
              vb.customize ["modifyvm", :id, "--memory", "1024"]
              unless File.exist?(file_to_disk1)
                 vb.customize [ "createmedium", "disk", "--filename", "sdb.vmdk", "--format", "vmdk", "--size", 1024 * 10 ]
              end
              unless File.exist?(file_to_disk2)
                 vb.customize [ "createmedium", "disk", "--filename", "sdc.vmdk", "--format", "vmdk", "--size", 1024 * 10 ]
              end
              unless File.exist?(file_to_disk3)
                 vb.customize [ "createmedium", "disk", "--filename", "sdd.vmdk", "--format", "vmdk", "--size", 1024 * 10 ]
              end
              unless File.exist?(file_to_disk4)
                 vb.customize [ "createmedium", "disk", "--filename", "sde.vmdk", "--format", "vmdk", "--size", 1024 * 10 ]
              end
              unless File.exist?(file_to_disk5)
                 vb.customize [ "createmedium", "disk", "--filename", "sdf.vmdk", "--format", "vmdk", "--size", 1024 * 10 ]
              end
              vb.customize [ "storagectl", :id, "--name", "SATA", "--add", "sata", "--controller", "IntelAHCI", "--portcount", "5", "--hostiocache", "on"]
              vb.customize [ "storageattach", :id , "--storagectl", "SATA", "--port", "0", "--device", "0", "--type", "hdd", "--medium", file_to_disk1]
              vb.customize [ "storageattach", :id , "--storagectl", "SATA", "--port", "1", "--device", "0", "--type", "hdd", "--medium", file_to_disk2]
              vb.customize [ "storageattach", :id , "--storagectl", "SATA", "--port", "2", "--device", "0", "--type", "hdd", "--medium", file_to_disk3]
              vb.customize [ "storageattach", :id , "--storagectl", "SATA", "--port", "3", "--device", "0", "--type", "hdd", "--medium", file_to_disk4]
              vb.customize [ "storageattach", :id , "--storagectl", "SATA", "--port", "4", "--device", "0", "--type", "hdd", "--medium", file_to_disk5]
            end
          end
          if ! File.exist?("./.vagrant/machines/otuslinux/virtualbox/action_provision")
            box.vm.provision "shell", path: "ext-script.sh"
          end
      end
  end
end
