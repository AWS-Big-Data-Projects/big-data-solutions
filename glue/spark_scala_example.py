import com.amazonaws.services.glue.ChoiceOption
import com.amazonaws.services.glue.GlueContext
import com.amazonaws.services.glue.MappingSpec
import com.amazonaws.services.glue.ResolveSpec
import com.amazonaws.services.glue.errors.CallSite
import com.amazonaws.services.glue.util.GlueArgParser
import com.amazonaws.services.glue.util.Job
import com.amazonaws.services.glue.util.JsonOptions
import org.apache.spark.SparkContext
import scala.collection.JavaConverters._

object GlueApp {
  val argNames = Seq("JOB_NAME", "PRIMARY_DESTINATION_WRITER_TYPE", "PRIMARY_DESTINATION_LOADER_TYPE","PRIMARY_DESTINATION","PRIMARY_DESTINATION_PARTITION","STAGE","NAMESPACE","ID_NAMESPACE_MAP","PRIMARY_SOURCE_PERIOD","PRIMARY_SOURCE_READER_TYPE","AddUuid1_TRANSFORMER","PRIMARY_SOURCE_PARTITION","STAGING_S3_FOLDER","SelectEventNamePartition_TRANSFORMER","AWS_REGION","PRIMARY_SOURCE_IGNORE_BOOKMARKING","ALIAS_TRANSLATION_LAMBDA")

  

  def main(sysArgs: Array[String]) {
    val spark: SparkContext = new SparkContext()
    val glueContext: GlueContext = new GlueContext(spark)

    val args = GlueArgParser.getResolvedOptions(sysArgs, argNames.toArray)
    Job.init(args("JOB_NAME"), glueContext, args.asJava)

    val prm_dest_wrt_type = args("PRIMARY_DESTINATION_WRITER_TYPE")
    val prm_dest_load_type = args("PRIMARY_DESTINATION_LOADER_TYPE")
    val prm_dest = args("PRIMARY_DESTINATION")
    val prm_dest_part = args("PRIMARY_DESTINATION_PARTITION")
    val stg = args("STAGE")
    val nmspc = args("NAMESPACE")
    val id_nmspc_map = args("ID_NAMESPACE_MAP")
    val prm_src_prd = args("PRIMARY_SOURCE_PERIOD")
    val prm_src_rdr_type = args("PRIMARY_SOURCE_READER_TYPE")
    val add_txf = args("AddUuid1_TRANSFORMER")
    val prm_src_prt = args("PRIMARY_SOURCE_PARTITION")
    val stg_s3_fldr = args("STAGING_S3_FOLDER")
    val slct_nm_part = args("SelectEventNamePartition_TRANSFORMER")
    val aws_rgn = args("AWS_REGION")
    val prm_src_ig_bm = args("PRIMARY_SOURCE_IGNORE_BOOKMARKING")
    val alias = args("ALIAS_TRANSLATION_LAMBDA")
    
    
    println("PRIMARY_DESTINATION_WRITER_TYPE = " + prm_dest_wrt_type);
    println("PRIMARY_DESTINATION_LOADER_TYPE = " + prm_dest_load_type);
    println("PRIMARY_DESTINATION = " + prm_dest);
    println("PRIMARY_DESTINATION_PARTITION = " + prm_dest_part);
    println("STAGE = " + stg);
    println("NAMESPACE = " + nmspc);
    println("ID_NAMESPACE_MAP = " + id_nmspc_map);
    println("PRIMARY_SOURCE_PERIOD = " + prm_src_prd);
    println("PRIMARY_SOURCE_READER_TYPE = " + prm_src_rdr_type);
    println("AddUuid1_TRANSFORMER = " + add_txf);
    println("PRIMARY_SOURCE_PARTITION = " + prm_src_prt);
    println("STAGING_S3_FOLDER = " + stg_s3_fldr);
    println("SelectEventNamePartition_TRANSFORMER = " + slct_nm_part);
    println("AWS_REGION = " + aws_rgn);
    println("PRIMARY_SOURCE_IGNORE_BOOKMARKING = " + prm_src_ig_bm);
    println("ALIAS_TRANSLATION_LAMBDA = " + alias);
    
  }
}
