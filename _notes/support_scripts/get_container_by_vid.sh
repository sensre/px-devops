#!/bin/bash
# usage:  pxvol.sh [vol_id]
# if volume_id is not specified all volumes will be listed

exec 2>/dev/null
vol=pxd${1}; [ $vol ] || vol="pxd"

echo "Host Processes Using ${vol} (No Containers)"
echo "==============================================="
echo "     PID              CMD  STATE  MOUNT"
for mnt in $((IFS=/; grep ${vol} /proc/*/mounts | while read line; do set -- $line; grep -qE "name=.*/(kubepods|docker|portworx\.service)/" /proc/${3}/cgroup || grep ${vol} /proc/${3}/mounts | awk '{ print $2 }';  done) | sort | uniq); do for pid in $(fuser -c ${mnt}); do awk -v mnt=${mnt} '{ printf("%8d  %15s  %5s  %s\n", $1, $2, $3, mnt) }' /proc/${pid}/stat; done; done


echo ""
echo "Docker Containers Using ${vol}"
echo "========================================"
for cid in $((IFS=/; grep ${vol} /proc/*/mounts | while read line; do set -- $line; grep -E "name=.*/(kubepods|docker)/" /proc/${3}/cgroup; done) | grep -o '[^/]*$' | sort | uniq); do docker ps --filter "id=${cid}"; done 2>/dev/null


echo ""
echo "Mount Points for ${vol}"
echo "========================================"
grep ${vol} /proc/*/mounts | awk '{ print $2 }' | sort | uniq
