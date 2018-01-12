import scala.io.Source

object SplitColumns {
       def main(args: Array[String]) { 
  val filename = Source.fromFile("../Files/ADP Impact User List.csv")
  
  for (line <- filename.getLines){
    val cols = line.split(",").map(_.trim)
    
   // Convert to key value pairs 
      println(s"Key->${cols(0)}, value->${cols(1)}")
       } 
  }
}
