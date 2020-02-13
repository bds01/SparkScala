# Second example of wordcount to print the results to console

import sys
 
from pyspark import SparkContext, SparkConf
 
if __name__ == "__main__":
	
	# create Spark context with necessary configuration
	sc = SparkContext("local","PySpark Word Count Exmaple")
	
	# read data from text file and split each line into words
	words = sc.textFile("hdfs://sandbox-hdp.hortonworks.com:8020/user/spark/contents.txt").flatMap(lambda line: line.split(" "))
	
	# count the occurrence of each word
	wordCounts = words.map(lambda word: (word, 1)).reduceByKey(lambda a,b:a +b)
	
	#Collect and print the output
	output = wordCounts.collect()
	
	for (word, count) in output: print("%s: %i" % (word, count))

        spark.stop()
