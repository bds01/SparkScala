

object Collections01 {
    def main(args: Array[String]) {
      val x = List(1,2.0,33D, 400L, "Melinda")
     //for(vals <- x) println(vals)
      x.foreach(println)
      println("")
            
      val fruits = Array("apple","banana","orange")
          for (f <- fruits) {
            val s = f.toUpperCase
            println(s)
          }
      println("")
      
      val days = Array("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")
      for ((day, count) <- days.zipWithIndex) {
        println(s"$count is $day")
      }
      
      for (i <- 0 until days.size) println(s"element $i is ${days(i)}")
    }
}