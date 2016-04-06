class python {
    package { 'python-devel':
        ensure  => installed,
    }

    package { 'python-pip':
        ensure  => installed,
        require => Package['python-devel']
    }

    package { 'python-virtualenv':
        ensure  => installed,
        require => Package['python-devel']
    }

    package { 'Fabric':
        ensure   => installed,
        provider => pip,
        require  => Package['python-devel'],
    }
}
