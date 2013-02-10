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

import string
import time

import zfswrapper as zfs

# Settings
_filter_prefix = 'hanoi'
_backup_control_nr = 'backup:cycle_nr'
_backup_property = 'backup:class'


def _get_class_list(nr):
    """Return list nr first classes from 26 letter alphabet.
    For nr>26 return also list 26 first classes. """
    return list(string.uppercase)[:nr]


def _get_next_control_number(snapshots_list, modulov):
    """Return next number for backup_control_nr"""
    next_control_nr = 0
    if snapshots_list:
        #help if we have some old snapshots without control_nr or with some bugs...
        try:
            prev = int(snapshots_list[0][_backup_control_nr])
        except ValueError:
            next_control_nr = 0
        else:
            next_control_nr = (prev + 1) % modulov
    return next_control_nr


def _get_current_hanoi_state(fs, snapshots_list):
    """Return list of dictionaries, where each element list is 
    snapshot properties dictionary. List is sorted by snapshot creation time.
    Snapshot list contain only snapshot with prefix name equal  _filter_prefix.
    """
    filter_snapshots = filter(lambda x: x.startswith('%s@%s' % (fs, _filter_prefix)), snapshots_list)
    #TODO: filter out broken - no control_num, no_class... ?!

    info_list = []
    for snapshot in filter_snapshots:
        # get info about each snapshot, may return None or empty dict
        info = zfs.zfs_get(snapshot, property='name,creation,%s,%s' % (_backup_property, _backup_control_nr))
        info_list.append(info)

    srt_snapshots = sorted(info_list, key=lambda snap: snap['creation'], reverse=True )
    for snap in srt_snapshots:
        print snap
    return srt_snapshots


def _gen_snapshot_tag():
    # create snapshot tag using time
    timestamp = time.strftime('%Y%m%d%H%M%S')
    tag = '%s-%s' % (_filter_prefix, timestamp)
    return tag


def backup_guard(fs, class_nr):
    """Guard tower of hanoi backup rotation scheme for ZFS:
    http://en.wikipedia.org/wiki/Backup_rotation_scheme#Tower_of_Hanoi

    .. note::
        It cover [2^(n-2)+1; 2^(n-1)] days/time_units, where n is class_nr.

        Fast calculation: 26 classes cover at least 2^24 + 1 = 16777217 time_units
    
    :param fs: zfs filesystem/volume name to backup
    :type fs: str
    :param class_nr: number of class used for rotation
    :type class_nr: int
    :raises: zfswrapper.ZfsException
    """
    # tag for new snapshot
    snp_tag = _gen_snapshot_tag()
    # get all snapshots given fs
    all_snapshots = zfs.zfs_list(fs=fs, types='snapshot') or []
    # get list of snapshots and properties sorted by creation time.
    srt_snapshots = _get_current_hanoi_state(fs, all_snapshots)
    _hanoi_builder(fs, snp_tag, class_nr, srt_snapshots)


def backup_guard_recurse(pool, class_nr):
    """Recurse version tower of hanoi backup rotation scheme for ZFS:
    http://en.wikipedia.org/wiki/Backup_rotation_scheme#Tower_of_Hanoi
    Snapshots are taken atomically, so that all recursive snapshots corre-
    spond to the same moment in time.

    :param fs: zpool name to backup (snapshot make also for all child zfs)
    :type fs: str
    :param class_nr: number of class used for rotation
    :type class_nr: int
    :raises: zfswrapper.ZfsException
    """
    # tag for new snapshot
    snp_tag = _gen_snapshot_tag()
    unknown_label = 'unknown'
    unknown_control_nr = 'X'

    # make new recursive snapshot - if problem ZfsException is throw
    zfs.zfs_snapshot(fs=pool, tag=snp_tag, recurse=True, 
            properties={_backup_property:unknown_label, _backup_control_nr:unknown_control_nr})
    # get all filesystem given pool
    all_fs = zfs.zfs_list(fs=pool, types='filesystem') or []
    for fs in all_fs:
        print 'fs', fs
        ## Note: you can set class_num per filesystem, exclude some zfs filesystems, e.g. pool
        # get all snapshots given fs
        fs_snapshots = zfs.zfs_list(fs=fs, types='snapshot') or []
        # get list of snapshots and properties sorted by creation time. First is allready taken snapshot.
        srt_snapshots = _get_current_hanoi_state(fs, fs_snapshots)[1:]
        # get control number - useful for debuging and checking hanoi rotation scheme
        _hanoi_builder(fs, snp_tag, class_nr, srt_snapshots, recurse=True)


def _hanoi_builder(fs, tag, class_nr, srt_snapshots, recurse=False):
    """Help function, take care for hanoi status
    
    :raises: zfswrapper.ZfsException
    """
    class_list = _get_class_list(class_nr) #e.g. ['A', 'B', 'C', 'D', 'E']
    modulov = 2**(class_nr-1) #useful to create control number
    next_control_nr = _get_next_control_number(srt_snapshots, modulov)

    for ptr in range(0, class_nr):
        # last must be replaced anyway;  snapshot has proper class
        last_class = (ptr == class_nr-1)
        has_proper_class = False
        if len(srt_snapshots) > ptr:
            has_proper_class = (srt_snapshots[ptr][_backup_property] == class_list[ptr])
        if not last_class and has_proper_class:
            continue
        else:
            # Hanoi rotation method has the drawback of overwriting
            # the very first backup (day 1 of the cycle) after only two days. 
            # However, this can easily be overcome by starting 
            # on the last day of a cycle.
            class_label = class_list[ptr]
            if not srt_snapshots:
                class_label = class_list[-1]

            # get all old snapshots same class
            old_snapshot = filter(lambda x: x[_backup_property]==class_label, srt_snapshots)

            print "to create: {'%s': '%s', '%s': '%s'}" % (_backup_property, class_label, _backup_control_nr, next_control_nr)
            if recurse:
                snp_already_taken = '%s@%s' % (fs, tag)
                # mark already taken snapshot with proper class and control_nr - if problem ZfsException is throw
                zfs.zfs_set(snp_already_taken, _backup_control_nr, next_control_nr)
                zfs.zfs_set(snp_already_taken, _backup_property, class_label)
            else:
                # make new snapshot - if problem ZfsException is throw
                zfs.zfs_snapshot(fs, tag, properties={_backup_property:class_label, _backup_control_nr:next_control_nr})
            # delete old snapshots same class, only if new snapshot was taken - if probelm ZfsException is throw
            for old in old_snapshot:
                print 'to destroy:', old
                zfs.zfs_destroy(old['name'])
            # job done
            break


if __name__ == '__main__':
    class_nr = 5
    
    print 'Guard zfs'
    fs = 'galaxy01/fleet11'
    backup_guard(fs, class_nr)
    
    print '\nGuard zpool'
    pool = 'galaxy03'
    _filter_prefix = 'tower'
    backup_guard_recurse(pool, class_nr)

