#!/bin/bash -l

#SBATCH --job-name=translation-training
#SBATCH --partition=nmes_gpu
#SBATCH --gres=gpu
#SBATCH --signal=USR2
#SBATCH --time=48:00:00
#SBATCH --mem=10240

module load anaconda3/2021.05-gcc-9.4.0
ml test_switch_kcl
source test_switch
ml git-lfs


source /users/${USER}/.bashrc
source activate /scratch/users/${USER}/conda/torch-env

pip install accelerate
pip install tqdm

python scripts/TrainAlirezaEnPlkde4.py
python scripts/TrainAlirezaPlEnkde4.py
python scripts/TrainEnMulkde4.py
python scripts/TrainEnPlkde4.py
python scripts/TrainMulEnkde4.py
python scripts/TrainPlEnkde4.py

python scripts/TrainAlirezaEnPlOpusAcc.py
python scripts/TrainAlirezaPlEnOpusAcc.py
python scripts/TrainPlEnOpusAcc.py
python scripts/TrainEnPlOpusAcc.py
python scripts/TrainEnMulOpusAcc.py
python scripts/TrainMulEnOpusAcc.py

python scripts/TrainAlirezaEnPlParaCrawl.py
python scripts/TrainAlirezaPlEnParaCrawl.py
python scripts/TrainPlEnPara.py
python scripts/TrainEnPlPara.py
python scripts/TrainEnMulPara.py
python scripts/TrainMulEnPara.py

python scripts/TrainAlirezaEnPlParaCrawl3.py
python scripts/TrainAlirezaPlEnParaCrawl3.py
python scripts/TrainPlEnPara3.py
python scripts/TrainEnPlPara3.py
python scripts/TrainEnMulPara3.py
python scripts/TrainMulEnPara3.py