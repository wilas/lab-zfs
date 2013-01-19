stage { "base": before => Stage["main"] }
stage { "last": require => Stage["main"] }

# basic config
class { "install_repos": stage => "base" }
class { "basic_package": stage => "base" }
class { "user::root": stage    => "base"}

# /etc/hosts
host { "zetta.farm":
    ip           => "77.77.77.99",
    host_aliases => "zetta",
}
host { "zepto.farm":
    ip           => "77.77.77.98",
    host_aliases => "zepto",
}

# firewall manage
service { "iptables":
    ensure => running,
    enable => true,
}
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
class { "basic_firewall": }

# Install ZFS
class { "zfsonlinux": 
    version => "0.6.0-rc12",
}
