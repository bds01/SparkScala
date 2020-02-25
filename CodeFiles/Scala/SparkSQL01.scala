import org.apache.spark.sql.SparkSession
import org.apache.spark._
import org.apache.spark.SparkContext._
import org.apache.log4j._

object SparkSQL01 {
  def main(args: Array[String]) {
    
    Logger.getLogger("org").setLevel(Level.ERROR)

    val sparkSession = SparkSession.builder
      .master("local")
      .appName("spark session example")
      .config("spark.sql.warehouse.dir", "file:///C:/SparkScala/")
      .getOrCreate()

    val df = sparkSession.read.option("header","true").csv("../Files/Leads_072115.csv")

    df.show()

  }
  
}
