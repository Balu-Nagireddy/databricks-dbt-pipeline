import os
from pathlib import Path
from src.pipeline.spark_session import get_spark_session

def run_smoke_test():
    print("Initializing Spark Session for Smoke Test...")
    spark = get_spark_session("SparkSmokeTest")
    
    # We will test reading the olist_customers_dataset.csv
    csv_file = Path("./data/raw/olist_customers_dataset.csv")
    if not csv_file.exists():
        print(f"Error: Target test file {csv_file} does not exist!")
        return False
        
    print(f"Reading test dataset: {csv_file}")
    df = spark.read.csv(str(csv_file), header=True, inferSchema=True)
    
    print("\n--- Spark Read Verification ---")
    print(f"Successfully read: {csv_file}")
    print("Schema:")
    df.printSchema()
    
    row_count = df.count()
    print(f"Row count returned by Spark: {row_count}")
    
    # Let's perform a simple select and show
    df.select("customer_id", "customer_city").show(5, truncate=False)
    
    print("\nSpark session verification COMPLETED successfully!")
    spark.stop()
    return True

if __name__ == "__main__":
    success = run_smoke_test()
    if not success:
        os._exit(1)
