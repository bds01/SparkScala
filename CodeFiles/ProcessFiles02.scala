import scala.io.Source

object ProcessFiles02 {
     def main(args: Array[String]) {
  
  val NEWLINE = 10
  var newlineCount = 0L     
  val filename = "../Files/ADP Impact User List.csv"

  for (line <- Source.fromFile(filename).getLines) {
    println(line)
    newlineCount += 1
  }
  
  //Print the number of lines in the file
  println(s"The number of lines are ${newlineCount -1}")
     }
  
}