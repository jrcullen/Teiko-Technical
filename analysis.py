import sqlite3
import pandas as pd

DB_NAME = "cell_data.db"
OUTPUT_FILE = "summary.csv"


def load_data(conn):
    """
    Load joined data from samples + cell_counts tables
    """
    query = """
    SELECT 
        s.sample_id AS sample,
        c.b_cell,
        c.cd8_t_cell,
        c.cd4_t_cell,
        c.nk_cell,
        c.monocyte
    FROM samples s
    JOIN cell_counts c
    ON s.sample_id = c.sample_id
    """
    return pd.read_sql(query, conn)


def compute_summary(df):
    """
    Convert to long format and compute total counts + percentages
    """
    # Calculate total count per sample
    df["total_count"] = (
        df["b_cell"] +
        df["cd8_t_cell"] +
        df["cd4_t_cell"] +
        df["nk_cell"] +
        df["monocyte"]
    )

    # Convert wide → long format
    long_df = df.melt(
        id_vars=["sample", "total_count"],
        value_vars=["b_cell", "cd8_t_cell", "cd4_t_cell", "nk_cell", "monocyte"],
        var_name="population",
        value_name="count"
    )

    # Calculate percentage
    long_df["percentage"] = (long_df["count"] / long_df["total_count"]) * 100

    return long_df


def main():
    conn = sqlite3.connect(DB_NAME)

    # Load data
    df = load_data(conn)

    # Compute summary table
    summary_df = compute_summary(df)

    # Save output
    summary_df.to_csv(OUTPUT_FILE, index=False)

    conn.close()

    print(f"Summary table saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()