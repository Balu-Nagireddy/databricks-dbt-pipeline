from pathlib import Path
from sqlalchemy import text
from src.warehouse.transaction import db_transaction
from src.common.logging import get_logger

logger = get_logger(__name__)

def execute_ddl(sql_file_path: Path):
    """
    Reads the schema init SQL script, parses individual statements,
    and runs them sequentially inside a single database transaction.
    """
    logger.info(f"Loading SQL DDL script: {sql_file_path}")
    if not sql_file_path.exists():
        raise FileNotFoundError(f"SQL file not found at: {sql_file_path}")

    with open(sql_file_path, "r", encoding="utf-8") as f:
        sql = f.read()

    # Parse and extract statements by semicolon
    statements = []
    current_statement = []
    for line in sql.splitlines():
        trimmed = line.strip()
        if not trimmed or trimmed.startswith("--"):
            continue
        current_statement.append(line)
        if trimmed.endswith(";"):
            statements.append("\n".join(current_statement))
            current_statement = []

    logger.info(f"Found {len(statements)} DDL statements to execute.")

    # Execute all statements in a single transaction block
    with db_transaction() as conn:
        for index, stmt in enumerate(statements, 1):
            cleaned_stmt = stmt.strip()
            if cleaned_stmt:
                # Log first line of statement for visibility
                first_line = cleaned_stmt.splitlines()[0]
                logger.info(f"[{index}/{len(statements)}] Executing: {first_line[:120]}")
                conn.execute(text(cleaned_stmt))
                
    logger.info("DDL Schema Initialisation completed successfully.")
