sudo systemctl stop portworx
sudo docker rm portworx.service -f
sudo rm /etc/systemd/system/portworx.service -f
sudo rm /etc/systemd/system/dcos.target.wants/portworx.service -f
sudo rm /etc/systemd/system/multiuser.target.wants/portworx.service
sudo systemctl daemon-reload
sudo /opt/pwx/bin/pxctl service node-wipe --all
sudo chattr -i /etc/pwx/.private.json
sudo rm -rf /etc/pwx
sudo umount /opt/pwx/oci
sudo rm -rf /opt/pwx
sudo rmmod px -f