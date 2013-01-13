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
# src page: github.com/wilas/zfs-soup/tools
#

import string
import time

import discobolus
import zfswrapper as zfs

def _get_class_list(nr):
    """Return list nr first classes from 26 letter alphabet.
    For nr>26 return also list 26 first classes. """
    return list(string.uppercase)[:nr]


def backup_guard(fs, class_nr):
    """http://en.wikipedia.org/wiki/Backup_rotation_scheme#Tower_of_Hanoi
    cover [2^(n-2)+1; 2^(n-1)] days/time_units
    Info: 26 classes cover 2^24 + 1 = 16777217 time_units
    """

    filtr_prefix = 'hanoi'
    backup_control_nr = 'backup:cycle_nr'
    backup_property = 'backup:class'
    class_list = _get_class_list(class_nr)
    next_control_nr = 0
    modulov = 2**(class_nr-1)
    
    all_snapshots = zfs.zfs_list(fs=fs, types='snapshot') or []

    filtr_snapshots = filter(lambda x: x.startswith('%s@%s' % (fs, filtr_prefix)), all_snapshots)
    #TODO: filtr out broken - no control_num, no_class ... ?!

    info_list = []
    for snapshot in filtr_snapshots:
        info = zfs.zfs_get(snapshot, property='name,creation,%s,%s' % (backup_property, backup_control_nr))
        info_list.append(info)

    srt_snapshots = sorted(info_list, key=lambda snap: snap['creation'], reverse=True )
    for snap in srt_snapshots:
        print snap

    # get next_control_nr
    if srt_snapshots:
        #help if we have some old snapshots without control_nr or with some bugs...
        try:
            prev = int(srt_snapshots[0][backup_control_nr])
        except ValueError:
            next_control_nr = 0
        else:
            next_control_nr = (prev + 1) % modulov

    for ptr in range(0, class_nr):
        # last must by replaced anyway, co jak zmniejsze ilosc tasm ? i zostana stare backupy z tagami wyzszymi nie do usuniecia ?
        # to wszystko sie zawiesi..... jak hanoi sie ulozy....
        # ostatnia klase bede obrzadzal, mam snapshota to zobaczenia, znapszot jest poprawnej klasy 
        if (len(class_list)-1>ptr) and (len(srt_snapshots) > ptr) and (srt_snapshots[ptr][backup_property] == class_list[ptr]):
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
            old_snapshot = filter(lambda x: x[backup_property]==class_list[ptr], srt_snapshots)

            # create snapshot tag using time
            #timestamp = time.strftime('%Y%m%d%H%M%S')
            timestamp = time.time()
            tag = '%s-%s' % (filtr_prefix, timestamp)

            try:
                print "to create: {'%s': '%s', '%s': '%s'}" % (backup_property, class_label, backup_control_nr, next_control_nr)
                # make new snapshot - if not made then exception is throw from zfswrapper  
                zfs.zfs_snapshot(fs, tag, properties={backup_property:class_label, backup_control_nr:next_control_nr})
            except ZfsException as e:
                print 'Create new snapshot fail (FYI: old snapshots not destroyed):', e
            else:
                # delete old snapshots if new snapshot was taken
                for old in old_snapshot:
                    print 'to destroy:', old
                    zfs.zfs_destroy(old['name'])
            # job done
            break

if __name__ == '__main__':
    fs='galaxy01/fleet11'
    backup_guard(fs, 5)
