#!/bin/bash
set -e
ROLE="$1"
if [ "$ROLE" = "namenode" ]; then
  if [ ! -f /opt/hadoop/dfs/name/current/VERSION ]; then
    hdfs namenode -format -force -nonInteractive
  fi
  exec hdfs namenode
elif [ "$ROLE" = "datanode" ]; then
  exec hdfs datanode
else
  echo "Usage: start-hadoop.sh namenode|datanode"
  exit 1
fi
