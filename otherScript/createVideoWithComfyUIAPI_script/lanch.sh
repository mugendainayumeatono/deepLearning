echo "$(date '+%Y-%m-%d %H:%M:%S') - lanch" > /home/hdd1/createVideoWithComfyUIAPI/lanch_log.log
echo "$(date '+%Y-%m-%d %H:%M:%S') - first kill old comfyui" >> /home/hdd1/createVideoWithComfyUIAPI/lanch_log.log
/bin/bash /home/hdd1/comfyUI_other/ComfyUI/kill.sh
sleep 2
echo "$(date '+%Y-%m-%d %H:%M:%S') - start comfyui" >> /home/hdd1/createVideoWithComfyUIAPI/lanch_log.log
/bin/bash /home/hdd1/comfyUI_other/ComfyUI/run.sh
sleep 30
echo "$(date '+%Y-%m-%d %H:%M:%S') - start createVideo" >> /home/hdd1/createVideoWithComfyUIAPI/lanch_log.log
/bin/bash /home/hdd1/createVideoWithComfyUIAPI/run.sh
echo "$(date '+%Y-%m-%d %H:%M:%S') - end" >> /home/hdd1/createVideoWithComfyUIAPI/lanch_log.log
