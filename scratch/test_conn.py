import os
import urllib.parse
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def test_conn():
    db_user = "postgres.vighgvgxeqmpzossxxjr"
    db_pass = "Rgukt@14314"
    db_host = "aws-1-ap-south-1.pooler.supabase.com"
    db_name = "postgres"

    for port in ["6543", "5432"]:
        escaped = urllib.parse.quote_plus(db_pass)
        url = f"postgresql://{db_user}:{escaped}@{db_host}:{port}/{db_name}"
        print(f"Testing new pooler on port {port}...")
        try:
            engine = create_engine(url)
            with engine.connect() as conn:
                res = conn.execute(text("SELECT 1")).fetchone()
                print(f"SUCCESS! Result: {res}")
                return url
        except Exception as e:
            print(f"FAILED: {e}")

if __name__ == "__main__":
    test_conn()
