cd /home/duan/github/schemaindex/schemaindex/spec/hdfsindex/java/src/com/schemaindex

javac -cp .:../../../lib/* HdfsINotify2Restful.java
java -cp .:../../../lib/*  HdfsINotify2Restful  http://localhost:8088 hdfs1 hdfs://localhost:9000


# javac -cp .:/home/duan/github/inotify/hdfs-inotify-example-master/src/main/java/com/onefoursix/httpcomponents-client-4.5.4/lib/*:/home/duan/java/jdk1.8.0_151/lib/*:/usr/local/hadoop/share/hadoop/hdfs/hadoop-hdfs-2.6.5.jar:/usr/local/hadoop/share/hadoop/common/hadoop-common-2.6.5.jar:/usr/local/hadoop/share/hadoop/common/lib/commons-logging-1.1.3.jar:/usr/local/hadoop/share/hadoop/hdfs/lib/guava-11.0.2.jar:/usr/local/hadoop/share/hadoop/common/lib/commons-collections-3.2.2.jar:/usr/local/hadoop/share/hadoop/common/lib/* HdfsINotify2Restful.java
#java -cp .:/home/duan/github/inotify/hdfs-inotify-example-master/src/main/java/com/onefoursix/httpcomponents-client-4.5.4/lib/*:/home/duan/java/jdk1.8.0_151/lib/*:/usr/local/hadoop/share/hadoop/hdfs/hadoop-hdfs-2.6.5.jar:/usr/local/hadoop/share/hadoop/common/hadoop-common-2.6.5.jar:/usr/local/hadoop/share/hadoop/common/lib/commons-logging-1.1.3.jar:/usr/local/hadoop/share/hadoop/hdfs/lib/guava-11.0.2.jar:/usr/local/hadoop/share/hadoop/common/lib/commons-collections-3.2.2.jar:/usr/local/hadoop/share/hadoop/common/lib/* HdfsINotify2Restful  http://localhost:8088 hdfs1 hdfs://localhost:9000

