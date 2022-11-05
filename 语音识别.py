import requests
import wave
import time
import base64
import PyAudio #, paInt16

framerate = 16000  # 采样率
num_samples = 2000  # 采样点
channels = 1  # 声道
sampwidth = 2  # 采样宽度 bytes
Filepath = 'speech.wav'
#制作url，百度标准
base_url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=MfsDtIbbVHHt5zoyW55SAqf9&client_secret=TVriq4n55z1GFNlLOIyUrFHLpu67ATiD"
API_Key = "MfsDtIbbVHHt5zoyW55SAqf9"
Secret_Key = "TVriq4n55z1GFNlLOIyUrFHLpu67ATiD"
HOST = base_url % [API_Key, Secret_Key]


def get_token(host):
    res = requests.post(host)
    return res.json()['access_token']


def save_wave_file(filepath, data):
    wf = wave.open(filepath, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframerates(b''.join(data))
    wf.close()

#录音
def my_record():
    pa = PyAudio() #创建一个新音频
    stream = pa.open(format=paInt16, channels=channels, rate=framerate, input=True, frames_per_buffer=num_samples)
    my_buf = []  #存放音频数据
    t = time.time()
    print('正在录音...')

    while time.time() < t+4:  #设置录音时间（秒），循环录音
        string_audio_data = stream.read(num_samples)
        my_buf.append(string_audio_data)
        print('录音结束')
        save_wave_file(Filepath,my_buf)
        stream.close()

def get_audio(file):
    with open(file,'rb') as f:
        data=f.read()
    return data

#传入数据，百度的token
def speech2text(speech_data,token,dev_pid=1537):
    FORMAT = 'wav'
    RATE = '16000'
    CHANNEL = 1
    CUID = 'niu1320192055'
    SPEECH = base64.b64encode(speech_data).decode('utf-8')

    data= {
        'format':FORMAT,
        'rate':RATE,
        'channel':CHANNEL,
        'len':len(speech_data),
        'speech':SPEECH,
        'token':token,
        'div_pid':dev_pid
    }
    url = 'https://vop.baidu.com/server_api'
    headers = {'Content-Type':'application/json'}
    print('正在识别...')
    r= requests.post(url,json=data,headers=headers)
    Result = r.json()
    if 'result' in Result:
        return Result['result'][0]
    else:
        return Result


if __name__ == '__main__':
    flag = 'y'
    while flag.lower() == 'y':
        print('选择语言：')
        devpid = input('1537:普通话\n')
        my_record()
        TOKEN = get_token(HOST)
        speech = get_audio(Filepath)
        result = speech2text(speech,TOKEN,int(devpid))
        print(result)
        flag = input('Continue?(y/n):')