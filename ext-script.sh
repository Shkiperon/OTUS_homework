#!/bin/bash
mkdir -p ~root/.ssh; cp ~vagrant/.ssh/auth* ~root/.ssh
yum install mdadm gdisk xfsdump -y 
remove=$(find /dev/ -name sd?1 | cut -c8)
full="abcdef"
full=${full/$remove}
full=$(echo $full | sed 's/\(\w\)/\/dev\/sd\1 /g' | sed 's/,$//g')
mdadm --zero-superblock $full
mdadm --create /dev/md0 -l 6 -n 4 -x 1 $full
sed -e 's/\s*\([\+0-9a-zA-Z]*\).*/\1/' << EOF | sudo gdisk /dev/md0
  n
  1
  
  +11G
  

  n
  2
  
  
  
  w
  y
EOF
mkdir -p /mnt/{home,var,rootfsbck}

pvcreate /dev/md0p{1,2}
vgextend VolGroup00 /dev/md0p{1,2}
lvcreate -L 500M -n home VolGroup00
lvcreate -L 2G -n var VolGroup00
lvcreate -L 3G -n rootfsbck VolGroup00
lvconvert -m 1 /dev/VolGroup00/var -y
vgscan
vgchange -ay

#cp -ar /home/* /mnt/home;rm -rf /home;ln -s /mnt/home /home
sleep 5s
mkfs.xfs /dev/VolGroup00/{home,var,rootfsbck}
for MNTDIR in 'home' 'var' 'rootfsbck'
do
mkfs.xfs /dev/VolGroup00/$MNTDIR
mount /dev/VolGroup00/$MNTDIR /mnt/$MNTDIR
done
cp -ar /home/* /mnt/home
rm -rf /home/*;umount /mnt/home;mount /dev/VolGroup00/home /home
echo "/dev/mapper/VolGroup00-home /home           xfs    defaults      0 0" | sudo tee -a /etc/fstab
echo "Configuration has been finished. Enjoy :-)"
