# Makefile

# Pipeline target
make pipeline:
	snakemake --cores 1 --rerun-incomplete