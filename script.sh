module load bioinfo-tools
module load python/3.7.2
module load cellranger/7.1.0

export PYTHONPATH=/sw/bioinfo/Chromium-cellranger/7.1.0/bianca/lib/python/site-packages:$PYTHONPATH

python3 /home/angee/Desktop/proj/data/ScRNA/demultiplexing/override_assign_features.py

cellranger multi --id=demultiplexed_pool2_rerun --csv=5p_hashing_demux_pool_2_rerun_config.csv