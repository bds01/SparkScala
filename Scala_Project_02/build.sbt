name := "RatingCounter"

version := "1.0"

scalaVersion := "2.11.8"

libraryDependencies += "org.apache.spark" %% "spark-core" % "2.0.0"

libraryDependencies += "org.apache.spark" % "spark-sql_2.11" % "2.0.0" % "provided"

libraryDependencies += "com.databricks" % "spark-xml_2.11" % "0.4.1"