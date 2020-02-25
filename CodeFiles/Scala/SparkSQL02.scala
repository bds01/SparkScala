import org.apache.spark.sql.SparkSession
import org.apache.spark._
import org.apache.spark.SparkContext._
import org.apache.log4j._
import org.apache.spark.sql.types._
import com.databricks.spark.avro._
import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.functions._
import org.apache.spark.sql.Row

object SparkSQL02 {
  def main(args: Array[String]) {
    
    Logger.getLogger("org").setLevel(Level.ERROR)

    val sparkSession = SparkSession.builder
      .master("local")
      .appName("spark session example")
      .config("spark.sql.warehouse.dir", "file:///C:/SparkScala/")
      .getOrCreate()

    val df = sparkSession.read.option("header","true").csv("../Files/ADP Impact User List.csv")

    // Display the contents of DataFrame
    df.show()
    
    // This import is needed to use the $-notation
    import sparkSession.implicits._
    
    // Filtering data
    df.select($"User", $"Text", $"UGNM").filter($"UGNM".contains("SALES")).show()
    
    // Group by, Data Conversion
    val df2 = df.select(df("User"), df("Text"), df("Previous Sign-on Date").cast(IntegerType).as("SignDate"), df("UGNM"))
    df2.groupBy("UGNM").sum("SignDate").show()
    
    // Spark SQL
    df.createOrReplaceTempView("ImpactUserList")
    
   // Rank Function     
    val sqlDF = sparkSession.sql("SELECT User, Text, Output, `Previous Sign-on Date`, UGNM, " +
        "RANK() OVER (partition by UGNM ORDER BY `Previous Sign-on Date` ASC) as Rank FROM ImpactUserList WHERE UGNM=\"ACCOUNTING\"")
    sqlDF.show()

  }
  
}
