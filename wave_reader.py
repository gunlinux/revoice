import wave


reader = wave.Wave_read('out.wav')
print('channels:', reader.getnchannels())
print('getnframes:',reader.getnframes())
print('comptype:',reader.getcomptype())
print('sample_w:', reader.getsampwidth())
print('rate:', reader.getframerate())
print('get compname', reader.getcompname())
