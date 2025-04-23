source /home/vipuser/miniconda3/bin/activate /home/vipuser/miniconda3/envs/diffusion-pipe
export CUDA_HOME=/usr/local/cuda
nohup deepspeed --num_gpus=1 diffusion-pipe/train.py --deepspeed --regenerate_cache --config config/yama_beta2.toml >log.log 2>&1 &
