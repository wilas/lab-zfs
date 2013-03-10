class zfsonlinux {

    $baseurl = 'http://github.com/downloads/zfsonlinux'
    #since that version support for dkms (module will be automatically rebuilt when your kernel is updated)
    $version = hiera('zfsonlinux::version','0.6.0-rc12')

    $zfsdep = [ 'zlib-devel',
                'lsscsi',
                'libuuid-devel',
                'parted',
                'libblkid-devel',
                'e2fsprogs-devel',
                'libselinux-devel']

    package { $zfsdep:
        ensure => installed,
    }

    # Already installed via basic_package module:
    #gcc
    #make
    #wget
    #kernel-devel

    package { 'rpm-build':
        ensure => installed,
    }

    package { 'dkms':
        ensure => installed,
    }

    exec { 'get spl': #keep in files
        command => "wget -O /opt/spl-${version}.tar.gz ${baseurl}/spl/spl-${version}.tar.gz",
        path    => '/bin:/sbin:/usr/bin:/usr/sbin',
        creates => "/opt/spl-${version}.tar.gz",
        require => Package[$zfsdep, 'rpm-build', 'dkms', 'gcc', 'make', 'wget', 'kernel-devel'],
    }
    exec { 'unzip spl':
        command => "tar -xvzf /opt/spl-${version}.tar.gz -C /opt",
        path    => '/bin:/sbin:/usr/bin:/usr/sbin',
        creates => "/opt/spl-${version}",
        require => Exec['get spl'],
    }
    exec { 'build spl':
        command  => './configure && make rpm',
        path     => '/bin:/sbin:/usr/bin:/usr/sbin',
        cwd      => "/opt/spl-${version}",
        provider => 'shell',
        timeout  => 0,
        creates  => "/opt/spl-${version}/spl-${version}.x86_64.rpm",
        require  => Exec['unzip spl'],
    }
    exec { 'install spl':
        command  => 'yum install -y *.x86_64.rpm',
        path     => '/bin:/sbin:/usr/bin:/usr/sbin',
        cwd      => "/opt/spl-${version}",
        unless   => 'yum list installed spl',
        require  => Exec['build spl'],
    }
    exec { 'get zfs':
        command => "wget -O /opt/zfs-${version}.tar.gz ${baseurl}/zfs/zfs-${version}.tar.gz",
        path    => '/bin:/sbin:/usr/bin:/usr/sbin',
        creates => "/opt/zfs-${version}.tar.gz",
        require => Exec['install spl'],
    }
    exec { 'unzip zfs':
        command => "tar -xvzf /opt/zfs-${version}.tar.gz -C /opt",
        path    => '/bin:/sbin:/usr/bin:/usr/sbin',
        creates => "/opt/zfs-${version}",
        require => Exec['get zfs'],
    }
    exec { 'build zfs':
        command  => './configure && make rpm',
        path     => '/bin:/sbin:/usr/bin:/usr/sbin',
        cwd      => "/opt/zfs-${version}",
        provider => 'shell',
        timeout  => 0,
        creates  => "/opt/zfs-${version}/zfs-${version}.x86_64.rpm",
        require  => Exec['unzip zfs'],
    }
    exec { 'install zfs':
        command => 'yum install -y *.x86_64.rpm',
        path    => '/bin:/sbin:/usr/bin:/usr/sbin',
        cwd     => "/opt/zfs-${version}",
        unless  => 'yum list installed zfs',
        require => Exec['build zfs'],
    }
}
