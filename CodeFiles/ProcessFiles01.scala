import scala.io.Source

object ProcessFiles01 {
   def main(args: Array[String]) {
      
    val filename = "../Files/ADP Impact User List.csv"
    for (line <- Source.fromFile(filename).getLines.toArray) {
      println(line)
    }
  }
}