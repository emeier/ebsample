stage { 'pre': }

Stage['pre'] -> Stage['main']

class epel {
    package { 'ca-certificates':
        ensure => 'latest',
    }

    package { 'epel-release':
        ensure  => installed,
        require => Package['ca-certificates'],
    }
}

class { 'epel':
    stage => pre,
}

class defaultnode {
    service { 'iptables':
        enable => false,
        ensure => 'stopped'
    }

    file { '/etc/localtime':
       ensure => 'link',
       target => '/usr/share/zoneinfo/America/Chicago',
    }
}

include defaultnode
include python
include git
include aws
