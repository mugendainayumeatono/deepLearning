#source /home/vipuser/miniconda3/bin/activate /home/vipuser/miniconda3/envs/musubi-tuner
source 00_config.sh
export CUDA_HOME=/usr/local/cuda
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

cmd="accelerate launch"
cmd="$cmd --num_cpu_threads_per_process 1"
cmd="$cmd --mixed_precision bf16"
cmd="$cmd musubi-tuner/wan_train_network.py"
cmd="$cmd --task i2v-14B"
#cmd="$cmd --dit /home/hdd1/comfyUI/ComfyUI/models/diffusion_models/wan-kijai/Wan2_1-I2V-14B-720P_fp8_e4m3fn.safetensors"
cmd="$cmd --dit /home/hdd1/comfyUI/ComfyUI/models/diffusion_models/confyui-org/wan2.1_i2v_480p_14B_bf16.safetensors"
cmd="$cmd --dataset_config $DATA_SET_PATH"
#cmd="$cmd --sdpa"
cmd="$cmd --flash_attn"
#cmd="$cmd --split_attn"
#cmd="$cmd --xformers"
cmd="$cmd --mixed_precision bf16"
cmd="$cmd --fp8_base"
cmd="$cmd --optimizer_type adamw8bit"
cmd="$cmd --learning_rate 1e-5"
cmd="$cmd --gradient_checkpointin"
cmd="$cmd --max_data_loader_n_workers 2"
cmd="$cmd --persistent_data_loader_workers"
cmd="$cmd --network_module networks.lora_wan"
cmd="$cmd --network_dim 64"
cmd="$cmd --timestep_sampling shift"
cmd="$cmd --discrete_flow_shift 2.0"
cmd="$cmd --max_train_epochs 16"
cmd="$cmd --save_every_n_epochs 1"
cmd="$cmd --seed 6349681"
cmd="$cmd --output_dir /home/hdd1/musubi-tuner/output"
cmd="$cmd --output_name yami_vioed_beta1.lora"
cmd="$cmd --blocks_to_swap 36" ##max value 36

#$cmd >log.log 2>&1 &
$cmd
