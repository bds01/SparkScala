package com.nustartech.spark

import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.sql._
import org.apache.log4j._
import scala.xml._

object ParseXML {
  def main(args: Array[String]) {
    
    // Set the log level to only print errors
    Logger.getLogger("org").setLevel(Level.ERROR)
        
    // Create a SparkContext using every core of the local machine, named RatingsCounter
    val sc = new SparkContext("local[*]", "ParseXML")
    
    val sqlContext = new SQLContext(sc)
  }
}