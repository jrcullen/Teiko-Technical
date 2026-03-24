rule all:
    input:
        "database/cell_data.db",
        "outputs/summary.csv",
        "outputs/stats.csv",
        "outputs/boxplot.png",
        "outputs/subset_data.csv"

rule load_data:
    input:
        "data/cell-count.csv"
    output:
        "database/cell_data.db"
    shell:
        "python analysis/load_data.py"

rule run_analysis:
    input:
        db="database/cell_data.db"
    output:
        summary="outputs/summary.csv",
        stats="outputs/stats.csv",
        boxplot="outputs/boxplot.png",
        subset="outputs/subset_data.csv"
    shell:
        "python analysis/analysis.py"