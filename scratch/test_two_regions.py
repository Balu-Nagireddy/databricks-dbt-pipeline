import os
import urllib.parse
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

def test():
    db_user = "postgres.vighgvgxeqmpzossxxjr"
    db_pass = "Rgukt@14314"
    db_name = "postgres"
    
    for region in ["ap-south-1", "us-east-1", "ap-southeast-1"]:
        db_host = f"aws-0-{region}.pooler.supabase.com"
        for port in ["5432", "6543"]:
            url = f"postgresql://{db_user}:{urllib.parse.quote_plus(db_pass)}@{db_host}:{port}/{db_name}"
            print(f"Testing {region} Port {port}...")
            try:
                engine = create_engine(url, connect_args={'connect_timeout': 3})
                with engine.connect() as conn:
                    print("SUCCESS!")
            except Exception as e:
                print(f"ERROR: {e}")

if __name__ == "__main__":
    test()
