import os
import shutil
import glob
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import kagglehub

# Load environment variables
load_dotenv()

class ColumnProfile(BaseModel):
    name: str
    missing_count: int
    missing_percentage: float

class FileProfile(BaseModel):
    filename: str
    encoding: str
    row_count: int
    column_count: int
    columns: List[str]
    columns_detail: List[ColumnProfile]

class DatasetProfiler:
    """
    Profiles a dataset to ensure quality validation.
    """
    def __init__(self, raw_dir: Path):
        self.raw_dir = raw_dir

    def get_csv_files(self) -> List[Path]:
        return list(self.raw_dir.glob("*.csv"))

    def profile_file(self, file_path: Path) -> FileProfile:
        # Determine encoding: typical Olist files are UTF-8 or Latin-1
        encoding = 'utf-8'
        try:
            df = pd.read_csv(file_path, encoding='utf-8', nrows=5)
            # Try to read full file with utf-8 to be sure
            df = pd.read_csv(file_path, encoding='utf-8')
        except UnicodeDecodeError:
            encoding = 'latin-1'
            df = pd.read_csv(file_path, encoding='latin-1')

        row_count = len(df)
        column_count = len(df.columns)
        columns = list(df.columns)
        
        columns_detail = []
        null_counts = df.isnull().sum().to_dict()
        for col in columns:
            missing = null_counts.get(col, 0)
            missing_pct = (missing / row_count * 100) if row_count > 0 else 0.0
            columns_detail.append(
                ColumnProfile(
                    name=col,
                    missing_count=missing,
                    missing_percentage=round(missing_pct, 2)
                )
            )

        return FileProfile(
            filename=file_path.name,
            encoding=encoding,
            row_count=row_count,
            column_count=column_count,
            columns=columns,
            columns_detail=columns_detail
        )

    def profile_all(self) -> List[FileProfile]:
        csv_files = self.get_csv_files()
        profiles = []
        for f in csv_files:
            print(f"Profiling: {f.name}...")
            profiles.append(self.profile_file(f))
        return profiles

class DatasetDownloader:
    """
    Acquires dataset via kagglehub and saves it to local raw storage.
    """
    def __init__(self, dataset_name: str, target_dir: Path):
        self.dataset_name = dataset_name
        self.target_dir = target_dir

    def download(self) -> List[Path]:
        print(f"Acquiring dataset '{self.dataset_name}' from Kaggle...")
        download_dir = kagglehub.dataset_download(self.dataset_name)
        download_path = Path(download_dir)
        print(f"Acquired dataset cached at: {download_path}")

        # Ensure target directory exists
        self.target_dir.mkdir(parents=True, exist_ok=True)

        downloaded_csvs = list(download_path.glob("*.csv"))
        copied_files = []
        for csv_file in downloaded_csvs:
            dest = self.target_dir / csv_file.name
            shutil.copy2(csv_file, dest)
            copied_files.append(dest)
            print(f"Copied dataset file: {csv_file.name} -> {dest}")

        return copied_files

def generate_profiling_report(profiles: List[FileProfile], output_path: Path):
    """
    Generates a markdown documentation report of dataset validation.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    md = [
        "# Data Profiling Report",
        "",
        "This report contains metadata, structural definitions, validation metrics, and data quality metrics of the acquired dataset.",
        "",
        "## Dataset Details",
        f"- **Dataset ID**: `{os.getenv('KAGGLE_DATASET', 'olistbr/brazilian-ecommerce')}`",
        "- **Acquisition Method**: `kagglehub`",
        "",
        "## File Validation Summary",
        "| File Name | Encoding | Rows | Columns |",
        "| :--- | :--- | :--- | :--- |"
    ]
    
    for p in profiles:
        md.append(f"| {p.filename} | {p.encoding} | {p.row_count:,} | {p.column_count} |")
        
    md.append("")
    md.append("## Column & Data Quality Details")
    
    for p in profiles:
        md.append(f"### {p.filename}")
        md.append(f"- **Encoding**: {p.encoding}")
        md.append(f"- **Total Rows**: {p.row_count:,}")
        md.append(f"- **Total Columns**: {p.column_count}")
        md.append("")
        md.append("#### Schema & Missing Values")
        md.append("| Column Name | Missing Values Count | Missing % |")
        md.append("| :--- | :---: | :---: |")
        for col in p.columns_detail:
            md.append(f"| `{col.name}` | {col.missing_count:,} | {col.missing_percentage:.2f}% |")
        md.append("")
        
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md))
        
    print(f"Data profiling report generated at: {output_path}")

def main():
    dataset_name = os.getenv("KAGGLE_DATASET", "olistbr/brazilian-ecommerce")
    raw_data_path_str = os.getenv("RAW_DATA_PATH", "./data/raw")
    raw_data_path = Path(raw_data_path_str)
    
    # Download
    downloader = DatasetDownloader(dataset_name=dataset_name, target_dir=raw_data_path)
    downloader.download()
    
    # Profile
    profiler = DatasetProfiler(raw_dir=raw_data_path)
    profiles = profiler.profile_all()
    
    # Generate report
    report_path = Path("./docs/DATA_PROFILING.md")
    generate_profiling_report(profiles, report_path)

if __name__ == "__main__":
    main()
