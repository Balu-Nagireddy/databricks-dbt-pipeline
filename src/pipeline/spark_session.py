import os
import sys
import urllib.request
from pathlib import Path
from pyspark.sql import SparkSession
from dotenv import load_dotenv

# Load env variables
load_dotenv()

def ensure_winutils():
    """
    Downloads winutils.exe and hadoop.dll for Hadoop 3.3.4 if on Windows,
    and configures the local HADOOP_HOME environment variable.
    """
    if os.name != 'nt':
        return  # Only needed for Windows

    # We will place hadoop binaries inside a local 'hadoop' directory in the project
    project_root = Path(__file__).resolve().parents[2]
    hadoop_dir = project_root / "hadoop"
    bin_dir = hadoop_dir / "bin"
    
    winutils_path = bin_dir / "winutils.exe"
    hadoop_dll_path = bin_dir / "hadoop.dll"

    if not winutils_path.exists() or not hadoop_dll_path.exists():
        bin_dir.mkdir(parents=True, exist_ok=True)
        print("Downloading Hadoop Windows binaries (winutils.exe & hadoop.dll) for Hadoop 3.3.5...")
        
        base_url = "https://github.com/cdarlint/winutils/raw/master/hadoop-3.3.5/bin"
        
        try:
            # Download winutils.exe
            urllib.request.urlretrieve(f"{base_url}/winutils.exe", str(winutils_path))
            print("Downloaded winutils.exe successfully.")
            
            # Download hadoop.dll
            urllib.request.urlretrieve(f"{base_url}/hadoop.dll", str(hadoop_dll_path))
            print("Downloaded hadoop.dll successfully.")
        except Exception as e:
            print(f"Warning: Failed to download Hadoop binaries: {e}")
            print("Spark might encounter issues writing local Parquet files.")

    # Configure environment variables
    hadoop_home_str = str(hadoop_dir.absolute())
    os.environ["HADOOP_HOME"] = hadoop_home_str
    
    # Append bin directory to system PATH for current process
    bin_path_str = str(bin_dir.absolute())
    if bin_path_str not in os.environ.get("PATH", ""):
        os.environ["PATH"] = f"{bin_path_str}{os.path.pathsep}{os.environ['PATH']}"

def get_spark_session(app_name: str = None) -> SparkSession:
    """
    Creates or gets a PySpark session configured for the project,
    ensuring Java 21 and Windows compatibility settings are applied.
    """
    # Set up HADOOP_HOME and download binaries if running on Windows
    ensure_winutils()

    env_app_name = app_name or os.getenv("SPARK_APP_NAME", "DataEngineeringPipeline")
    master = os.getenv("SPARK_MASTER", "local[*]")
    
    # JVM options required for Java 17+ and Java 21 to run Spark properly
    # (prevents illegal reflective access exceptions from breaking Spark serialization/memory)
    jvm_opts = (
        "--add-opens=java.base/java.lang=ALL-UNNAMED "
        "--add-opens=java.base/java.lang.invoke=ALL-UNNAMED "
        "--add-opens=java.base/java.lang.reflect=ALL-UNNAMED "
        "--add-opens=java.base/io.netty=ALL-UNNAMED "
        "--add-opens=java.base/java.io=ALL-UNNAMED "
        "--add-opens=java.base/java.net=ALL-UNNAMED "
        "--add-opens=java.base/java.nio=ALL-UNNAMED "
        "--add-opens=java.base/java.util=ALL-UNNAMED "
        "--add-opens=java.base/java.util.concurrent=ALL-UNNAMED "
        "--add-opens=java.base/java.util.concurrent.atomic=ALL-UNNAMED "
        "--add-opens=java.base/sun.nio.ch=ALL-UNNAMED "
        "--add-opens=java.base/sun.nio.cs=ALL-UNNAMED "
        "--add-opens=java.base/sun.security.action=ALL-UNNAMED "
        "--add-opens=java.base/sun.util.locale.provider=ALL-UNNAMED "
        "--add-opens=java.base/util=ALL-UNNAMED"
    )
    
    # Apply to python subprocess environment before JVM boots
    os.environ["JDK_JAVA_OPTIONS"] = jvm_opts
    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

    builder = SparkSession.builder \
        .appName(env_app_name) \
        .master(master) \
        .config("spark.driver.extraJavaOptions", jvm_opts) \
        .config("spark.executor.extraJavaOptions", jvm_opts) \
        .config("spark.sql.shuffle.partitions", "4") \
        .config("spark.sql.warehouse.dir", "./data/warehouse") \
        .config("spark.hadoop.fs.file.impl", "org.apache.hadoop.fs.RawLocalFileSystem") \
        .config("spark.sql.autoBroadcastJoinThreshold", "-1")

    # If JDBC URL is available, we could configure driver paths here if required
    # db_url = os.getenv("DATABASE_URL")
    
    spark = builder.getOrCreate()
    return spark
