import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.sql._
import org.apache.log4j._
import scala.xml._
import com.databricks.spark.xml

object xmlParse {
  def main(args: Array[String]) {
    val df = Seq(("one", 1), ("one", 1), ("two", 1)).toDF("word", "count")
    df.show()      
    }
  }