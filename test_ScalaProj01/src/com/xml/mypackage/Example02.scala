package com.xml.mypackage

import org.apache.spark._

object Example02 {
  def main(args: Array[String]) {
  val names = Map("fname" -> "Robert",
                  "lname" -> "Goren")
 
for ((k,v) <- names) println(s"key: $k, value: $v")

  val a = Array("apple", "banana", "grapes", "orange")
  
  a.foreach(println)
  }
  
}