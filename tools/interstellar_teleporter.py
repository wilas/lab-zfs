import zfswrapper as zfs


send_fs ='galaxy01/fleet11'
send_tag = 'satellite-red01'
to_send = '%s@%s' % (send_fs, send_tag)

# create local snapshot if not exist
if not zfs.zfs_list(fs=to_send):
    zfs.zfs_snapshot(send_fs, send_tag)

# replication simulator
# recv_fs can't exist on recv_host, otherwise error is risen
recv_fs = 'galaxy_slave01/fleet11_alfa'
#recv_fs = 'galaxy_slave01/fleet11_beta'
zfs.zfs_teleport_snapshot(send_fs, send_tag, recv_fs, recv_host='zepto') #remote

recv_fs = 'galaxy02/fleet11_alfa'
#recv_fs = 'galaxy02/fleet11_beta'
zfs.zfs_teleport_snapshot(send_fs, send_tag, recv_fs) #local
