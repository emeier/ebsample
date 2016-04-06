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
    service { 'firewalld':
        enable      => false,
        ensure      => stopped,
    }
}

node default {
    include defaultnode
    include python
    include git
    include aws
    include vim
}
