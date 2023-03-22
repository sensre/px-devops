#/bin/bash

set -e

dryRun="true"
for i in "$@"
do
case $i in
    --date)
        echo "Deleting cloudsnaps older than: $2"
        oldDate=$2
        shift
        shift
        ;;
    --dry-run)
        dryRun=$2
        shift
        shift
        ;;
    --cred)
        echo "Credential: $2"
        cred=$2
        shift
        shift
        ;;
esac
done

echo "Dry run: $dryRun"
echo ""

csToDelete=$(/opt/pwx/bin/pxctl cs l --cred-id $cred -j  | jq --arg e "$oldDate" 'map(select(.Timestamp | . <= $e))')

echo "The following cloudsnaps will be deleted:"
echo $csToDelete | jq '.[] | {ID,Timestamp}'

if [ $dryRun == "false" ] ; then
        echo $csToDelete | jq -r '.[].ID' | xargs -n1 /opt/pwx/bin/pxctl cs d --cred-id $cred -s
fi
