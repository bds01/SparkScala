package com.xml.mypackage

import org.apache.spark._
import org.apache.spark.rdd._
import org.apache.spark.SparkConf
import org.apache.spark.SparkContext._
import org.apache.log4j._

object spamfile {
    def main(args: Array[String]) {
   
    // Set the log level to only print errors
    Logger.getLogger("org").setLevel(Level.ERROR)
       
        
    // Create a SparkContext using every core of the local machine, named RatingsCounter
    val sc = new SparkContext("local[*]", "TextFile")
    
    val inFile = sc.textFile("../test_ScalaProj01/target/files/wordfile.txt")
    
    val nums = inFile.flatMap(line => line.split(" ")).map(word => (word,1)).reduceByKey(_ + _)
    nums.foreach(println)
    
    }
  
}