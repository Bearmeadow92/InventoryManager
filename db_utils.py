import sqlite3

# Database initialization
def init_db():
    """Initialize the SQLite database."""
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    # Create the assets table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        assigned_to TEXT,
        brand TEXT,
        model TEXT,
        serial_number TEXT,
        mac_address TEXT,
        ip_address TEXT,
        warranty_expiration TEXT,
        notes TEXT
    )
    """)

    conn.commit()
    conn.close()

def execute_query(query, params=()):
    """Execute a query on the database."""
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def fetch_all(query, params=()):
    """Fetch all results from a query."""
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results
