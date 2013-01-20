import os
import subprocess
import tempfile
import unittest

class ZfsTestCase(unittest.TestCase):
    """Class with helpful methods for clear testing zfs.
    
    Inherit from :class:`unittest.TestCase`
    """

    def _zpool_generate(self, zpool_name, fs_names=[], snapshots=[]):
        """Generate temporary pool"""
        # create disc as 64MB tempfile
        handle, self.path = tempfile.mkstemp('.zfsdisc')
        with os.fdopen(handle, 'wb') as f:
            f.seek(64*1048576-1)
            f.write('\0')
        f.close()
        # create pool
        subprocess.call(['zpool', 'create', '-o', 'cachefile=none', zpool_name, self.path])
        # create fs
        for fs in fs_names:
            subprocess.call(['zfs', 'create', '-p', fs])
        # create snapshots
        for snapshot in snapshots:
            subprocess.call(['zfs', 'snapshot', snapshot])
        #subprocess.call(['ls', '-la', self.path])
        #subprocess.call(['zpool', 'status', zpool_name])
        #subprocess.call(['zfs', 'list', '-t', 'snapshot,filesystem'])

    def _zpool_clean(self, zpool_name):
        """Remove temporary pool"""
        # destroy pool
        subprocess.call(['zpool', 'destroy', zpool_name])
        # remove temp disc
        subprocess.call(['rm', '-rf', self.path])
