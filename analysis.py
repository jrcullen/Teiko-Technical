import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu

DB_NAME = "cell_data.db"
OUTPUT_FILE = "summary.csv"
STATS_FILE = "stats.csv"
PLOT_FILE = "boxplot.png"


def load_data(conn):
    """
    Load joined data from samples + cell_counts tables
    """
    query = """
    SELECT 
        s.sample_id AS sample,
        s.project,
        s.subject,
        s.condition,
        s.treatment,
        s.response,
        s.sex,
        s.sample_type,
        s.time_from_treatment_start,
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

# Part 2
def initial_analysis(df):
    """
    Convert to long format and compute total counts + percentages
    """
    df["total_count"] = (
        df["b_cell"] +
        df["cd8_t_cell"] +
        df["cd4_t_cell"] +
        df["nk_cell"] +
        df["monocyte"]
    )

    long_df = df.melt(
        id_vars=["sample", "total_count", "condition", "treatment", "response", "sample_type"],
        value_vars=["b_cell", "cd8_t_cell", "cd4_t_cell", "nk_cell", "monocyte"],
        var_name="population",
        value_name="count"
    )

    long_df["percentage"] = (long_df["count"] / long_df["total_count"]) * 100

    return long_df

# Part 3
def statistical_analysis(summary_df):
    """
    Part 3: Compare responders vs non-responders using Mann–Whitney U test
    """

    # Filter required subset
    df = summary_df[
        (summary_df["condition"] == "melanoma") &
        (summary_df["treatment"] == "miraclib") &
        (summary_df["sample_type"] == "PBMC")
    ]

    # Statistical Testing
    results = []

    for population in df["population"].unique():
        pop_df = df[df["population"] == population]

        responders = pop_df[pop_df["response"] == "yes"]["percentage"]
        non_responders = pop_df[pop_df["response"] == "no"]["percentage"]

        # Mann–Whitney U test
        if len(responders) > 0 and len(non_responders) > 0:
            stat, pval = mannwhitneyu(responders, non_responders, alternative='two-sided')
        else:
            pval = None

        results.append({
            "population": population,
            "p_value": pval,
            "significant": pval < 0.05 if pval is not None else False
        })

    stats_df = pd.DataFrame(results)
    stats_df.to_csv(STATS_FILE, index=False)

    # Boxplot Visualization
    plt.figure(figsize=(8, 6))

    for i, population in enumerate(df["population"].unique()):
        pop_df = df[df["population"] == population]

        responders = pop_df[pop_df["response"] == "yes"]["percentage"]
        non_responders = pop_df[pop_df["response"] == "no"]["percentage"]

        positions = [i * 2, i * 2 + 1]

        plt.boxplot([responders, non_responders],
                    positions=positions,
                    widths=0.6)

    # X-axis labels
    labels = []
    for pop in df["population"].unique():
        labels.extend([f"{pop}\nR", f"{pop}\nNR"])

    plt.xticks(range(len(labels)), labels, rotation=45)
    plt.ylabel("Relative Frequency (%)")
    plt.title("Responders (R) vs Non-Responders (NR)")

    plt.tight_layout()
    plt.savefig(PLOT_FILE)
    plt.close()

    print(f"Stats saved to {STATS_FILE}")
    print(f"Boxplot saved to {PLOT_FILE}")

# Part 4
def subset_analysis(df):
    """
    Part 4: Subset analysis for baseline melanoma PBMC samples treated with miraclib
    """

    subset = df[
        (df["condition"] == "melanoma") &
        (df["treatment"] == "miraclib") &
        (df["sample_type"] == "PBMC") &
        (df["time_from_treatment_start"] == 0)
    ]

    print("\n--- Part 4 Results ---\n")

    # Samples per project
    samples_per_project = subset.groupby("project")["sample"].nunique()
    print("Samples per project:")
    print(samples_per_project)
    print()

    # Responders vs Non-Responders (by subject)
    response_counts = subset.groupby("response")["subject"].nunique()
    print("Subjects (Responders vs Non-Responders):")
    print(response_counts)
    print()

    # Males vs Females (by subject)
    sex_counts = subset.groupby("sex")["subject"].nunique()
    print("Subjects (Male vs Female):")
    print(sex_counts)
    print()

    # Avg B cells (melanoma males, responders, time=0)
    male_responders = subset[
        (subset["sex"] == "M") &
        (subset["response"] == "yes")
    ]

    avg_b_cells = male_responders["b_cell"].mean()

    if pd.notna(avg_b_cells):
        avg_b_cells = round(avg_b_cells, 2)
    else:
        avg_b_cells = None

    print("Average B cells (Melanoma, Male, Responders, t=0):")
    print(avg_b_cells)
    print()

    # save results
    subset.to_csv("subset_data.csv", index=False)

def main():
    conn = sqlite3.connect(DB_NAME)

    # Load data
    df = load_data(conn)

    # Part 2
    summary_df = initial_analysis(df)
    summary_df.to_csv(OUTPUT_FILE, index=False)
    print(f"Summary table saved to {OUTPUT_FILE}")

    # Part 3
    statistical_analysis(summary_df)

    # Part 4
    subset_analysis(df)

    conn.close()


if __name__ == "__main__":
    main()