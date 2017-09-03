package com.xml.mypackage

import org.apache.spark._

object Example01 {
    def main(args: Array[String]) {
      val hannah = new Student("Hannah", 25)
      
      hannah.print()
    }
  
}

class Student(name: String, score: Int){
  def print(){
    println(s"$name has score of $score.")
  }
}