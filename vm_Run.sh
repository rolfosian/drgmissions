#!/bin/bash

#requires sudoers entries:
# %whoami ALL=(root) NOPASSWD: /usr/bin/virsh domstate * 
# %whoami ALL=(root) NOPASSWD: /bin/bash /path/to/vm_Run.sh
# or simply run directly as root

# i had to run dos2unix on this piece of shit to get it to run properly on debian after editing it on windows because it was riddled with ghost newlines and return carriages

# Crontab entry:
# 50 10 * * 4 sudo /bin/bash /path/to/vm_Run.sh 

# Be wary of force shutoff. Windows doesn't like it and there's a chance it will initiate a system repair, especially if you do it during startup.

VM_NAME="win10"

virsh --connect qemu:///system start "$VM_NAME"
virt-manager --connect qemu:///system --show-domain-console "$VM_NAME"

while true; do
    vm_state=$(sudo virsh domstate $VM_NAME)

    if [[ $vm_state == "shut off" ]]; then
        echo "VM is shut down. Exiting..."
        break
    fi

    sleep 3
done

killall virt-manager
exit 0