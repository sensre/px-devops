#!/bin/bash
set -euo pipefail
SRC=$1
SECRETPATH="pwx/crypt"
RSYNCLOG="/tmp/${SRC}-rsync.log"
SIZE=$(pxctl volume inspect $SRC | grep Size | cut -d':' -f2 | cut -d'.' -f1 | sed 's/^ *//g')
CRED=$(pxctl credentials list | tail -1 | awk {'print $1'})
BACKID=$(pxctl cloudsnap backup --full --cred-id ${CRED} ${SRC} | cut -d" " -f7)
echo
echo "Backing up: ${SRC}"
echo "###########"
while [ "$(pxctl cloudsnap status --name ${BACKID} | tail -1 | awk {'print $3'})" != "Backup-Done" ]; do 
	echo 'Backup in progress'
	sleep 1
done
echo
echo "Deleting unencryted volume: ${SRC}..."
yes yes | pxctl volume delete ${SRC} || true
echo
echo "Creating encrypted volume: ${SRC}..."
pxctl volume create --size ${SIZE} --repl 3 --secure --secret_key ${SECRETPATH}/${SRC} --label SECRET_NAME=${SECRETPATH}/${SRC} ${SRC}
echo
SNAPID=$(pxctl cloudsnap list | grep ${SRC} | tail -1 | awk {'print $3'})
RESTID=$(pxctl cloudsnap restore --snap ${SNAPID} --volume ${SRC}-nocrypt | cut -d":" -f3)
echo "Restoring: ${SRC}-nocrypt"
echo "##########"
while [ "$(pxctl cloudsnap status --name ${RESTID} | tail -1 | awk {'print $3'})" != "Restore-Done" ]; do
	echo 'Restore in progress'
	sleep 1
done
echo
echo "Preparing to clone ${SRC}-nocrypt to ${SRC}..."
pxctl host attach ${SRC}-nocrypt
sudo mkdir /var/lib/osd/mounts/${SRC}-nocrypt
pxctl host mount ${SRC}-nocrypt --path /var/lib/osd/mounts/${SRC}-nocrypt
pxctl host attach --secret_key ${SECRETPATH}/${SRC} ${SRC}
sudo mkdir /var/lib/osd/mounts/${SRC}
pxctl host mount ${SRC} --path /var/lib/osd/mounts/${SRC}
echo
echo "Cloning ${SRC}-nocrypt to ${SRC}..."
sudo -E rsync -azvP /var/lib/osd/mounts/${SRC}-nocrypt/ /var/lib/osd/mounts/${SRC}/ >> ${RSYNCLOG}
if [[ $? -ne 0 ]]; then
	echo "The rsync failed! Please see ${RSYNCLOG} for details!"
	echo "Exiting!"
	exit 1
fi
sudo rm ${RSYNCLOG}
echo "Cloning successful!"
echo
echo "Cleaning up..."
pxctl host unmount ${SRC} --path /var/lib/osd/mounts/${SRC}
pxctl host detach ${SRC}
pxctl host unmount ${SRC}-nocrypt --path /var/lib/osd/mounts/${SRC}-nocrypt
pxctl host detach ${SRC}-nocrypt
if [[ -f /var/lib/osd/mounts/${SRC} ]]; then
	sudo rm -r /var/lib/osd/mounts/${SRC}
fi
if [[ -f /var/lib/osd/mounts/${SRC}-nocrypt ]]; then
	sudo rm -r /var/lib/osd/mounts/${SRC}-nocrypt
fi
yes yes | pxctl volume delete ${SRC}-nocrypt || true
echo
echo "This is the ID of the last unencrypted snapshot: ${SNAPID}"
echo "You can manually delete it once you're confident the new encrypted volume is stable!"
echo