# Building a Raspberry Pi NAS - Part 3: Storing files encrypted in the cloud

This post is part of a series on building the ultimate NAS system with a raspberry pi, creating your own "cloud".
In this post I'll present a way to make sure you do not lose your important files.
For this, we'll setup a personal account on a cloud service provider and then mount the space they give us on the raspberry pi's file system. The files will be replicated remotely to this service to prevent data loss if local file systems fail.
This storage space will also be used for very important and sensitive data. For this reason, it will be fully encrypted so that not even the cloud sys admins could read it.
Alternative titles: 
- Mount box.com on raspberry pi 
- Encrypt files with encFs on raspberry pi 

Part 1: Getting a reliable remote storage space
First get an account on box.com (this is a cloud storage provider). Personal accounts are free and give you 10GB.  I chose them because they support the webdav protocol, unlike google drive which would be my first option. Other possible provider could be HiDrive
. In theory you could use any remote storage space provider that supports some protocol that you can use for mounting. 
Now let's create a mount point. In this series I am mounting the different filesystems on ~/mnt. For this create a ~/mnt/box1 folder.

```shell
cd ~/mnt
mkdir box1
```

Now install the necessary packages to mount a webdav fs.
```shell
sudo apt-get install davfs2
```

We want this to be fully automated and automounted on reboot. For this, we need to store the user and password you used for the box.com account in a file.
Create folder ~/.davfs2
```shell
cd ~
mkdir .davfs2
```

Inside this folder, edit file called secrets 
```shell
cd .davfs2
nano secrets
```
and insert a single line like this:
https://dav.box.com/dav username password
Where username / password are replaced by your own 
Now we need to add the pi user to the davfs2 group so that he can mount these guys.
```shell
sudo usermod -aG davfs2 pi
```
Also do the reconfig:
```shell
sudo dpkg-reconfigure davfs2
```
Select yes on the screen that appears. 
Edit /etc/fstab as root and insert the following line:
```
https://dav.box.com/dav /home/pi/mnt/box1  davfs  rw,noexec,noauto,user,async,_netdev,uid=pi,gid=pi  0  0
```
The _netdev specifies that this fs is only mounted if there is a network connection. You should test this. Logout and login again (so that your user gets the new group), and try to mount the file system with the following command: 
```shell
mount /home/pi/mnt/box1
```
You will most likely get an error: /sbin/mount.davfs: file /home/pi/.davfs2/secrets has wrong permissions This is because the user pi is still not in the group above. Reboot the pi.
```shell
sudo shutdown -r now
```
Now that the pi is rebooted, go to the .davfs2 folder and change permissions of the secrets file. If you do not do it, you'll get the following error: "/sbin/mount.davfs: file /home/pi/.davfs2/secrets has wrong permissions"
```shell
cd ~/.davfs2
chmod 600 secrets
```
Now, try to mount the file system:
```shell
mount /home/pi/mnt/box1
```
if everything ok you can now copy files from/to /home/pi/mnt/box1 and they are being stored remotely. 
Note: I have found that automounting this with the auto option in etc/fstab is not very reliable. For this reason, we'll use an init script below to deal with the auto mounting on boot. 

## Part 2: Encrypting the files

To encrypt the files we'll use EncFS. This is a filesystem that allows you to mount another existing mount point. When you create files on the EncFs file system, they are transparently encrypted with a password you have chosen and stored (encrypted) in the underlying file system. We'll use the file system created previously as the underlying storage. 
Create a new mount point for the encrypted. I'll call it encbox1 
```shell
cd ~/mnt
mkdir encbox1
```
Install encfs 
```shell
sudo apt-get install encfs
```
To be able to mount fuse based file systems (like encfs) you need to be on the fuse group. 
```shell
sudo gpasswd -a pi fuse
```
Now it is easy to create the encrypted virtual file system. Use the following command: 
```shell
encfs ~/mnt/box1 ~/mnt/encbox1
```

This will use ~/mnt/box1 as an encrypted storage for whatever you create on encbox1. 
Let's test by creating a file on encbox1 and then listing content of encbox1 and box1: 
```shell
echo "test" > ~/mnt/encbox1/teste.txt
ls -lah ~/mnt/encbox1/
total 1,0K
drwxr-xr-x 3 pi pi 160 Abr 26 20:20 .
-rw-r--r-- 1 pi pi   5 Abr 26 20:11 teste.txt
ls -lah ~/mnt/box1/
total 2,5K
drwxr-xr-x 3 pi pi  160 Abr 26 20:20 .
-rw-r--r-- 1 pi pi 1,1K Abr 26 20:09 .encfs6.xml
drwx------ 2 pi pi    0 Abr 26 00:22 lost+found
-rw-r--r-- 1 pi pi   13 Abr 26 20:11 xbeDOz08kT4LmeJpXZmNAnky
```

Notice that the file is slightly larger after encryption (13Bytes) while the plain one is 5. This is because there is a overhead of +8Bytes when per file Initialization vectors are used. More with man encfs. 

## Part 3: Automounting encfs
As it turns out, automounting an encfs is not as simple as putting a line on /etc/fstab. We will create an init script for this and then set it to run automatically on boot. Create your script on /etc/init.d/boxencfs 
Also, you need to put encfs password on a file only you can read.
```shell
cd ~
mkdir .encfs
cd .encfs
nano box1
```

(now insert your password and ctrl+o, ctrl+x)
```shell
chmod 700 box1
sudo nano /etc/init.d/boxencfs
```
And insert the following code: 
```shell
#! /bin/bash
# /etc/init.d/boxencfs

### BEGIN INIT INFO
# Provides:          boxencfs
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Simple script to mount box.com via webdav and an encfs on top of it
# Description:       Mount box.com via webdav and encfs on top of it.
### END INIT INFO

# If you want a command to always run, put it here

# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Mounting box.com"
    su pi -c "mount /home/pi/mnt/box1"
    echo "Mounting encfs"
    su pi -c "cat /home/pi/.encfs/box1 | encfs -S /home/pi/mnt/box1 /home/pi/mnt/encbox1"
    ;;
  stop)
    echo "Unmounting encfs"
    su pi -c "fusermount -u /home/pi/mnt/encbox1"
    echo "Unmounting box.com"
    umount /home/pi/mnt/box1
    ;;
  *)
    echo "Usage: /etc/init.d/boxencfs {start|stop}"
    exit 1
    ;;
esac

exit 0
```

This script, when passed the start argument, first mounts the box1 system on /home/pi/mnt/box1 and then mounts the encfs. The password for the encfs is stored on /home/pi/.encfs/box1 ( a file created previously ) and then piped to the encfs. -S argument to encfs makes it read the password from stdin. With the stop argument it does the opposite in opposite order. After saving this file, make it executable: 
```shell
sudo chmod +x /etc/init.d/boxencfs
```

Test this file very well by starting it and stopping it. A problem here may halt your reboot process. Test that it stops 
```shell
sudo /etc/init.d/boxencfs stop
```

Now test that it starts. After this, check your encbox1 and box1 folders to see if they have the files expected. 
```shell
sudo /etc/init.d/boxencfs start
```
When you feel this is fine, set it to run on boot/shutdown 
sudo update-rc.d boxencfs defaults
And now reboot your pi and pray that it doesn't hang on reboot :) 
```shell
sudo shutdown -r now
```

## Part 4: schedule an rsync to copy files to box1

At this moment we have a folder with 10GB capacity and anything we put there is encrypted on the fly and sent to box.com servers. This folder will be where we will store a copy of our important files. To see this you can run df -h:
```shell
Filesystem               Size  Used Avail Use% Mounted on
rootfs                   7,1G  2,3G  4,5G  34% /
/dev/root                7,1G  2,3G  4,5G  34% /
devtmpfs                 211M     0  211M   0% /dev
tmpfs                     44M  416K   44M   1% /run
tmpfs                    5,0M     0  5,0M   0% /run/lock
tmpfs                     88M     0   88M   0% /run/shm
/dev/mmcblk0p1            56M   19M   38M  34% /boot
/dev/sda3                 12G  2,5G  8,5G  23% /home/pi/mnt/media1
/dev/sdb1                 30G  2,0G   26G   7% /home/pi/mnt/media2
/dev/sda2                9,8G  266M  9,0G   3% /home/pi/mnt/home
https://dav.box.com/dav   10G     0   10G   0% /home/pi/mnt/box1
encfs                     10G     0   10G   0% /home/pi/mnt/encbox1
```
In my case, I want to make a backup of /home/pi/mnt/home (which is a mount point for an external USB drive (see previous parts of this tutorial)) into /home/pi/mnt/encbox1. The command you want to run is:
```shell
cd ~/mnt
rsync -rtvuh --progress --delete home encbox1
```
This syncs whatever is in ~/mnt/home into ~/mnt/encbox1. -r means recursive, t to preserve modification times, v for verbose, h for human readable sizes. --delete makes files be deleted on encbox1 if they were deleted on home.
```shell
crontab -e
```

Now we setup cron so that this command is executed every day at 12:00. For this, type:
crontab -e
An editor appears, in my case it is nano. Insert a line like the following:
```shell
0 12 * * * rsync -rtvuhW --progress --delete --inplace /home/pi/mnt/home/ /home/pi/mnt/encbox1/ >> /home
/pi/.log/boxbackups.log
```
This line has the following semantic: At minute 0 of hour 12, every day of the month, every month of the year, every day of the week. run the rsync command. The rsync flags are important. without --inplace, rsync creates all files with 0 bytes. This is a known issue when rsyncing to a network folder. Also, all paths are absolute, to avoid issues and the output is concatenated to a log file (/home/pi/.log/boxbackups.log) so that we can later see what was backed up. 


References:

http://www.sbprojects.com/projects/raspberrypi/webdav.php
http://www.howtoforge.com/encrypt-your-data-with-encfs-debian-squeeze-ubuntu-11.10
http://www.jveweb.net/en/archives/2010/11/synchronizing-folders-with-rsync.html http://www.google.com :P