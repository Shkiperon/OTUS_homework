#!/bin/bash
mkdir -p ~root/.ssh; cp ~vagrant/.ssh/auth* ~root/.ssh
sudo yum install mdadm gdisk -y 
remove=$(find /dev/ -name sd?1 | cut -c8)
full="abcdef"
full=${full/$remove}
full=$(echo $full | sed 's/\(\w\)/\/dev\/sd\1 /g' | sed 's/,$//g')
sudo mdadm --zero-superblock $full
sudo mdadm --create /dev/md0 -l 6 -n 4 -x 1 $full
sed -e 's/\s*\([\+0-9a-zA-Z]*\).*/\1/' << EOF | sudo gdisk /dev/md0
  n
  1
  
  +500M
  
  n
  2
  
  +1G
  
  n
  3
  
  +5G
  
  n
  4
  
  +7G
  
  n
  5
  
  
  
  w
  y
EOF
sudo mkdir -p /mnt/{boot,home,rootfs,usr}
counter=1
for MNTDIR in 'boot' 'home' 'rootfs' 'usr'
do
sudo mkfs.ext4 /dev/md0p$counter
OUT=$(sudo blkid | grep "/dev/md0p$counter:" | cut -d\" -f 2)
echo "UUID="${OUT}" /mnt/"$MNTDIR"           ext4    defaults      0 0" | sudo tee -a /etc/fstab
sudo mount -U "${OUT}" /mnt/"$MNTDIR"
counter=$((counter+1))
done
sudo mkswap /dev/md0p$counter
OUT=$(sudo blkid | grep "/dev/md0p$counter:" | cut -d\" -f 2)
echo "UUID="${OUT}" swap                     swap    defaults      0 0" | sudo tee -a /etc/fstab
sudo swapon -U "${OUT}"
echo 'The /dev/md0p[1-5] has been formated to EXT4 and added to fstab.'
echo 'If you need to format partions in another type of FS - do it manually :)'
