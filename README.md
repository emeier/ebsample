Elastic Beanstalk Sample Deployment
--------------

This is a sample project to deploy a Django app to Amazon Elastic Beanstalk using [Fabric](http://www.fabfile.org/) and the [Elastic Beanstalk CLI](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3.html)

[Vagrant](https://www.vagrantup.com/) and [Puppet](https://puppetlabs.com/) ensure we can create a reproducible and portable environment.

Prerequisites
-------------
* Vagrant (tested with 1.8.1)
* VirtualBox (tested with 4.3)

Installation
------------
* Clone the repo `git clone https://github.com/emeier/ebsample.git`
* Create a file with your AWS credentials at
`puppet/environments/dev/hieradata/gitignore.yaml`

```
---
aws::aws_access_key_id: "ACCESS_KEY"
aws::aws_secret_access_key: "SECRET_KEY"
```

* Run `cd ebsample && vagrant up` ... get some coffee
* SSH to VM `vagrant ssh`
* Setup your virtualenv `cd /vagrant && fab install`

Deployment
----------
* `vagrant ssh`
* `cd /vagrant`
* Run `fab <environment> deploy` to deploy to the specified environment

Environments
------------
* `dev` is configured to deploy 1 `t2.micro` instance
* `prod` is configured to deploy 2 `m4.large` instances

Extras
------
* `fab <environment> health` to show Elastic Beanstalk health
* `fab <environment> terminate` to terminate an environment
* `fab <environment> config` to modify the environment config
* `fab eb_list` to show all Elastic Beanstalk environments

TODO
----
* Blue/green deployment strategy
