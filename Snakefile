rule all:
    input:
        "cell_data.db",
        "summary.csv",
        "stats.csv",
        "boxplot.png",
        "subset_data.csv"

rule load_data:
    input:
        "cell-count.csv"
    output:
        "cell_data.db"
    shell:
        "python load_data.py"

rule run_analysis:
    input:
        db="cell_data.db"
    output:
        summary="summary.csv",
        stats="stats.csv",
        boxplot="boxplot.png",
        subset="subset_data.csv"
    shell:
        "python analysis.py"