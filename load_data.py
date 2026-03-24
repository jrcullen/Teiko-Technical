import sqlite3
import pandas as pd
import os

# File paths
DB_NAME = "cell_data.db"
CSV_FILE = "cell-count.csv"

def create_connection():
    return sqlite3.connect(DB_NAME)

def create_tables(conn):
    cursor = conn.cursor()

    # Create samples table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS samples (
        sample_id TEXT PRIMARY KEY,
        project TEXT,
        subject TEXT,
        condition TEXT,
        age INTEGER,
        sex TEXT,
        treatment TEXT,
        response TEXT,
        sample TEXT,
        sample_type TEXT,
        time_from_treatment_start INTEGER
    );
    """)

    # Create cell_counts table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cell_counts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sample_id TEXT,
        b_cell INTEGER,
        cd8_t_cell INTEGER,
        cd4_t_cell INTEGER,
        nk_cell INTEGER,
        monocyte INTEGER,
        FOREIGN KEY (sample_id) REFERENCES samples(sample_id)
    );
    """)

    conn.commit()

def load_data(conn):
    df = pd.read_csv(CSV_FILE)

    cursor = conn.cursor()

    for _, row in df.iterrows():
        # Insert into samples
        cursor.execute("""
        INSERT OR IGNORE INTO samples VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row["sample"],
            row["project"],
            row["subject"],
            row["condition"],
            row["age"],
            row["sex"],
            row["treatment"],
            row["response"],
            row["sample"],
            row["sample_type"],
            row["time_from_treatment_start"]
        ))

        # Insert into cell_counts
        cursor.execute("""
        INSERT INTO cell_counts (
            sample_id, b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte
        ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            row["sample"],
            row["b_cell"],
            row["cd8_t_cell"],
            row["cd4_t_cell"],
            row["nk_cell"],
            row["monocyte"]
        ))

    conn.commit()

def main():

    conn = create_connection()
    create_tables(conn)
    load_data(conn)
    conn.close()

    print(f"Database '{DB_NAME}' created and data loaded successfully.")

if __name__ == "__main__":
    main()