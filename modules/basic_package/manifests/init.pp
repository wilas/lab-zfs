
class basic_package {

    package { [ "wget",
                "mc",
                "vim-common",
                "git",
                "iptables",
                "rubygems"
        ]:
        ensure => installed,
    }

    # package help create vagrant box
    package { [ "make",
                 "gcc",
                 "kernel-devel",
                 "curl",
                 "bzip2"
        ]:
        ensure => installed,
    }

    # https://github.com/rodjek/puppet-lint
    # puppet-lint <path to file>
    # or you can add: require 'puppet-lint/tasks/puppet-lint' to your Rakefile
    # and then run: rake lint
    package { "puppet-lint":
        ensure   => installed,
        provider => "gem",
        require  => Package["rubygems"],
    }

}
