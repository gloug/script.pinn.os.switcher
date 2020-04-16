# Pinn Os Switcher
Pinn Os switcher plugin allows you to boot to another Os partition when using PINN Operating System installer.

## Notes
* This plugin is ONLY working with KODI installed on Raspberry Pi on an Operating System installed via PINN Operating System installer (like LibreElec).
* PINN is a version of the NOOBS Operating System Installer for the Raspberry Pi. For more information please see https://github.com/procount/pinn/wiki.

## How it works
Plugin simply bypass PINN by editing the **autoboot.txt** file in the root directory of PINN.

*More specifically:* it mounts the 2 PIN RECOVERY and SETTING partitions (respectively partition 1 and partition 5) to detect the bootable OS available.
Then, depending on your choice, it adds ```boot_partition=<partition number>``` in **autoboot.txt** file in the root directory of the RECOVERY partition.

**IMPORTANT NOTE:** If you don't want your Raspberry Pi to keep booting to the selected OS afterwards, you need to add a script at the startup of each OS to delete the autoboot.txt file.

* **For Rapsbian:**

Create a file ```/home/pi/removeautoboot.sh``` (for example) and add:
```
mkdir /media/PINN_RECOVERY
mount /dev/mmcblk0p1 /media/PINN_RECOVERY
rm /media/PINN_RECOVERY/autoboot.txt
```
Make your script executable with:
```
chmod +x /home/pi/removeautoboot.sh
```
Then edit the file ```/etc/rc.local``` and add at the end (before exit 0):
```
sh /home/pi/removeautoboot.sh &
```

* **For Lakka or LibreElec:**

Create (or edit) ```/storage/.config/autostart.sh``` and add:
```
(
mkdir /media/PINN_RECOVERY
mount /dev/mmcblk0p1 /media/PINN_RECOVERY
rm /media/PINN_RECOVERY/autoboot.txt
)&
```

## In Work...
* automatic remove of autoboot.txt file during boot (using ```before-reboot.sh``` ?)

## Change History

**0.2**
* Auo mount in tmp path (folders are umount and removed afterward)
* No configuration needed: List of bootable OS is read from PINN SETTING partition ('installed_os.json' file)

**0.1**
* Init version
* Moun path is configurable
* List of bootable OS is manually configurable