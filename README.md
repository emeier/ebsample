SG DevOps Task
--------------

> Publish a sample on github that lets me install a simple django app (on ElasticBeanstalk if you know how) without RDS on AWS using an ELB

Installation
------------
* Install fabric `pip install fabric`
* Setup your virtualenv `fab install`

Deployment
-----------
Run `fab <dev|prod> deploy` to deploy to the specified environment

Extras
------
`fab eb_list` to show all Elastic Beanstalk environments
`fab eb_terminate:<name>` to terminate an environment
`fab eb_scale:<number>,name=<name>` to change the number of instances


TODO
----
* Specify config for EB env on creation
* Blue/green deployment
