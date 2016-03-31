SG DevOps Task
--------------

> Publish a sample on github that lets me install a simple django app (on ElasticBeanstalk if you know how) without RDS on AWS using an ELB

Installation
------------
* Install fabric `pip install fabric`
* Setup your virtualenv `fab install`

Initial Deployment
----------
First, initialize the app `fab eb_init:app_name`
Next, create the environment to begin deployment `fab eb_create_env`

Deployments
-----------
Run `fab eb_deploy` to deploy to the active environment

Extras
------
`fab eb_list` to show all Elastic Beanstalk environments
`fab eb_terminate:<name>` to terminate an environment
`fab eb_scale:<number>,name=<name>` to change the number of instances


TODO
----
* Add healthcheck endpoint
* Specify config for EB
