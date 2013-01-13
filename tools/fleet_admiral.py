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
import json

import discobolus
import zfswrapper as zfs


def _load_zfs_scheme(filename):
    with open(filename,'r') as file:
        zfs_scheme = json.load(file)
    file.close()
    return zfs_scheme

def _create_filesystem(zfs_scheme):
    for zpool  in zfs_scheme:
        # create disc to play
        disc = zfs_scheme[zpool]['disc']
        discobolus.create_disc(disc)
        # create zpool
        if not zfs.zpool_list(zpool):
            zfs.zpool_create(zpool, disc)
        # create zfs
        for fs in zfs_scheme[zpool]['fs']:
            if not zfs.zfs_list(fs['name']):
                zfs.zfs_create(fs['name'])

if __name__ == '__main__':
    starfleet = 'starfleet.json'
    zfs_scheme =  _load_zfs_scheme(starfleet)
    _create_filesystem(zfs_scheme)

