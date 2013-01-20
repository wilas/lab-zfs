#
# Copyright 2013, Kamil Wilas (wilas.pl)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# src page: github.com/wilas/zfs-soup/
#

import zfswrapper as zfs


def replication_simulator():
    """Demo - send and receive snapshot.
    
    .. warning::
        recv_fs can't exist on recv_host, otherwise error is risen
    """

    send_fs ='galaxy01/fleet11'
    send_tag = 'satellite-red01'
    to_send = '%s@%s' % (send_fs, send_tag)

    # create local snapshot to teleport if not exist
    if not zfs.zfs_list(fs=to_send):
        zfs.zfs_snapshot(send_fs, send_tag)

    # Remote repl. - using ssh
    recv_fs = 'galaxy_slave01/fleet11_alfa'
    #recv_fs = 'galaxy_slave01/fleet11_beta'
    zfs.zfs_teleport_snapshot(send_fs, send_tag, recv_fs, recv_host='zepto')

    # Local repl.
    recv_fs = 'galaxy02/fleet11_alfa'
    #recv_fs = 'galaxy02/fleet11_beta'
    zfs.zfs_teleport_snapshot(send_fs, send_tag, recv_fs)


if __name__ == '__main__':
    replication_simulator()
