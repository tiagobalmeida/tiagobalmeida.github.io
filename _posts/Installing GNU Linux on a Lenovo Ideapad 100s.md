# Installing GNU/Linux on a Lenovo Ideapad 100s

This post is a work in progress on how to install GNU/Linux on a Lenovo Ideapad 100s. 
You'd think this is a trivial thing in 2018 but given the particular hardware on this device, this is actually quite painful.
I'm writing this post-activity so there may be some details I don't remember how they were solved. In any case, hope this helps.

# The problem 

This laptop uses a 64bit CPU but only boots with a 32bit UEFI boot. This is an awkward setup as usually 32bit computers boot through a BIOS and 64bit ones use a 64bit UEFI. 
In any case a few devices have this setup. What this means in practice is that if you burn an Ubuntu iso to an USB stick and try to boot from it, it won't be recognized.
The 32bit image of Ubuntu ships with a BIOS boot and the 64bit ships only with a 64bit UEFI so neither of them are an option.

# Solving this conundrum

The easy way of doing this is to install _Linuxium_. This is a very interesting project. A tool was developed that allows you to rebuild an original iso with support for mini-pcs and other awkward hardware like this one.

I didn't go that route as I struggled to run the `isorespin` tool in a linux virtual machine on the Ideapad itself. It unpacks a large iso, changes it and rebuilds it. This either took too long or failed with lack of storage space.


## The Debian way

So I searched for a different Linux distro..
The _multiarch_ Debian distribution ships with both 32 and 64 bit UEFI -> [Here](https://wiki.debian.org/UEFI#Support_for_mixed-mode_systems:_64-bit_system_with_32-bit_UEFI). So I figured installing this would be easy. How hard can it be right? aha.
The only _multiarch_ currently available is the _netinst_ variant, which means it will try to download all packages during the setup. 
This is what I burned to the usb stick.

### Resize Windows

As far as I know there are 2 variants of the Ideapad 100s, one with 32GB the other with 64. I have the 32GB and windows uses about 8 empty so there isn't a lot of space to play. Before installing anything we need to resize the windows partitions. On windows fire up `Disk Manager`. In the tool you will see 3 partitions, the EFI system partition (a few MBs), the windows recovery one (About 1GB) and the Windows one. I've resized windows to be 22GB thus leaving about 10 for Linux.

### Booting the USB

Plug the USB stick and press `Fn` `F12`. This will bring up the boot menu. In there you have to allow booting from an USB stick. I can't remember how this is done but a quick search on google will help you. 

### Install the multiarch netinst

Installation is straightforward but there's a problem :-) The Linux kernel shipped with it (version 4.9) does not currently support the wifi hardware of this laptop. Support for it was introduced in 4.12. 
So you'll have to do the setup without network.
This will only setup a basic system with a terminal and not much else. When the setup asks you which wifi hardware you're using, just skip it. It won't be listed as one the known devices.

### We want wifi goddammit!

Right, to have wifi we need to upgrade the kernel. On another computer [Download the 4.14 kernel](https://packages.debian.org/stretch-backports/linux-doc-4.14) or whatever is latest when you're reading this. Transfer the kernel file to the computer with an USB stick.

Install the kernel. As root run:

```sh
dpkg -i linux-doc-4.14_4.14.13-1-bpo9+1_all.deb
```

This will reconfigure your grub boot options as well. Reboot the system and confirm you're using the newer kernel with 
```
uname -a
```

You should see something like the following:
```sh
Linux ideapad 4.14.0-0.bpo.3-amd64 #1 SMP Debian 4.14.13-1~bpo9+1 (2018-01-14) x86_64 GNU/Linux
```

So now we need to do our first connection so we can download something useful.

On the same packages website you downloaded the kernel, we need to grab a few more packages and their dependencies.

Install package `wireless-tools` and `libiw30`. You will see loads of dependencies. I remember having download about 10 files and installing them all.
You'll also need the Realtek firmware. Download it from [https://packages.debian.org/stretch-backports/all/firmware-realtek/download
](https://packages.debian.org/stretch-backports/all/firmware-realtek/download
)
And install it with `dpkg`.

Once that is done you should have the `wpa_supplicant` command line tool. Use your favourite editor and, as root, edit `/etc/wpa_supplicant.conf` In there add a section that looks like the following:

```
network={
	ssid="Name Of Wifi Network"
	psk="ThePassword"
}
```

Load the kernel driver module and bring the connection up with:
```sh
modprobe rtl8723ae
modprobe rtl8723-common
ip link set wlan0 up
wpa_supplicant -iwlan0 -c/etc/wpa_supplicant.conf -Dwext
```
You should see something saying `BLA_BLA_CONNECTED` :-)
On another root terminal do:
```sh
dhclient wlan0
```
You should now have internet! 

### Update the sources list

For some reason my sources file was broken. I added the following entries to the `/etc/apt/sources.list` file:

```
deb  http://deb.debian.org/debian stretch main
deb-src  http://deb.debian.org/debian stretch main

deb  http://deb.debian.org/debian stretch-updates main
deb-src  http://deb.debian.org/debian stretch-updates main
```


Use `apt` or `apt-get` to install your favorite packages. 


### Getting some graphics

This is completely a matter of preference but I installed the gnome desktop environment and works fairly well.

```sh
apt-install gnome
```

# What's working and open issues

Some things are currently not working. If you have a solution please leave a comment below :)

Issues: 
 - Sound - Doesn't work. Didn't even try to solve it to be honest.
 - Battery sensor - Doesn't know which level the battery is at.

Untested:
 - External monitor through the HDMI interface

Working
  - Desktop environment
  - Brightness control
  - Shutdown and boot
  - Graphics performance seems comparable to the windows in the same laptop.
  - I'm typing this on this laptop, so pretty stable.

# References

https://unix.stackexchange.com/questions/115898/how-do-i-upgrade-the-debian-wheezy-kernel-offline

https://wiki.debian.org/WiFi/HowToUse#Command_Line

https://unix.stackexchange.com/questions/92799/connecting-to-wifi-network-through-command-line

http://www.jfwhome.com/2014/03/07/perfect-ubuntu-or-other-linux-on-the-asus-transformer-book-t100/

https://plus.google.com/communities/117853703024346186936

http://linuxiumcomau.blogspot.com/

http://linuxiumcomau.blogspot.com/2017/06/customizing-ubuntu-isos-documentation.html

https://askubuntu.com/questions/392719/32-bit-uefi-boot-support

