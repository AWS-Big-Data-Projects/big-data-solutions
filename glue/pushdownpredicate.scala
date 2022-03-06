import com.amazonaws.services.glue.DynamicFrame
import com.amazonaws.services.glue.DynamicRecord
import com.amazonaws.services.glue.GlueContext
import com.amazonaws.services.glue.util.JsonOptions
import org.apache.spark.SparkContext
import java.util.Calendar
import java.util.GregorianCalendar
import scala.collection.JavaConversions._

val spark: SparkContext = SparkContext.getOrCreate()
val glueContext: GlueContext = new GlueContext(spark)


val githubEvents: DynamicFrame = glueContext.getCatalogSource(
database = "avro",
tableName = "glue_pd"
).getDynamicFrame()

githubEvents.schema.asFieldList.foreach { field =>
println(s"${field.getName}: ${field.getType.getType.getName}")
}


val partitionPredicate =
    "date_format(to_date(concat(year, '-', month, '-', day)), 'E') in ('Sat', 'Sun')"

val pushdownEvents = glueContext.getCatalogSource(
   database = "avro",
   tableName = "glue_pd",
   pushDownPredicate = partitionPredicate).getDynamicFrame()
