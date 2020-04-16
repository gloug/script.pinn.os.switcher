############################################
# Pinn Os switcher plugin allows you to boot to another Os partition when using PINN Operating System installer.
# IMPORTANT: This plugin is ONLY working with KODI installed on Raspberry Pi on an Operating System installed via PINN Operating System installer (like LibreElec).
# Author: gloug
#
# Note: PINN is a version of the NOOBS Operating System Installer for the Raspberry Pi. For more information please see https://github.com/procount/pinn/wiki.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
############################################

import os
import xbmcaddon
import xbmcgui
import json
from time import strftime

__MOUNT_FOLDER__ = "/media"
__PINN_RECOVERY_PARTITION__ = "/dev/mmcblk0p1"  # name of PINN RECOVERY partition (partition number 1)
__PINN_RECOVERY_MOUNT_PATH__ = os.path.join(__MOUNT_FOLDER__, "pinn_recovery_%s" % strftime("%Y%m%d_%B%M%S"))  # path where PINN RECOVERY parition will be mounted
__AUTOBOOT_FILE__ = os.path.join(__PINN_RECOVERY_MOUNT_PATH__, "autoboot.txt")  # path to autoboot.txt file
__PINN_SETTING_PARTITION__ = "/dev/mmcblk0p5"  # name of PINN SETTING partition (partition number 5)
__PINN_SETTING_MOUNT_PATH__ = os.path.join(__MOUNT_FOLDER__, "pinn_setting_%s" % strftime("%Y%m%d_%B%M%S"))  # path where PINN SETTING parition will be mounted
__INSTALLED_OS_JSON__ = os.path.join(__PINN_SETTING_MOUNT_PATH__, "installed_os.json")  # path to installed_os.json file
__VERIFY_PINN_MSG__ = "Be sure that you are using Kodi on RPI with PINN Operating system installer."

# flags
__reboot__ = False

def _DEBUG_(*args):
    xbmcgui.Dialog().ok("DEBUG", *args)

def get_partition_number(bootable_os):
    # partition must be first element of key "partitions": /dev/mmcblk0pX with X the number
    return bootable_os["partitions"][0].replace("/dev/mmcblk0p", "")

def clean_close():
    # umount partitions
    for mount_dir in os.listdir(__MOUNT_FOLDER__):
        if mount_dir.startswith("pinn_setting_"):
            code = os.system("umount %s " %  os.path.join(__MOUNT_FOLDER__, mount_dir))
            os.rmdir(os.path.join(__MOUNT_FOLDER__, mount_dir))

    for mount_dir in os.listdir(__MOUNT_FOLDER__):
        if mount_dir.startswith("pinn_recovery_"):
            code = os.system("umount %s " %  os.path.join(__MOUNT_FOLDER__, mount_dir))
            os.rmdir(os.path.join(__MOUNT_FOLDER__, mount_dir))


addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')

# try mounting Pinn system partitions
if not os.path.isdir(__PINN_RECOVERY_MOUNT_PATH__):
    os.makedirs(__PINN_RECOVERY_MOUNT_PATH__)
if not os.path.isdir(__PINN_SETTING_MOUNT_PATH__):
    os.makedirs(__PINN_SETTING_MOUNT_PATH__)
code1 = os.system("mount %s %s" % (__PINN_RECOVERY_PARTITION__, __PINN_RECOVERY_MOUNT_PATH__))
code2 = os.system("mount %s %s" % (__PINN_SETTING_PARTITION__, __PINN_SETTING_MOUNT_PATH__))

if code1 != 0 or code2 != 0:
    xbmcgui.Dialog().ok(
       addonname,
       "Error mounting PINN partitions",
       "PINN RECOVERY partition (%s) and/or PINN SETTING partition (%s) cannot be mounted. %s" % (__PINN_RECOVERY_PARTITION__, __PINN_SETTING_PARTITION__, __VERIFY_PINN_MSG__)) 
    clean_close()
    exit()

# check installed os
os_list = []
try:
    with open(__INSTALLED_OS_JSON__, 'r') as f:
        os_list = json.loads(f.read())  
    if type(os_list) != list:  # must be a list of dictionary
        raise(Exception, "%s is not a list of dict." % __INSTALLED_OS_JSON__)
except Exception as e:
    xbmcgui.Dialog().ok(
        addonname,
        "Error finding PINN installed OS.",
        "Failed reading 'installed_os.json' file in PINN SETTING partition (%s)." % __PINN_SETTING_PARTITION__)
    clean_close()
    exit()


# check bootable OS
bootable_os = [x for x in os_list if x["bootable"] is True]

if len(bootable_os) > 0:
    os_idx = int(xbmcgui.Dialog().select("Choose OS", ["%s: %s" % (x["name"], x["description"]) for x in bootable_os]))

    # check nb_part > 5 because partition 0 to 5 are reserved to pinn system
    if os_idx > -1:
        try:
            partition_number = get_partition_number(bootable_os[os_idx])
        except Exception as e:
            xbmcgui.Dialog().ok(
                addonname,
                "Error getting OS partition number.",
                "Failed reading '/dev/mmcblk0pX' information (with X number of partition).")
            clean_close()
            exit()

        try:
            # write autoboot.txt
            if os.path.isfile(__AUTOBOOT_FILE__):
                os.remove(__AUTOBOOT_FILE__)

            with open(__AUTOBOOT_FILE__, "w") as f:
                f.write("boot_partition=%s" % partition_number)
                __reboot__ = True

        except Exception as e:
            xbmcgui.Dialog().ok(
                "Switching to %s" % bootable_os[os_idx]["name"],
                "Exception Error. Please see log file.")
            clean_close()
            exit()
else:
    xbmcgui.Dialog().ok(
        addonname,
        "Error finding bootable OS",
        "Sorry, there is no bootable OS available. Please verify you PINN configuration.")
    clean_close()
    exit()

# reboot
if __reboot__:
    xbmcgui.Dialog().notification("Switching to %s" % bootable_os[os_idx]["name"], "please wait...", time=20000)
    os.system("reboot")

clean_close()
exit()
