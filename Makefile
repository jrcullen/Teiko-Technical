# Makefile

# Setup target: creates the conda environment
setup:
	conda env create -f env/environment.yml -n teiko

# Pipeline target: runs the full data pipeline
pipeline:
	snakemake --cores 1 --rerun-incomplete

# Dashboard target: starts the interactive Streamlit dashboard
dashboard:
	streamlit run dashboard/dashboard.py