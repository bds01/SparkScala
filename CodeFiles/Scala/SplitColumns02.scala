

object SplitColumns02 {
  def main(args: Array[String]) {
    println("User,Text,Previous Sign-on Date,Output,CLIENT,TAUT,UGNM")
    val bufferedSource = io.Source.fromFile("../Files/ADP Impact User List.csv")
    
    for (line <- bufferedSource.getLines) {
    
      val cols = line.split(",").map(_.trim)
      
      //Convert to pipe separated
       println(s"${cols(0)}|${cols(1)}|${cols(2)}|${cols(3)}")
}
           
         }
}
