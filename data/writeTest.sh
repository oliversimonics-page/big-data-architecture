hdfs dfs -rm -r -f /benchmarks/TestDFSIO
hadoop jar /opt/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-client-jobclient-3.4.2-tests.jar TestDFSIO -write -nrFiles 4 -size 64MB
