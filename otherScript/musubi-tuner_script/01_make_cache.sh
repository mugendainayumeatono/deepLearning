source /home/vipuser/miniconda3/bin/activate /home/vipuser/miniconda3/envs/diffusion-pipe

cmd="python musubi-tuner/wan_cache_latents.py"
cmd="$cmd --dataset_config /home/hdd1/musubi-tuner/resource/dataset.toml"
cmd="$cmd --vae /home/hdd1/diffusion-pipe/modules/Wan2.1-I2V-14B-480P/Wan2.1_VAE.pth"
cmd="$cmd --clip /home/hdd1/diffusion-pipe/modules/Wan2.1-I2V-14B-480P/models_clip_open-clip-xlm-roberta-large-vit-huge-14.pth"
cmd="$cmd --vae_dtype bf16"
#cmd="$cmd --text_encoder_dtype bf16"

$cmd
