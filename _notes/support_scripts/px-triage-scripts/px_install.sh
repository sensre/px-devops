latest_stable=$(curl -fsSL 'https://install.portworx.com?type=dock&stork=false' | awk '/image: / {print $2}')

sudo docker run --entrypoint /runc-entry-point.sh     --rm -i --privileged=true     -v /opt/pwx:/opt/pwx -v /etc/pwx:/etc/pwx     $latest_stable

sudo /opt/pwx/bin/px-runc install -e -c RK_1_10_Mar_18_01_19_UTC -k etcd:http://70.0.5.213:2379,etcd:http://70.0.5.211:2379,etcd:http://70.0.5.212:2379 -s /dev/sdd -d enp0s3 -m enp0s3


sudo systemctl daemon-reload

sudo systemctl enable portworx

sudo systemctl start portworx

