# Teiko-Technical
Helping Bob understand how his drug candidate affects immune cell populations.

# Setup the Environment
This project uses a Conda environment defined in env/environment.yml.

make setup

Then activate the environment:
conda activate teiko

# Run the Full Data Pipeline
To execute the entire pipeline (Parts 1–4), run:
make pipeline

This will:
Initialize the SQLite database (cell_data.db)
Load data from data/cell-count.csv
Generate the following outputs:

File	Description
outputs/summary.csv	Relative frequency table for each cell population (Part 2)
outputs/stats.csv	Statistical test results (Mann–Whitney U test) (Part 3)
outputs/boxplot.png	Boxplot comparing responders vs non-responders (Part 3)
outputs/subset_data.csv	Filtered baseline melanoma PBMC dataset (Part 4)

# Launch the Interactive Dashboard
To start the Streamlit dashboard:
make dashboard

Then open a browser and go to:
http://localhost:8501

The dashboard provides interactive access to:

Summary table (Part 2)
Responders vs non-responders comparison (Part 3)
Baseline subset analysis (Part 4)