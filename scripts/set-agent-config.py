#!/usr/bin/python

## *******************************************************************************************
## set-agent-config.py 
## 
## Example of how to set the Flume Configuration file for a Flume Agent using the Cloudera Manager API
## 
## Usage: set-agent-config.py <agent-id> <config-file>
##
##        for example:  set-agent-config.py agent1 agent1.conf
## 
##        (the rest of the values are set in the script below)
## 
## *******************************************************************************************

## ** imports *******************************

import sys
from cm_api.api_client import ApiResource



## ** Settings ******************************

## Cloudera Manager Host
cm_host = "brooklyn.onefoursix.com"
cm_port = "7180"

## Cloudera Manager login with at least Configurator role
cm_login = "configurator"

## Cloudera Manager password
cm_password = "configurator_password"

## Cluster Name
cluster_name = "Cluster 1"

## Name of Flume Service
flume_service_name = "Flume"

## CM API Version 
## See the chart here to get the right value: http://cloudera.github.io/cm_api/docs/releases/
## I'll default to v10 of the API for Cloudera Manager 5.4
cm_api_version = "10"

## ******************************************


if len(sys.argv) != 3:
  print "Error: Wrong number of arguments"
  print "Usage: set-agent-config.py <agent-id> <config-file>"
  print "Example: set-agent-config.py agent1 flume.conf"
  quit(1)

agent_ref = sys.argv[1]

config_file =  sys.argv[2]

print "Setting config file '" + config_file + "' for Agent '" + agent_ref + "' for Flume Service '" + flume_service_name + "' on cluster '" + cluster_name + "'..."

## load the flume.conf file
f = open(config_file,'r')
flume_conf = ""
while 1:
    line = f.readline()
    if not line:break
    flume_conf += line
f.close()

## Get the CM api
api = ApiResource(server_host=cm_host, server_port=cm_port, username=cm_login, password=cm_password, version=cm_api_version)

## Get the cluster
cluster = api.get_cluster(cluster_name)

## Get the Flume Service
flume_service = cluster.get_service(flume_service_name)

## Get the Agent
role = flume_service.get_role(agent_ref)

## Set the flume.conf in the config
role.update_config({"agent_config_file" : flume_conf})

print "New configuration set!"
