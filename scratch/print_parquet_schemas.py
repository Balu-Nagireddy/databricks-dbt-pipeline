import glob
import pandas as pd
from pathlib import Path

def print_schemas():
    gold_dir = Path("data/gold")
    parquet_files = glob.glob(str(gold_dir / "**/*.parquet"), recursive=True)
    
    # Group by the dataset name (parent directory of the parquet file)
    datasets = {}
    for p in parquet_files:
        p_path = Path(p)
        # Find the parent folder that contains the partition/parquet files
        # e.g. data/gold/sales/daily_sales/part-...
        # The dataset name is daily_sales
        dataset_name = p_path.parent.name
        # If it is partitioned (e.g. year=2018), get one level higher
        if "=" in dataset_name:
            dataset_name = p_path.parent.parent.name
        if dataset_name not in datasets:
            datasets[dataset_name] = p_path
            
    for name, path in datasets.items():
        try:
            df = pd.read_parquet(path)
            print(f"Dataset: {name}")
            print(f"Columns: {list(df.columns)}")
            print("-" * 50)
        except Exception as e:
            print(f"Failed to read {name}: {e}")

if __name__ == "__main__":
    print_schemas()
