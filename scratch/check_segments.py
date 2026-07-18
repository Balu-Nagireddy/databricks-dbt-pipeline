from sqlalchemy import text
from src.warehouse.connection import connection_manager

def main():
    conn = connection_manager.get_connection()
    try:
        res = conn.execute(text("SELECT DISTINCT customer_segment FROM serving.dim_customers_clv;")).fetchall()
        print("Segments:", [r[0] for r in res])
    finally:
        conn.close()

if __name__ == "__main__":
    main()
