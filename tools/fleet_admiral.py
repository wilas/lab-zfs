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
import re
import json
import os
import sys
import subprocess

import zfswrapper as zfs

def create_disc(filename):
    """Creates 64MB demo file/disc for given filename only if file not exist.
    
    :param filename: path to file
    :type filename: str
    :returns: bool -- True if disc was created or False if disc already exist or error during creation.
    """
    if os.path.isfile(filename):
        print 'file exist', filename
        return False
    result = subprocess.call(['dd', 'if=/dev/zero', 'of=%s' % filename, 'bs=1024', 'count=65536'])
    if result: #returncode > 0, mean error during disc creation
        print 'creation error', filename
        return False
    subprocess.call(["ls","-l",filename])
    return True

def load_zfs_scheme(filename):
    """Returns python object from given json file
    
    :param filename: path to json file
    :type filename: str
    :returns: dict -- python reprezentation of zfs datasets
    """
    with open(filename,'r') as file:
        zfs_scheme = json.load(file)
    file.close()
    return zfs_scheme

def create_filesystem(zfs_scheme):
    """Creates zfs datasets from given zfs_scheme.
    
    :param zfs_scheme: python reprezentation of zfs datasets
    :type zfs_scheme: dict
    :raises: :class:`zfswrapper.ZfsException`
    """
    for zpool  in zfs_scheme:
        # extract discs from vdev description
        reserved = ['mirror', 'raidz[0-9]*', 'spare', 'log', 'cache']
        regex = re.compile(r'|'.join(reserved))
        vdev = zfs_scheme[zpool]['vdev']
        discs = filter(lambda x: not regex.search(x), vdev)
        # create discs to play
        for disc in discs:
            create_disc(disc)
        # create zpool
        if not zfs.zpool_list(zpool):
            zfs.zpool_create(zpool, vdev)
        # create zfs
        for fs in zfs_scheme[zpool]['fs']:
            if not zfs.zfs_list(fs['name']):
                zfs.zfs_create(fs['name'])

if __name__ == '__main__':
    starfleet = 'json_galaxy/starfleet.json'
    # json file as an argument
    if len(sys.argv) > 1:
        starfleet = sys.argv[1]
    zfs_scheme =  load_zfs_scheme(starfleet)
    create_filesystem(zfs_scheme)

