#!/bin/bash -l

#SBATCH --job-name=hyperparam
#SBATCH --partition=nmes_gpu
#SBATCH --gres=gpu
#SBATCH --signal=USR2
#SBATCH --time=48:00:00
#SBATCH --mem=40960

module load anaconda3/2021.05-gcc-9.4.0

source /users/${USER}/.bashrc
source activate /scratch/users/${USER}/conda/torch-env


python scripts/hyperEnPlkde4.py
python scripts/hyperEnPlopus.py
python scripts/hyperEnPlpara.py
python scripts/hyperPlEnkde4.py
python scripts/hyperPlEnOpus.py
python scripts/hyperPlEnPara.py

python scripts/hyperEnMulkde4.py
python scripts/hyperEnMulOpus.py
python scripts/hyperEnMulPara.py

python scripts/hyperMulEnkde4.py
python scripts/hyperMulEnOpus.py
python scripts/hyperMulEnPara.py
