FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# 1. Install Java 8 and utilities (Matches Lab Requirement)
RUN apt-get update && \
    apt-get install -y openjdk-8-jdk wget ssh pdsh netcat nano && \
    apt-get clean

# 2. Set Environment Variables
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV HADOOP_VERSION=3.3.6
ENV SPARK_VERSION=3.5.0
ENV HADOOP_HOME=/usr/local/hadoop
ENV SPARK_HOME=/usr/local/spark
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$SPARK_HOME/bin

# 3. Install Hadoop
RUN wget https://archive.apache.org/dist/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz && \
    tar -xvf hadoop-$HADOOP_VERSION.tar.gz && \
    mv hadoop-$HADOOP_VERSION /usr/local/hadoop && \
    rm hadoop-$HADOOP_VERSION.tar.gz

# 4. Install Spark
RUN wget https://archive.apache.org/dist/spark/spark-$SPARK_VERSION/spark-$SPARK_VERSION-bin-hadoop3.tgz && \
    tar -xvf spark-$SPARK_VERSION-bin-hadoop3.tgz && \
    mv spark-$SPARK_VERSION-bin-hadoop3 /usr/local/spark && \
    rm spark-$SPARK_VERSION-bin-hadoop3.tgz

# 5. Configure SSH (Passwordless for Hadoop)
RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
    chmod 0600 ~/.ssh/authorized_keys

# 6. Basic Hadoop Config (Core & HDFS)
RUN echo "export JAVA_HOME=$JAVA_HOME" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh
RUN echo '<configuration><property><name>fs.defaultFS</name><value>hdfs://hadoop-master:9000</value></property></configuration>' > $HADOOP_HOME/etc/hadoop/core-site.xml
RUN echo '<configuration><property><name>dfs.replication</name><value>1</value></property></configuration>' > $HADOOP_HOME/etc/hadoop/hdfs-site.xml

# 7. Add the Start Script (matches your Lab's command)
COPY start-hadoop.sh /start-hadoop.sh
RUN chmod +x /start-hadoop.sh

WORKDIR /root
CMD ["/bin/bash", "-c", "service ssh start; tail -f /dev/null"]