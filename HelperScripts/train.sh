#!/bin/bash -l

#SBATCH --job-name=training
#SBATCH --partition=nmes_gpu
#SBATCH --gres=gpu
#SBATCH --signal=USR2
#SBATCH --time=48:00:00
#SBATCH --mem=40960

module load anaconda3/2021.05-gcc-9.4.0
ml test_switch_kcl
source test_switch
ml git-lfs


source /users/${USER}/.bashrc
source activate /scratch/users/${USER}/conda/torch-env

python scripts/TrainNLLBEnPlPara.py
python scripts/TrainNLLBEnPlOpus.py
python scripts/TrainNLLBEnPlPara3.py
python scripts/TrainNLLBPlEnPara3.py
python scripts/TrainNLLBPlEnOpus.py
python scripts/TrainNLLBEnPlCC.py
python scripts/TrainNLLBPlEnCC.py


python scripts/TrainAlirezaEnPlCC.py
python scripts/TrainAlirezaPlEnCC.py
python scripts/TrainEnPlCC.py
python scripts/TrainPlEnCC.py
python scripts/TrainEnMulCC.py
python scripts/TrainMulEnCC.py

python scripts/TrainAlirezaEnPlkde4.py
python scripts/TrainAlirezaPlEnkde4.py
python scripts/TrainEnMulkde4.py
python scripts/TrainEnPlkde4.py
python scripts/TrainMulEnkde4.py
python scripts/TrainPlEnkde4.py

python scripts/TrainAlirezaEnPlOpus100.py
python scripts/TrainAlirezaPlEnOpus100.py
python scripts/TrainPlEnOpus100.py
python scripts/TrainEnPlOpus100.py
python scripts/TrainEnMulOpus100.py
python scripts/TrainMulEnOpus100.py

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