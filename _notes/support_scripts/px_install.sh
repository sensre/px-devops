latest_stable=$(curl -fsSL 'https://install.portworx.com?type=dock&stork=false' | awk '/image: / {print $2}')

sudo docker run --entrypoint /runc-entry-point.sh     --rm -i --privileged=true     -v /opt/pwx:/opt/pwx -v /etc/pwx:/etc/pwx     $latest_stable

sudo /opt/pwx/bin/px-runc install -e -c px-sen -k etcd:http://10.15.84.40:2379,etcd:http://10.15.84.39:2379,etcd:http://10.15.84.38:2379 -s /dev/sdd -d ens160 -m ens160

sudo systemctl daemon-reload

sudo systemctl enable portworx

sudo systemctl start portworx

