# Installing GNU/Linux on a Lenovo Ideapad 100s

This post is a work in progress on how to install GNU/Linux on a Lenovo Ideapad 100s. 
You'd think this is a trivial thing in 2018 but given the particular hardware on this device, this is actually quite painful.
I'm writing this post-activity so there may be some details I don't remember how I solved them. In any case, hope this helps.

# The problem 

This laptop uses a 64bit CPU but only boots with a 32bit UEFI boot. This is an awkward setup as usually 32bit computers boot through a BIOS and 64bit use a proper 64bit UEFI. 
In any case a few devices have this setup. What this means in practice is that if you burn an Ubuntu iso to an USB stick and try to boot from it, it won't be recognized.
The 32bit image of Ubuntu ships with a BIOS boot and the 64bit ships only with a 64bit UEFI so neither of them are an option.

# Solving this conundrum

The easy way of doing this is to install _Linuxium_. This is a very interesting project. A tool was developed that allows you to rebuild an original iso with support for mini-pcs and other awkward hardware like this one.

I didn't go that route as I struggled to run the tool in a linux virtual machine on the Ideapad itself. The tool unpacks a large iso, changes it and rebuilds it. 
This either took too long or failed with lack of storage space.


## The Debian way

The _multiarch_ Debian distribution ships with both 32 and 64 bit UEFI -> [Here](https://wiki.debian.org/UEFI#Support_for_mixed-mode_systems:_64-bit_system_with_32-bit_UEFI). So I figured installing this would be easy. Was I wrong..
The only _multiarch_ currently available is the _netinst_ variant, which means it will try to download all packages during the setup. 
This is what I burned to the usb stick and booted.

### Install the multiarch netinst

Installation is straightforward but there's a problem :-) The Linux kernel shipped with it (version 4.9) does not currently support the wifi hardware, which was introduced in 4.12. 
So you'll have to do the setup without network.
This will only setup a basic system with a terminal and not much else. When the setup asks you which wifi hardware you're using, just skip it. It won't be listed as one the known devices.

### We want wifi goddammit!
Right, to have wifi we need to upgrade the kernel. On another computer [Download the 4.14 kernel](https://packages.debian.org/stretch-backports/linux-doc-4.14) or whatever is latest when you're reading this.

Install the kernel:

```sh
dpkg -i linux-doc-4.14_4.14.13-1-bpo9+1_all.deb
```

This will reconfigure your grub boot options as well. Reboot the system and confirm you're using the newer kernel with 
```
uname -a
```

### Wifi setup

TO DO
