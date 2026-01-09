# TP9: Spark Batch & Streaming Processing with Docker

This project implements a single-node Hadoop/Spark cluster using Docker
to demonstrate three core data processing techniques:

-   **Interactive Processing** (Scala via `spark-shell`)
-   **Batch Processing** (Java application)
-   **Real-Time Streaming** (Structured Streaming)

------------------------------------------------------------------------

## 📋 Prerequisites

-   Docker & Docker Compose installed
-   No local Java/Spark/Hadoop installation required (everything runs
    inside containers)

------------------------------------------------------------------------

## 🚀 Installation & Setup

### 1. Build and Start the Cluster

``` bash
docker compose up -d --build
docker exec -it hadoop-master bash
```

### 2. Initialize Hadoop

``` bash
# Remove buggy pdsh tool
apt-get remove -y pdsh

# Restart SSH
service ssh restart

# Authorize keys
ssh-keyscan localhost >> ~/.ssh/known_hosts
ssh-keyscan hadoop-master >> ~/.ssh/known_hosts
ssh-keyscan 0.0.0.0 >> ~/.ssh/known_hosts

# Set Root Permissions for Hadoop
export HDFS_NAMENODE_USER=root
export HDFS_DATANODE_USER=root
export HDFS_SECONDARYNAMENODE_USER=root
export YARN_RESOURCEMANAGER_USER=root
export YARN_NODEMANAGER_USER=root

# Start the Cluster
/start-hadoop.sh
jps
```

------------------------------------------------------------------------

## 🛠️ Usage Guide

# Phase 1: Interactive Mode (Spark Shell)

### Prepare Data

``` bash
hdfs dfs -rm -r -f file1.count
echo -e "Hello Spark Wordcount
Hello Hadoop Also" > file1.txt
hdfs dfs -mkdir -p /user/root
hdfs dfs -put file1.txt
```

### Run Spark Shell

``` bash
spark-shell
```

``` scala
val lines = sc.textFile("file1.txt")
val wc = lines.flatMap(_.split("\\s+")).map(w => (w, 1)).reduceByKey(_ + _)
wc.saveAsTextFile("hdfs://hadoop-master:9000/user/root/file1.count")
:quit
```

### View Output

``` bash
hdfs dfs -cat file1.count/part-00000
```

------------------------------------------------------------------------

# Phase 2: Batch Processing (Java)

### Prepare Input

``` bash
hdfs dfs -rm -r -f out-spark
hdfs dfs -mkdir -p input
echo -e "2024-01-01\tNY\tShoes\t100" > purchases.txt
hdfs dfs -put purchases.txt input/
```

### Create Java File

``` bash
nano WordCountTask.java
```

``` java
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.*;
import scala.Tuple2;
import java.util.Arrays;

public class WordCountTask {
    public static void main(String[] args) {
        SparkConf conf = new SparkConf().setAppName("WordCountTask");
        JavaSparkContext sc = new JavaSparkContext(conf);

        JavaRDD<String> textFile = sc.textFile(args[0]);
        JavaPairRDD<String, Integer> counts = textFile
            .flatMap(s -> Arrays.asList(s.split("\t")).iterator())
            .mapToPair(word -> new Tuple2<>(word, 1))
            .reduceByKey((a, b) -> a + b);

        counts.saveAsTextFile(args[1]);
        sc.close();
    }
}
```

### Compile & Submit

``` bash
javac -cp "/usr/local/spark/jars/*" WordCountTask.java
jar cf wordcount.jar WordCountTask.class

spark-submit --class WordCountTask --master local wordcount.jar hdfs://hadoop-master:9000/user/root/input/purchases.txt hdfs://hadoop-master:9000/user/root/out-spark 2> /dev/null

hdfs dfs -cat out-spark/part-00000
```

------------------------------------------------------------------------

# Phase 3: Real-Time Streaming

``` bash
nano Stream.java
```

``` java
import org.apache.spark.sql.*;
import org.apache.spark.sql.streaming.*;
import java.util.Arrays;

public class Stream {
    public static void main(String[] args) throws Exception {
        SparkSession spark = SparkSession.builder()
            .appName("NetworkWordCount")
            .master("local[*]")
            .getOrCreate();

        Dataset<Row> lines = spark.readStream()
            .format("socket")
            .option("host", "localhost")
            .option("port", 9999)
            .load();

        Dataset<String> words = lines.as(Encoders.STRING())
            .flatMap(x -> Arrays.asList(x.split(" ")).iterator(), Encoders.STRING());

        Dataset<Row> wordCounts = words.groupBy("value").count();

        StreamingQuery query = wordCounts.writeStream()
            .outputMode("complete")
            .format("console")
            .trigger(Trigger.ProcessingTime("1 second"))
            .start();

        query.awaitTermination();
    }
}
```

``` bash
javac -cp "/usr/local/spark/jars/*" Stream.java
jar cf stream.jar Stream.class
```

### Run Streaming

Terminal 1:

``` bash
docker exec -it hadoop-master bash
nc -lk 9999
```

Terminal 2:

``` bash
spark-submit --class Stream --master local stream.jar
```

------------------------------------------------------------------------

## 🔧 Troubleshooting

| Error | Solution |
| :--- | :--- |
| **FileAlreadyExistsException** | Delete folder: `hdfs dfs -rm -r <dir>` |
| **Hadoop won't start** | Run `apt-get remove pdsh` then `service ssh start` |
| **NameNode issue** | Re-run `/start-hadoop.sh` |
| **Output not in HDFS** | Run `export HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop` |