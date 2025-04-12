#!/bin/sh

source /home/vipuser/miniconda3/bin/activate /home/vipuser/miniconda3/envs/comfyui_other

nohup python /home/hdd1/comfyUI_other/ComfyUI/main.py --listen > /home/hdd1/comfyUI_other/ComfyUI/lastestRunningLog.log 2>&1 &
#nohup python main.py --listen --force-upcast-attention > lastestRunningLog.log 2>&1 &
echo "comfyui has run in background please see logfile lastestRunningLog.log"
#python main.py --listen
#python main.py --listen --cuda-device 0 --gpu-onl

