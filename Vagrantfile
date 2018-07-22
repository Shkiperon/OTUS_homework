# -*- mode: ruby -*-
# vim: set ft=ruby :

MACHINES = {
  :Server => {
        :box_name => "centos/7",
        :net => [
                   {ip: '192.168.0.2', adapter: 2, netmask: "255.255.255.240", virtualbox__intnet: "dir-net"},
                ]
  },

  :Test => {
        :box_name => "centos/7",
        :net => [
                   {ip: '192.168.0.3', adapter: 2, netmask: "255.255.255.240", virtualbox__intnet: "dir-net"},
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

        box.vm.provision "shell", run: "always", inline: <<-SHELL
          mkdir -p ~root/.ssh; cp ~vagrant/.ssh/auth* ~root/.ssh
        SHELL

	case boxname.to_s
        when "Server"
          box.vm.provision "shell", run: "always", inline: <<-SHELL
            yum install -y epel-release
            yum install -y pam_script
  	    useradd firstuser
            echo "firstuser:firstpass" | chpasswd
            useradd seconduser
            echo "seconduser:secondpass" | chpasswd
            groupadd admin
            usermod -a -G admin firstuser
            sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd_config
            echo "auth       required     pam_script.so" >> /etc/pam.d/sshd
            echo "cap_sys_admin seconduser" > /etc/security/capability.conf
            echo "auth       optional     pam_cap.so" >> /etc/pam.d/su
            cp /vagrant/pam_script /etc/pam_script && chmod 0755 /etc/pam_script
            systemctl restart sshd
          SHELL
        end

      end

  end

end

