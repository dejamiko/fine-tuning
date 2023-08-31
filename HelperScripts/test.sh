#!/bin/bash -l

#SBATCH --job-name=testing
#SBATCH --partition=nmes_gpu
#SBATCH --gres=gpu
#SBATCH --signal=USR2
#SBATCH --time=48:00:00
#SBATCH --mem=10240

module load anaconda3/2021.05-gcc-9.4.0

source /users/${USER}/.bashrc
source activate /scratch/users/${USER}/conda/torch-env

pip install scipy>1.17
pip install --upgrade datasets

export TRANSFORMERS_CACHE=/scratch/users/k20010020/cache/

python scripts/TestModelScoresWMT.py
python scripts/TestModelScoresOpus.py
python scripts/TestModelScoresTatoeba.py
python scripts/TestModelScoresMix.py
python scripts/TestModelEfficiency.py
python scripts/TestModelScoresFlores.py
python scripts/TestModelScoresFloresTwo.py
python scripts/TestModelScoresFlores101.py
python scripts/TestModelScoresFlores101Two.py
python scripts/TestModelScoresOpus100.py
python scripts/TestModelScoresIVA.py
python scripts/TestModelScoresTED14.py
python scripts/TestModelScoresTED15.py
python scripts/TestModelScoresTED16.py