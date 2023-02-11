for i in $(pxctl s l | grep [0-9] | awk '{print $1}'); do pxctl s d $i ; done
