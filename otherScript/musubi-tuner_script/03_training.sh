source /home/vipuser/miniconda3/bin/activate /home/vipuser/miniconda3/envs/diffusion-pipe
export CUDA_HOME=/usr/local/cuda

cmd="accelerate launch"
cmd="$cmd --num_cpu_threads_per_process 1"
cmd="$cmd --mixed_precision bf16"
cmd="$cmd musubi-tuner/wan_train_network.py"
cmd="$cmd --task i2v-14B"
cmd="$cmd --dit /home/hdd1/comfyUI/ComfyUI/models/diffusion_models/confyui-org/wan2.1_i2v_480p_14B_bf16.safetensors"
cmd="$cmd --dataset_config /home/hdd1/musubi-tuner/resource/dataset.toml"
cmd="$cmd --sdpa"
#cmd="$cmd --flash-attn"
#cmd="$cmd --split_attn"
cmd="$cmd --mixed_precision bf16"
#cmd="$cmd --fp8_base"
cmd="$cmd --optimizer_type adamw8bit"
cmd="$cmd --learning_rate 2e-4"
cmd="$cmd --gradient_checkpointin"
cmd="$cmd --max_data_loader_n_workers 2"
cmd="$cmd --persistent_data_loader_workers"
cmd="$cmd --network_module networks.lora_wan"
cmd="$cmd --network_dim 32"
cmd="$cmd --timestep_sampling shift"
cmd="$cmd --discrete_flow_shift 3.0"
cmd="$cmd --max_train_epochs 16"
cmd="$cmd --save_every_n_epochs 1"
cmd="$cmd --seed 42"
cmd="$cmd --output_dir /home/hdd1/musubi-tuner/output"
cmd="$cmd --output_name yami_vioed_beta1.lora"
cmd="$cmd --blocks_to_swap 36" ##max value 36

#$cmd >log.log 2>&1 &
$cmd
