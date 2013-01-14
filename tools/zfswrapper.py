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

# Read before use:
# - zfswrapper tested with ZFS pool version 28 #zpool upgrade -v
# - zfswrapper.zfs_get not work with white space in pool, fs and snapshot name.

import subprocess

_zfs = '/sbin/zfs'
_zpool = '/sbin/zpool'

class ZfsException(Exception):

    def __init__(self, command, error_code, message):
        self.command = command
        self.error_code = error_code
        self.message = message

    def __str__(self):
        return repr('Zfs execute %s, error_code:%s, %s' % 
                (self.command, self.error_code, self.message))
    

def _run(args):
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)
    message = proc.communicate()[0].rstrip()
    if proc.returncode:
        raise ZfsException(args, proc.returncode, message)
    return message

def zfs_create(fs, properties={}):
    cmd = [_zfs, 'create']
    for property, value in properties.iteritems():
        cmd += ['-o','%s=%s' % (property, value)]
    cmd += [fs]
    _run(cmd)

def zfs_destroy(fs, options=None):
    cmd = [_zfs, 'destroy']
    if options:
        cmd += [options]
    cmd += [fs]
    _run(cmd)

def zfs_get(fs, property='all'):
    cmd = [_zfs, 'get', '-Hp', '-o', 'property,value', property, fs]
    try:
        output = _run(cmd)
    except ZfsException:
        return {}
    properties={}
    for desc in output.splitlines():
       prty, val  = desc.split()
       properties[prty] = val
    return properties

def zfs_list(fs=None, types='filesystem,snapshot', depth=None):
    cmd = [_zfs, 'list', '-rH', '-o', 'name']
    if types:
        cmd += ['-t', types]
    if depth:
        cmd += ['-d', depth]
    if fs:
        cmd += [fs]
    try:
        output = _run(cmd)
    except ZfsException:
        return None
    if not output or output.startswith('no datasets available'):
        return None
    return output.splitlines()

def zfs_set(fs, property, value):
    cmd = [_zfs, 'set', '%s=%s' % (property, value), fs]
    _run(cmd)

def zfs_snapshot(fs, tag, recursive=False, properties={}):
    cmd = [_zfs, 'snapshot']
    if recursive:
        cmd += ['-r']
    for property, value in properties.iteritems():
        cmd += ['-o','%s=%s' % (property, value)]
    cmd += ['%s@%s' % (fs, tag)]
    _run(cmd)

def zpool_add(pool, vdev):
    """vdev is a list"""
    cmd = [_zpool, 'add', '-f', pool] + vdev
    _run(cmd)

def zpool_attach(pool, device, new_device):
    cmd = [_zpool, 'attach', '-f', pool, device, new_device]
    _run(cmd)

def zpool_create(pool, vdev, properties={}):
    """vdev is a list"""
    cmd = [_zpool, 'create']
    for property, value in properties.iteritems():
        cmd += ['-o','%s=%s' % (property, value)]
    cmd += [pool]
    cmd += vdev
    _run(cmd)

def zpool_destroy(pool):
    cmd = [_zpool, 'destroy', '-f', pool]
    _run(cmd)

def zpool_detach(pool, device):
    cmd = [_zpool, 'detach', pool, device]
    _run(cmd)

def zpool_list(pool=None):
    cmd = [_zpool, 'list', '-H', '-o', 'name']
    if pool:
        cmd += [pool]
    try:
        output = _run(cmd)
    except ZfsException:
        return None
    if not output or output.startswith('no pools available'):
        return None
    return output.splitlines()

