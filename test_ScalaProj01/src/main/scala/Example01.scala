
import scala.io.Source

// Read the data from the text file
object Example01 {
    def main(args: Array[String]) {
      
    val filename = "../test_ScalaProj01/target/files/spam.data"
    for (line <- Source.fromFile(filename).getLines.toArray) {
      println(line)
    }
  }
}
