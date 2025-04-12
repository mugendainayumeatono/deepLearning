docker run --rm --gpus all -p 30000:30000 \
-v /home/hdd1/LLM/deepSeek/deepSeekCache:/root/.cache/huggingface \
--ipc=host \
lmsysorg/sglang:latest python3 -m sglang.launch_server \
--model-path /root/.cache/huggingface/DeepSeek-R1-Distill-Qwen-14B \
--tp 1 \
--trust-remote-code \
--port 30000 \
--host 0.0.0.0
