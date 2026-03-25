# Teiko-Technical
Helping Bob understand how his drug candidate affects immune cell populations.

# Setup the Environment
This project uses a Conda environment defined in env/environment.yml. First, run:

```bash
make setup
```

Then activate the environment using:

```bash
conda activate teiko
```

# Run the Full Data Pipeline
To execute the entire pipeline (Parts 1–4), run:

```bash
make pipeline
```

This will:

- Initialize the SQLite database (cell_data.db)
- Load data from data/cell-count.csv
- Generate the following outputs:

| File | Description |
|------|------------|
| outputs/summary.csv | Relative frequency table for each cell population (Part 2) |
| outputs/stats.csv | Statistical test results (Mann–Whitney U test) (Part 3) |
| outputs/boxplot.png | Boxplot comparing responders vs non-responders (Part 3) |
| outputs/subset_data.csv | Filtered baseline melanoma PBMC dataset (Part 4) |

# Launch the Interactive Dashboard
To start the Streamlit dashboard:

```bash
make dashboard
```

After running `make dashboard`, open the forwarded URL provided by Streamlit (such as: http://localhost:8501) in your browser.

The dashboard provides interactive access to:

- Summary table (Part 2)
- Responders vs non-responders comparison (Part 3)
- Baseline subset analysis (Part 4)

# Database Schema Design
The relational database consists of two main tables:

1. samples Table

| Column | Type | Description |
|--------|------|-------------|
| sample_id | TEXT (Primary Key) | Unique identifier for each sample |
| project | TEXT | Project the sample belongs to |
| subject | TEXT | Patient/subject identifier |
| condition | TEXT | Disease type |
| age | INTEGER | Age of subject |
| sex | TEXT | Biological sex |
| treatment | TEXT | Treatment administered |
| response | TEXT | Response to treatment (yes/no) |
| sample | TEXT | Original sample identifier |
| sample_type | TEXT | Sample type |
| time_from_treatment_start | INTEGER | Timepoint of sample collection |

2. cell_counts Table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER (Primary Key) | Auto-incremented row ID |
| sample_id | TEXT (Foreign Key) | Links to samples Table |
| b_cell | INTEGER | B cell count |
| cd8_t_cell | INTEGER | CD8 T cell count |
| cd4_t_cell | INTEGER | CD4 T cell count |
| nk_cell | INTEGER | NK cell count |
| monocyte | INTEGER | Monocyte count |

Design Rationale:

The database schema follows a normalized relational design by separating sample metadata and cell population counts into two tables. This makes sure that patient and sample information is only stored once, while cell measurements are linked through a foreign key relationship. This structure improves data integrity, simplifies updates, and makes queries more efficient and easier to understand, especially when joining metadata with cell count information for downstream analysis.

Scalability Considerations:

The schema would scale effectively if the dataset grew to include hundreds of projects and thousands of samples. New data could be added by just inserting additional rows without needing schema changes. Some other analytics that would be good to perform include longitudinal analyses to track how immune cell populations change over time within the same patient, because the time_from_treatment_start field enables timepoint comparisons. Cohort based analyses such as filtering by condition, treatment, or sample type, would also be useful for identifying trends across specific patient groups. Predictive modeling could also be performed using the cell population data to identify features associated with treatment response, since the structured format allows easy extraction of features for machine learning. If more cell types or measurements were introduced, the schema could be extended to support more flexible data structures, enabling even more advanced analyses in the future.

# Code Structure
The project separates data management, analysis, and visualization to ensure clarity, reproducibility, and modularity. Each part has its own role, making it easy to update or expand.
- load_data.py: Creates the database and loads the CSV data into structured tables.
- analysis/analysis.py: Performs all analysis such as summary tables, statistical comparisons, subset analysis, and generates output CSVs and plots.
- dashboard/dashboard_app.py: Reads the output files and presents them interactively in Streamlit.
- Snakefile: Orchestrates the full pipeline with Snakemake, ensuring all steps run reproducibly with `make pipeline`

This structure ensures that computation and visualization are separate, outputs are reproducible, and the project can scale to handle additional analyses or new dashboard features without disrupting existing functionality.