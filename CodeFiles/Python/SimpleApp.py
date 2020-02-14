"""SimpleApp.py"""
from pyspark.sql import SparkSession

logFile = "hdfs://sandbox-hdp.hortonworks.com:8020/user/spark/contents.txt"  # Should be some file on your system
spark = SparkSession.builder.appName("SimpleApp").getOrCreate()
logData = spark.read.text(logFile).cache()

numAs = logData.filter(logData.value.contains('a')).count()
numBs = logData.filter(logData.value.contains('b')).count()

print("Lines with a: %i, lines with b: %i" % (numAs, numBs))

spark.stop()

# Run the program
# spark-submit --master local[4] SimpleApp.py
