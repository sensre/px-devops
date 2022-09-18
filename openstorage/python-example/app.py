import grpc
import argparse
from openstorage import api_pb2
from openstorage import api_pb2_grpc
from openstorage import connector

USAGE='''
$ python app.py [options]
'''

# Initialize app cli arguments
parser = argparse.ArgumentParser(usage=USAGE, description='Example Python OpenStorage SDK Application')
parser.add_argument('--cafile', dest='cafile', default='', help='CA file to connect to server using TLS')
parser.add_argument('--token', dest='token', default='', help='Authorization token')
parser.add_argument('--address', dest='address', default='127.0.0.1:9100', help='Address of server as <address>:<port>')
args = parser.parse_args()

c = connector.Connector(endpoint=args.address, cafile=args.cafile, token=args.token)
channel = c.connect()

try:
    # Cluster connection
    clusters = api_pb2_grpc.OpenStorageClusterStub(channel)
    ic_resp = clusters.InspectCurrent(api_pb2.SdkClusterInspectCurrentRequest())
    print('Connected to {0} with status {1}'.format(
        ic_resp.cluster.id,
        api_pb2.Status.Name(ic_resp.cluster.status)
    ))

    # Create a volume
    volumes = api_pb2_grpc.OpenStorageVolumeStub(channel)
    v_resp = volumes.Create(api_pb2.SdkVolumeCreateRequest(
        name="myvol",
        spec=api_pb2.VolumeSpec(
            size=100*1024*1024*1024,
            ha_level=3,
            format=api_pb2.FS_TYPE_EXT4,
        )
    ))
    print('Volume id is {0}'.format(v_resp.volume_id))

    # Create a snapshot
    snap = volumes.SnapshotCreate(api_pb2.SdkVolumeSnapshotCreateRequest(
        volume_id=v_resp.volume_id,
        name="mysnap"
    ))
    print('Snapshot created with id {0}'.format(snap.snapshot_id))

    # Create a credentials
    creds = api_pb2_grpc.OpenStorageCredentialsStub(channel)
    cred_resp = creds.Create(api_pb2.SdkCredentialCreateRequest(
        name='aws',
        aws_credential=api_pb2.SdkAwsCredentialRequest(
            access_key='dummy',
            secret_key='dummy',
            endpoint='dummy',
            region='dummy'
        )
    ))
    print('Credential id is {0}'.format(cred_resp.credential_id))

    # Create backup
    backups = api_pb2_grpc.OpenStorageCloudBackupStub(channel)
    backup_resp = backups.Create(api_pb2.SdkCloudBackupCreateRequest(
        volume_id=v_resp.volume_id,
        credential_id=cred_resp.credential_id,
        full=False
    ))

    # Get status
    status_resp = backups.Status(api_pb2.SdkCloudBackupStatusRequest(
        volume_id=v_resp.volume_id
    ))
    backup_status = status_resp.statuses[v_resp.volume_id]
    print('Status of the backup is {0}'.format(
        api_pb2.SdkCloudBackupStatusType.Name(backup_status.status)
    ))

    # Show history
    history = backups.History(api_pb2.SdkCloudBackupHistoryRequest(
        src_volume_id=v_resp.volume_id
    ))
    print('Backup history for volume {0}'.format(v_resp.volume_id))
    for item in history.history_list:
        print('Time:{0} Status:{1}'.format(
            item.timestamp.ToJsonString(),
            api_pb2.SdkCloudBackupStatusType.Name(item.status)
        ))

except grpc.RpcError as e:
    print('Failed: code={0} msg={1}'.format(e.code(), e.details()))