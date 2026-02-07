import re

def validate_sql(sql: str) -> str:
    #remove markdown
    sql = re.sub(r"```sql", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"```", "", sql)
    sql = sql.strip()

    #safety checks
    forbidden = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER"]
    for word in forbidden:
        if word.lower() in sql.lower():
            raise ValueError("Unsafe SQL detected")

    return sql 
