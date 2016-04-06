SG DevOps Task
--------------

> Publish a sample on github that lets me install a simple django app
> (on ElasticBeanstalk if you know how) without RDS on AWS using an ELB

Prerequisites
-------------
* Vagrant (tested with 1.8.1)
* VirtualBox (tested with 4.3)

Installation
------------
* Clone the repo `git clone <URL>`
* cd to the repo `cd ebsample`
* Run `vagrant up` ... get some coffee
* SSH to VM `vagrant ssh`
* Setup your virtualenv `cd /vagrant && fab install`

Deployment
-----------
Create a file with your AWS credentials at
`puppet/environments/dev/hieradata/gitignore.yaml`

```
---
aws::aws_access_key_id: "ACCESS_KEY"
aws::aws_secret_access_key: "SECRET_KEY"
```

Run `fab <dev|prod> deploy` to deploy to the specified environment

Extras
------
* `fab <environment> health` to show Elastic Beanstalk health
* `fab <dev|prod> terminate` to terminate an environment
* `fab <environment> config` to modify the environment config
* `fab eb_list` to show all Elastic Beanstalk environments

TODO
----
* Blue/green deployment strategy
