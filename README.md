# Description

Playing with ZFS file system.

## VM description:

 - OS: Scientific linux 6
 - machine with zfs: zetta.farm
 - machine with zfs: zepto.farm

## Howto

 - after repo clone run: `git submodule update`
 - create SL64_box using [veewee-SL64-box](https://github.com/wilas/veewee-SL64-box)
 - copy ssh_keys from [ssh-gerwazy](https://github.com/wilas/ssh-gerwazy)

```
    vagrant up 
    ssh root@77.77.77.99 #zetta
    ssh root@77.77.77.98 #zepto
    vagrant destroy
```

## Good to know:

 - why not fuse: http://lists.debian.org/debian-user/2012/05/msg01026.html
 - check zpool: `zpool status` or `zpool list`
 - check zfs: `zfs list -t filesystem,snapshot`
 - destroy zpool: `zpool destroy pool_name`
 - destroy zfs: `zfs destroy -r zfs_name`
 - destroy snapshot: `zfs destroy -r snapshot_name`
 - fleet_admiral.py - setup demo from json file
 - zfsguard.py - tower_of_hanoi backup rotation scheme using zfs snapshot: http://en.wikipedia.org/wiki/Backup_rotation_scheme#Tower_of_Hanoi
 - interstellar_teleporter.py - send and receive demo
 - py-zfswrapper - ZFS filesystem wrapper for python: https://github.com/wilas/py-zfswrapper
 
## Play time:

backup and restore
```
    python /vagrant/tools/fleet_admiral.py #setup demo 
    df -h
    cd /galaxy01/fleet11 && echo 'fleet11-red' > test.txt
    cat /galaxy01/fleet11/test.txt
    zfs snapshot galaxy01/fleet11@moon
    cd /galaxy01/fleet11 && echo 'fleet11-green' > test.txt
    cat /galaxy01/fleet11/test.txt
    zfs rollback -r galaxy01/fleet11@moon
    cat /galaxy01/fleet11/test.txt
```

hanoi backup rotation scheme
```
    python /vagrant/tools/fleet_admiral.py #setup demo 
    python /vagrant/tools/zfsguard.py #run as many times you want, but not too frequently (e.g. 1 per sec.)
    zfs list -t snapshot,filesystem
```

send and receive
```
    # ssh to zetta
    python /vagrant/tools/fleet_admiral.py #setup demo
    cd /galaxy01/fleet11 && echo 'fleet11-red' > test.txt
    zfs list -t filesystem,snapshot
    
    # ssh to zepto
    python /vagrant/tools/fleet_admiral.py json_galaxy/starfleet_slave.json #setup demo
    ls -la /galaxy_slave01/fleet11_alfa
    zfs list -t filesystem,snapshot
    
    # ssh to zetta
    python /vagrant/tools/interstellar_teleporter.py #run send/receive demo
    cat /galaxy02/fleet11_alfa/test.txt
    zfs list -t filesystem,snapshot
    
    # ssh to zepto
    cat /galaxy_slave01/fleet11_alfa/test.txt
    zfs list -t filesystem,snapshot
    
    # want play again? edit recv_fs in interstellar_teleporter.py to some non-existing or remove some datasets
```

## Bibliography

### Zfsonlinux

 - Zfsonlinux faq: http://zfsonlinux.org/faq.html
 - Zfsonlinux development: https://github.com/zfsonlinux/zfs
 - Install Zfs on centos6: http://pingd.org/2012/installing-zfs-raid-z-on-centos-6-2-with-ssd-caching.html
 - Install Zfs on centos6: http://prefetch.net/blog/index.php/2012/02/13/installing-zfs-on-a-centos-6-linux-server/

### General ZFS

 - !!! man zfs / man zpool
 - !! Zfs demonstarion tutorial: http://www.exitcertified.com/newsletter/2007-august/resources/zfs_demo.pdf
 - !! Zfs cheetsheet: http://lildude.co.uk/zfs-cheatsheet
 - Why Zfs: http://blog.icloudhosting.com/2011/10/27/the-beauty-of-zfs/
 - Best practices: http://www.solarisinternals.com/wiki/index.php/ZFS_Best_Practices_Guide 
 - Zfs admin guide: http://docs.oracle.com/cd/E19253-01/819-5461/zfsover-1/index.html
 - Zfs properties: http://docs.oracle.com/cd/E19253-01/819-5461/gazss/index.html
 - Zfs quick tutorial: http://www.mattzone.com/site/index.php?name=News&file=article&sid=3

### More ZFS
 - Send/receive: http://docs.oracle.com/cd/E19963-01/html/821-1448/gbchx.html
 - Send/receive fun: http://www.128bitstudios.com/2010/07/23/fun-with-zfs-send-and-receive/
 - Zfs replication: http://phillipcooper.co.uk/2011/12/zfs-replication/
 - Incremental backups over ssh: http://www.aisecure.net/2012/01/11/automated-zfs-incremental-backups-over-ssh/
 - Zfs raid-z: http://www.freebsd.org/doc/en_US.ISO8859-1/books/handbook/filesystems-zfs.html


## TODO

 - Unix/Unix-like (illumos, smartOS, omnios, freebsd) vagrant box


## Copyright and license

Copyright 2013, Kamil Wilas (wilas.pl)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this work except in compliance with the License.
You may obtain a copy of the License in the LICENSE file, or at:

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

