import os
import xbmcaddon
import xbmcgui

MAX_OS = 5


addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')

# get path to pinn system partition
pinn_sys_part_path = str(xbmcaddon.Addon().getSetting("pinn_system_folder"))
autoboot_file = os.path.join(pinn_sys_part_path, "autoboot.txt")

# get all os
os_list = []
for i in range(1, MAX_OS+1):
    name = str(xbmcaddon.Addon().getSetting("os%s_name" % str(i)))
    nb_part = str(xbmcaddon.Addon().getSetting("os%s_part_nb" % str(i)))
    if name != "" and nb_part != "" and nb_part != "0":
        os_list.append({
            "name": name,
            "nb_part": nb_part
        })

os_idx = xbmcgui.Dialog().select("Choose OS", [x["name"] for x in os_list])

# check nb_part > 5 because partition 0 to 5 are reserved to pinn system
if int(os_list[os_idx]["nb_part"]) <= 5:
    xbmcgui.Dialog().ok("Starting Raspbian", "Error", "Os '%s' has wrong partition configuration, it has to be superior to 5 (partitions 1 to 5 are reserved to pinn system)." % os_list[os_idx]["name"])
else:
    reboot = False

    try:
        if os.path.isfile(autoboot_file):
            os.remove(autoboot_file)

        if os.path.isdir(pinn_sys_part_path):
            with open(autoboot_file, "w") as f:
                f.write("boot_partition=%s" % os_list[os_idx]["nb_part"])
            reboot = True
    except Exception as e:
        xbmcgui.Dialog().ok("Starting Raspbian", "Error", str(e))

    if reboot:
        os.system("reboot")
