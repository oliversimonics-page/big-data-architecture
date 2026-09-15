hdfs dfs -rm -r -f /data/results/temperature
time hadoop jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.4.2.jar \
    -input /data/raw/sensors/sensors100.json \
    -output /data/results/temperature \
    -mapper /course-data/mapper.py \
    -reducer /course-data/reducer.py