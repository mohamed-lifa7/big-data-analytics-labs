#!/bin/bash
# Initialize HDFS if not already done
if [ ! -d "/tmp/hadoop-root/dfs/name" ]; then
    echo "Formatting NameNode..."
    $HADOOP_HOME/bin/hdfs namenode -format
fi

# Start Hadoop Daemons
echo "Starting HDFS..."
$HADOOP_HOME/sbin/start-dfs.sh
echo "Starting YARN..."
$HADOOP_HOME/sbin/start-yarn.sh

echo "Hadoop & Spark environment is ready!"