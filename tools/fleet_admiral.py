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
import re
import json
import os
import subprocess

import zfswrapper as zfs

def _create_disc(filename):
    """create 64MB disck using file if file not exist"""
    if os.path.isfile(filename):
        print 'file exist', filename
        return False
    subprocess.call(['dd', 'if=/dev/zero', 'of=%s' % filename, 'bs=1024', 'count=65536'])
    subprocess.call(["ls","-l",filename])
    return True

def _load_zfs_scheme(filename):
    with open(filename,'r') as file:
        zfs_scheme = json.load(file)
    file.close()
    return zfs_scheme

def _create_filesystem(zfs_scheme):
    for zpool  in zfs_scheme:
        # extract discs from vdev description
        reserved = ['mirror', 'raidz[0-9]*', 'spare', 'log', 'cache']
        regex = re.compile(r'|'.join(reserved))
        vdev = zfs_scheme[zpool]['vdev']
        discs = filter(lambda x: not regex.search(x), vdev)
        # create discs to play
        for disc in discs:
            _create_disc(disc)
        # create zpool
        if not zfs.zpool_list(zpool):
            zfs.zpool_create(zpool, vdev)
        # create zfs
        for fs in zfs_scheme[zpool]['fs']:
            if not zfs.zfs_list(fs['name']):
                zfs.zfs_create(fs['name'])

if __name__ == '__main__':
    starfleet = 'starfleet.json'
    zfs_scheme =  _load_zfs_scheme(starfleet)
    _create_filesystem(zfs_scheme)

