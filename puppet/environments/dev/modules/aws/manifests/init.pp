# Class: aws
#
#
class aws(
    $aws_access_key_id = undef,
    $aws_secret_access_key = undef
) {
    $aws_dir = '/home/vagrant/.aws'

    file { $aws_dir:
        ensure => directory,
    }

    file { "${aws_dir}/credentials":
        ensure  => file,
        content => template('aws/credentials.erb'),
        require => File[$aws_dir],
    }
}
