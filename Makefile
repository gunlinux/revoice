prep:
	git clone git@github.com:ufal/whisper_streaming.git

runserver:
	python3 whisper_streaming/whisper_online_server.py --model=medium --lan=ru # --warmup-file /tmp/fjk.wav
