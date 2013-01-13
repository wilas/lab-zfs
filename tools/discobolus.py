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

import os
import subprocess

def create_disc(filename):
    """create 64MB disck using file if file not exist"""
    if os.path.isfile(filename):
        print 'file exist', filename
        return False
    subprocess.call(['dd', 'if=/dev/zero', 'of=%s' % filename, 'bs=1024', 'count=65536'])
    subprocess.call(["ls","-l",filename])
    return True
