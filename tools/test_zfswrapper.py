import unittest
import zfsunittest
import zfswrapper as zfs

class ZfswrapperTest(zfsunittest.ZfsTestCase):
    """Inherit from :class:`zfsunittest.ZfsTestCase`"""

    def setUp(self):
        self.zpool_name = 'unittest01'
        self.fs_names = ['unittest01/mine01', 'unittest01/mine02', 'unittest01/mine03']
        self.snapshots = ['unittest01/mine01@coal001', 'unittest01/mine01@coal002', 'unittest01/mine02@copper001']
        self._zpool_generate(self.zpool_name, fs_names=self.fs_names, snapshots=self.snapshots)

    def tearDown(self):
        self._zpool_clean(self.zpool_name)

    def test_zfs_list(self):
        """zfs_list without args - return list all filesystems and snapshots. By default volumes are not included."""
        expected_fs = ['unittest01', 'unittest01/mine01', 'unittest01/mine02', 'unittest01/mine03', 
                'unittest01/mine01@coal001', 'unittest01/mine01@coal002', 'unittest01/mine02@copper001']
        zlist = zfs.zfs_list()
        for fs in expected_fs:
            self.assertTrue(fs in zlist)
    
    def test_zfs_list_defined_fs(self):
        """zfs_list with defined fs - return list only filesystems and snapshots given fs"""
        expected_fs = ['unittest01/mine01', 'unittest01/mine01@coal001', 'unittest01/mine01@coal002']
        not_expected_fs = ['unittest01', 'unittest01/mine02', 'unittest01/mine03', 'unittest01/mine02@copper001']
        zlist = zfs.zfs_list(fs='unittest01/mine01')
        for fs in expected_fs:
            self.assertTrue(fs in zlist)
        for fs in not_expected_fs:
            self.assertFalse(fs in zlist)
    
    def test_zfs_list_defined_types(self):
        """zfs_list with defined types - return list all 'types' for given fs"""
        expected_fs = ['unittest01/mine01@coal001', 'unittest01/mine01@coal002', 'unittest01/mine02@copper001']
        not_expected_fs = ['unittest01', 'unittest01/mine01', 'unittest01/mine02', 'unittest01/mine03']
        zlist = zfs.zfs_list(types='snapshot')
        for fs in expected_fs:
            self.assertTrue(fs in zlist)
        for fs in not_expected_fs:
            self.assertFalse(fs in zlist)
    
    def test_zfs_list_not_existing_fs(self):
        """zfs_list return None if given fs not exist"""
        zlist = zfs.zfs_list(fs='non_existing_filesystem')
        self.assertEqual(zlist, None)

if __name__ == '__main__':
    unittest.main()
