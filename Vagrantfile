Vagrant.require_version ">=1.8"

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "puppetlabs/centos-7.2-64-puppet"
  config.vm.box_version = "1.0.1"
  config.vm.hostname = "sgdevops"


  config.vm.network "private_network", ip: "10.10.10.10"

  config.ssh.forward_agent = true

  config.vm.provider :virtualbox do |vb|
    vb.gui = false
    vb.memory = 1024
    vb.cpus = 1

    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    vb.customize ["modifyvm", :id, "--natdnspassdomain1", "off"]
  end

  config.vm.provision "puppet" do |puppet|
    puppet.environment_path = "puppet/environments"
    puppet.environment = "dev"
    puppet.hiera_config_path = "puppet/hiera.yaml"
    puppet.working_directory = "/tmp/vagrant-puppet"
    puppet.options = "--verbose"
  end
end
