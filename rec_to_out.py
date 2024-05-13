import pyaudio
import wave
import socket


DEVICE = 4


def save_wave(file, frames, sampleRate, sample_width=2):
    # sampleRate = 44100.0  # hertz
    sampleRate = 8000  # 44100.0  # hertz
    obj = wave.open(file, "w")
    obj.setnchannels(1)  # mono
    obj.setsampwidth(sample_width)
    obj.setframerate(sampleRate)
    for frame in frames:
        obj.writeframesraw(frame)
    obj.close()


class RecordAudio:
    def __init__(self, rate, chunk=512, index=None, format=None):
        self.audio = pyaudio.PyAudio()
        self.format = format
        self.recordframes = []
        self.index = index
        self.timelimit = 15
        self.chunk = chunk
        self.rate = rate

    def get_devices(self):
        info = self.audio.get_host_api_info_by_index(0)
        numdevices = info.get("deviceCount")
        for i in range(0, numdevices):
            if self.audio.get_device_info_by_host_api_device_index(0, i).get(
                "maxInputChannels"
            ):
                print(
                    "Input Device id ",
                    i,
                    " - ",
                    self.audio.get_device_info_by_host_api_device_index(0, i).get(
                        "name"
                    ),
                )

    def start_record(self, handler=None, timelimit=None):
        if timelimit:
            self.timelimit = timelimit

        stream = self.audio.open(
            format=self.format,
            channels=1,  # only mono only hc
            rate=self.rate,
            input=True,
            input_device_index=self.index,
            frames_per_buffer=self.chunk,
        )
        print("recording started")
        self.frames = []
        for _ in range(0, int(self.rate / self.chunk * self.timelimit)):
            data = stream.read(self.chunk)
            self.frames.append(data)
            #new_data = resample(data,  8000, 16000)
            if handler:
                handler(data)
        print("recorded frames count =", len(self.frames))


class Client:
    def __init__(self, host="127.0.0.1", port=43007):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.host, self.port))

    def close(self):
        self.socket.close()

    def process(self, data):
        #self.socket.send(resample(data, 8000, 16000))
        self.socket.send(data)


def main():
    FORMAT = pyaudio.paInt16
    RATE = 16000 
    CHUNK = 512

    record = RecordAudio(index=DEVICE, format=FORMAT, rate=RATE, chunk=CHUNK)
    record.get_devices()
    client = Client()
    client.connect()
    record.start_record(timelimit=60, handler=client.process)
    save_wave("out.wav", record.frames, sampleRate=RATE, sample_width=2)
    client.close()


if __name__ == "__main__":
    main()
