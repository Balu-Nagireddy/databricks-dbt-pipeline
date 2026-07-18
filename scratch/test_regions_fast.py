import os
import urllib.parse
import concurrent.futures
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

regions = [
    "ap-southeast-1", "ap-south-1", "ap-south-2", "ap-southeast-2", "ap-northeast-1", "ap-northeast-2", 
    "us-east-1", "us-east-2", "us-west-1", "us-west-2", 
    "eu-west-1", "eu-central-1", "eu-west-2", "eu-west-3", "eu-north-1",
    "sa-east-1", "ap-southeast-3", "me-central-1", "ca-central-1"
]

def test_combination(region, port, password):
    db_user = "postgres.vighgvgxeqmpzossxxjr"
    db_name = "postgres"
    db_host = f"aws-0-{region}.pooler.supabase.com"
    
    escaped = urllib.parse.quote_plus(password)
    url = f"postgresql://{db_user}:{escaped}@{db_host}:{port}/{db_name}"
    try:
        engine = create_engine(url, connect_args={'connect_timeout': 2})
        with engine.connect() as conn:
            conn.execute("SELECT 1")
            return (region, port, password, True, None)
    except Exception as e:
        return (region, port, password, False, str(e))

def test_all():
    db_pass = "Rgukt@14314"
    tasks = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        for region in regions:
            for port in ["5432", "6543"]:
                for password in [db_pass, "Rgukt@14314D"]:
                    tasks.append(
                        executor.submit(test_combination, region, port, password)
                    )
        
        for future in concurrent.futures.as_completed(tasks):
            region, port, password, success, error = future.result()
            if success:
                print(f"SUCCESS: region={region}, port={port}, password={password}")
                executor.shutdown(wait=False, cancel_futures=True)
                return
            else:
                # Print ALL errors to inspect the difference
                print(f"FAILED: region={region}, port={port}, pwd={password[:5]} -> {error[:120]}")

if __name__ == "__main__":
    test_all()
