# Pinn Os Switcher
Pinn Os switcher plugin allows you to boot to another Os partition when using PINN Operating System installer.

## Notes
* This plugin is ONLY working with KODI installed on Raspberry Pi on an Operating System installed via PINN Operating System installer (like LibreElec).
* PINN is a version of the NOOBS Operating System Installer for the Raspberry Pi. For more information please see https://github.com/procount/pinn/wiki.

## How it works
Plugin simply bypass PINN by editing the **autoboot.txt** file in the root directory of PINN.

*More specifically:* it mounts the 2 PIN RECOVERY and SETTING partitions (respectively partition 1 and partition 5) to detect te bootable OS available.
Then, depending on your choice, it adds ```boot_partition=<partition number>``` in **autoboot.txt** file in the root directory of the RECOVERY partition.

**IMPORTANT NOTE:** If you don't want your Raspberry Pi to keep booting to the selected OS afterwards, you need to add a script at the startup of each OS to delete the autoboot.txt file.

## In Work
* auto remove of autoboot.txt file after reboot

## Versions

**0.2**
* Auo mount in tmp path (folders are umount and removed afterward)
* No configuration needed: List of bootable OS is read from PINN SETTING partition ('installed_os.json' file)

**0.1**
* Init version
* Moun path is configurable
* List of bootable OS is manually configurable