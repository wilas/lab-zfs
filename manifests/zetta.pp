# Node global
exec { 'clear-firewall':
    command     => '/sbin/iptables -F',
    refreshonly => true,
}
exec { 'persist-firewall':
    command     => '/sbin/iptables-save >/etc/sysconfig/iptables',
    refreshonly => true,
}
Firewall {
    subscribe => Exec['clear-firewall'],
    notify    => Exec['persist-firewall'],
}

# Include classes - search for classes in *.yaml/*.json files
hiera_include('classes')

# Classes order
Class['yum_repos'] -> Class['basic_package'] -> Class['user::root']
Class['basic_package'] -> Class['zfsonlinux']

# In real world from DNS
host { 'zetta.farm':
    ip           => '77.77.77.99',
    host_aliases => 'zetta',
}
host { 'zepto.farm':
    ip           => '77.77.77.98',
    host_aliases => 'zepto',
}

# Extra to play more with zfs (use py-zfswrapper)
package { 'python-setuptools':
    ensure => installed,
}
exec { 'install py-zfswrapper':
    command => 'python setup.py install && touch /opt/py-zfswrapper.files',
    path    => '/bin:/sbin:/usr/bin:/usr/sbin',
    cwd     => '/vagrant/tools/py-zfswrapper',
    creates => '/opt/py-zfswrapper.files',
    require => Package['python-setuptools'],
}

