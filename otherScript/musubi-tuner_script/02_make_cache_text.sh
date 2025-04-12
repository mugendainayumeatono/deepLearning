source /home/vipuser/miniconda3/bin/activate /home/vipuser/miniconda3/envs/diffusion-pipe

cmd="python musubi-tuner/wan_cache_text_encoder_outputs.py"
cmd="$cmd --dataset_config /home/hdd1/musubi-tuner/resource/dataset.toml"
cmd="$cmd --t5 /home/hdd1/diffusion-pipe/modules/Wan2.1-I2V-14B-480P/models_t5_umt5-xxl-enc-bf16.pth"
cmd="$cmd --batch_size 1"
#cmd="$cmd --fp8_t5"

$cmd
