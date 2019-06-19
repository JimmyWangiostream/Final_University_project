#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A demo of the Google CloudSpeech recognizer."""
import sys
import time
import aiy.audio
import aiy.cloudspeech
import aiy.voicehat
import socket
import pyaudio
#from pyaudio.src import pyaudio
import wave
import tempfile
from pygame import mixer
mixer.init()
from gtts import gTTS
import threading
from pyaudio import PyAudio, paInt16
import wave

framerate=8000
NUM_SAMPLES=2000
channels=1
sampwidth=2
check=0
button=aiy.voicehat.get_button()
client=0

def speak(sentence):
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts=gTTS(text=sentence,lang='zh-tw')
        tts.save("{}.mp3".format(fp.name))
        mixer.music.load('{}.mp3'.format(fp.name))
        mixer.music.play()

def fun2(t):
    global button
    global check
    print('2')
    #button.wait_for_press()
    #print('fun2 pressed')
    button.wait_for_press()
    check=1
    print('fun2 out')

def save_wave_file(filename,data):
    wf=wave.open(filename,'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b"".join(data))
    wf.close()

def my_record():
    global button
    global check
    print("press button starting recording your requset")
    #print(a)
    button.wait_for_press()
    print("recording Now")
    my_thread=threading.Thread(target=fun2,args=(2,))
    my_thread.start()
    pa=PyAudio()
    stream=pa.open(format=paInt16,channels=1,rate=framerate,input=True,frames_per_buffer=NUM_SAMPLES)
    my_buf=[]
    check=0
    while check==0:
        string_audio_data=stream.read(NUM_SAMPLES,exception_on_overflow = False)
        my_buf.append(string_audio_data)
        #count+=1
        print('.')
        save_wave_file('101.wav',my_buf)
    stream.close()
    print('Over')
    my_thread.join()
'''
chunk=1024
def play(t):
    if t==1:
        wf=wave.open(r"01.wav",'rb')
    elif t==2:
        wf=wave.open(r"02.wav",'rb')
    p=PyAudio()
    stream=p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=wf.getnchannels(),rate=wf.getframerate(),output=True)
    while True:
        data=wf.readframes(chunk)
        if data=="":break
        stream.write(data)
    stream.close()
    p.terminate()
'''
def sendrequest():
    global client
    client.close()
    client1=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client1.connect(('140.116.20.138',9000))
    client1.send(b'101_request\n')
    time.sleep(1)
    with open("101.wav","rb") as f:
        print("sending file")
        data=f.read()
        tt=client1.sendall(data)
        #print("file is sent")
        #ndata=client.recv(2048)
        #print('1')
        #command=ndata.decode('utf-8')
        #speak(command)
        client1.close()
        f.close()
    print(tt)
    if tt is None:
        speak("成功送出囉")
        #sys.exit(0)
    else:
        speak("發生錯誤")

def main():
    mixer.music.set_volume(1.0)
    recognizer = aiy.cloudspeech.get_recognizer()
    #recognizer.expect_phrase('turn off the light')
    #recognizer.expect_phrase('開燈')
    #recognizer.expect_phrase('blink')
    global button
    global client
    #button = aiy.voicehat.get_button()
    led = aiy.voicehat.get_led()
    aiy.audio.get_recorder().start()
    while True:        
        print('Press the button and speak')
        button.wait_for_press()
        connect_server()
        print('Listening...')
        text = recognizer.recognize()
        if text is None:
            print('Sorry, I did not hear you.')
            client.send(b'nothing\n')
        else:
            print('You said "', text, '"')
            if '開燈' in text:
                client.send(b'101_1_1\n')
                #led.set_state(aiy.voicehat.LED.ON)
                #CHUNK=1024
                #wf=wave.open("Wate.wav",'rb')
                #p= pyaudio.PyAudio()
                #stream=p.open(format=p.get_format_from_width(f.getsampwidth()),
                #channels=wf.getnchannels(),
                #rate=wf.getframerate(),
                #output=True)
                #data=wf.readframe(CHUNK)
                #while data !='':
                    #stream.write(data)
                    #data=f.readframes(CHUNK)
                #stream.stop_stream()
                #stream.close()
                #p.terminate()
                speak('開燈囉')
                print('on light')
            elif '位置' in text:
                while True:
                    speak('請說出獄詢問的設備')
                    print('Press the button and speak')
                    button.wait_for_press()
                    print('Listening...')
                    text = recognizer.recognize()
                    if text is None:
                        speak('請在說一次')
                    elif '餐廳' in text:
                        speak('餐廳位於二樓宴會廳')
                        break
                    elif '泳池' in text:
                        speak('游泳池位於一樓露天區')
                        break
                    elif '遊戲室' in text:
                        speak('遊戲室位於四樓休閒中心')
                        break
                    elif '三溫暖' in text:
                        speak('三溫暖位於一樓多功能廳')
                        break
                    elif '健身房' in text:
                        speak('健身房位於地下一樓健身中心')
                        break
            elif '關燈' in text:
                client.send(b'101_1_0\n')
                speak('關燈囉')
                print('off light')
            elif '我要客房服務' in text:
                #client.send(b'101_request\n')
                speak('按下按鈕後開始錄音錄音完畢後再按一下完成錄音')
                my_record()
                speak('是否確認送出')
                    #speak(command)
                #speak(command)
                while True:
                    button.wait_for_press()
                    print('Listening...')
                    text = recognizer.recognize()
                    print(text)
                    if text is None:
                        speak('請在說一次')
                    elif '是' in text or '對' in text:
                        sendrequest()
                        break
                    else:
                        speak("以取消傳送")
                        client.send(b'cancel\n')
                        break
            elif '餐廳人數' in text:
                client.send(b'respeople\n')
                data=client.recv(2048)
                command=data.decode('utf-8')
                speak(command)
            elif '泳池人數' in text:
                client.send(b'poolpeople\n')
                data=client.recv(2048)
                command=data.decode('utf-8')
                speak(command)
            elif '遊戲室人數' in text:
                client.send(b'gameroompeople\n')
                data=client.recv(2048)
                command=data.decode('utf-8')
                speak(command)
            elif '三溫暖人數' in text:
                client.send(b'spapeople\n')
                data=client.recv(2048)
                command=data.decode('utf-8')
                speak(command)
            elif '健身房人數' in text:
                client.send(b'gympeople\n')
                data=client.recv(2048)
                command=data.decode('utf-8')
                speak(command)
            elif '乾洗' in text:
                client.send(b'drywash\n')
                data=client.recv(2048)
                command=data.decode('utf-8')
                speak(command)                
                print('Press the button and speak')
                button.wait_for_press()
                print('Listening...')
                text = recognizer.recognize()                
                client.send(bytes(text,encoding='utf8'))               
                data=client.recv(2048)
                command=data.decode('utf-8')
                speak(command)                
            elif '叫車' in text:
                client.send(b'callcar\n')
                data=client.recv(2048)
                command=data.decode('utf-8')
                speak(command)           
                print('Press the button and speak')
                button.wait_for_press()
                print('Listening...')
                text = recognizer.recognize() 
                client.send(bytes(text,encoding='utf8'))               
                data=client.recv(2048)
                command=data.decode('utf-8')
                speak(command)                                
                print('Press the button and speak')
                button.wait_for_press()
                print('Listening...')
                text = recognizer.recognize()                
                client.send(bytes(text,encoding='utf8'))               
                data=client.recv(2048)
                command=data.decode('utf-8')
                speak(command)                                
                print('Press the button and speak')
                button.wait_for_press()
                print('Listening...')
                text = recognizer.recognize()                
                client.send(bytes(text,encoding='utf8'))               
                data=client.recv(2048)
                command=data.decode('utf-8')
                speak(command)                                                  
            elif '擦鞋' in text:
                client.send(b'wipeshoes\n')
                data=client.recv(2048)
                command=data.decode('utf-8')
                speak(command)                
                print('Press the button and speak')
                button.wait_for_press()
                print('Listening...')
                text = recognizer.recognize()                
                client.send(bytes(text,encoding='utf8'))               
                data=client.recv(2048)
                command=data.decode('utf-8')
                speak(command)                
            elif '測試' in text:
                print('test')
                text="123\n"
                client.send(bytes(text,encoding='utf8'))               
            elif '預約' in text:
                command=""
                #client.send(b'booking\n')
                #data=client.recv(2048)
                #command=data.decode('utf-8')
                speak('您要預約何種設備')                
                print('Press the button and speak')
                button.wait_for_press()
                print('Listening...')
                text = recognizer.recognize()
                print(text)
                if '兒童' in text:
                    print(text)
                    command+='1'                
                    speak('您要預約的人數')   
                    while True:             
                        print('Press the button and speak')
                        button.wait_for_press()
                        print('Listening...')
                        text = recognizer.recognize()
                        print(text)
                        if '一' in text:
                            command+='1'
                            break               
                        elif '兩' in text:
                            command+='2'
                            break
                        else:
                            speak("最多只能預約兩個人喔")               
                    speak('您要預約第幾個時段第一個一九到十第二個十到十一第參個十五到十六第四個十六到十七')    
                    while True:            
                        print('Press the button and speak')
                        button.wait_for_press()
                        print('Listening...')
                        text = recognizer.recognize()                
                        print(text)
                        if '一' in text:
                            command+='1'
                            break               
                        elif '二' in text:
                            command+='2'
                            break
                        elif '三' in text:
                            command+='3'
                            break
                        elif '四' in text:
                            command+='4'
                            break
                        else :
                            speak("請說出第幾個時段")
                    command+='\n'
                    client.send(bytes(command,encoding='utf8'))               
                    #data=client.recv(2048)
                    #command=data.decode('utf-8')
                    print(command)
                    speak('預約完成')                
                elif '游泳' in text:
                    print(text)
                    command+='2'
                    speak('您要預約的設備')                
                    while True:                
                        print('Press the button and speak')
                        button.wait_for_press()
                        print('Listening...')
                        text = recognizer.recognize()
                        print(text)
                        if '溫暖' in text:
                            command+='1'
                            break               
                        elif '蒸氣' in text:
                            command+='2'
                            break
                        elif '按摩' in text:
                            commnad+='3'
                            break
                        else:
                            speak("可以預約的設施為三溫暖或蒸氣室或按摩浴") 
                    speak('您要預約的人數') 
                    while True:               
                        print('Press the button and speak')
                        button.wait_for_press()
                        print('Listening...')
                        text = recognizer.recognize()
                        print(text)
                        if '一' in text:
                            command+='1'
                            break               
                        elif '兩' in text:
                            command+='2'
                            break
                        else:
                            speak("最多只能預約兩個人喔")               
                    speak('您要預約第幾個時段第一個一九到十第二個十到十一第參個十五到十六第四個十六到十七')                
                    while True:
                        print('Press the button and speak')
                        button.wait_for_press()
                        print('Listening...')
                        text = recognizer.recognize()                
                        if '一' in text:
                            command+='1'
                            break               
                        elif '二' in text:
                            command+='2'
                            break
                        elif '三' in text:
                            command+='3'
                            break
                        elif '四' in text:
                            command+='4'
                            break
                        else :
                            speak("請說出第幾個時段")
                    command+='\n'
                    client.send(bytes(command,encoding='utf8'))               
                    #data=client.recv(2048)
                    #command=data.decode('utf-8')
                    print(command)
                    speak('預約完成')                
                elif 'SPA' in text:
                    print(text)
                    command+='2'
                    speak('您要預約的項目')                
                    while True:                
                        print('Press the button and speak')
                        button.wait_for_press()
                        print('Listening...')
                        text = recognizer.recognize()
                        print(text)
                        if '臉' in text:
                            command+='1'
                            break               
                        elif '美胸' in text:
                            command+='2'
                            break
                        elif '精油' in text or '水療' in text:
                            commnad+='3'
                            break
                        else:
                            speak("可以預約的項目為臉部專業護理或激活美胸暢循或精油水療") 
                    speak('您要預約的人數') 
                    while True:               
                        print('Press the button and speak')
                        button.wait_for_press()
                        print('Listening...')
                        text = recognizer.recognize()
                        print(text)
                        if '一' in text:
                            command+='1'
                            break               
                        elif '兩' in text:
                            command+='2'
                            break
                        else:
                            speak("最多只能預約兩個人喔")               
                    speak('您要預約第幾個時段第一個一九到十第二個十到十一第參個十五到十六第四個十六到十七')                
                    while True:
                        print('Press the button and speak')
                        button.wait_for_press()
                        print('Listening...')
                        text = recognizer.recognize()                
                        if '一' in text:
                            command+='1'
                            break               
                        elif '二' in text:
                            command+='2'
                            break
                        elif '三' in text:
                            command+='3'
                            break
                        elif '四' in text:
                            command+='4'
                            break
                        else :
                            speak("請說出第幾個時段")
                    command+='\n'
                    client.send(bytes(command,encoding='utf8'))               
                    #data=client.recv(2048)
                    #command=data.decode('utf-8')
                    print(command)
                    speak('預約完成')                
                elif '健身' in text:
                    print(text)
                    command+='2'
                    speak('您要預約的器材')                
                    while True:                
                        print('Press the button and speak')
                        button.wait_for_press()
                        print('Listening...')
                        text = recognizer.recognize()
                        print(text)
                        if '跑步' in text:
                            command+='1'
                            break               
                        elif '飛輪' in text:
                            command+='2'
                            break
                        elif '登山' in text:
                            commnad+='3'
                            break
                        elif '橢圓' in text:
                            commnad+='4'
                            break
                        elif '蝴蝶' in text:
                            commnad+='5'
                            break
                        else:
                            speak("可以預約的設施為跑步機或飛輪或登山機或橢圓機或蝴蝶機") 
                    speak('您要預約的人數') 
                    while True:               
                        print('Press the button and speak')
                        button.wait_for_press()
                        print('Listening...')
                        text = recognizer.recognize()
                        print(text)
                        if '一' in text:
                            command+='1'
                            break               
                        elif '兩' in text:
                            command+='2'
                            break
                        else:
                            speak("最多只能預約兩個人喔")               
                    speak('您要預約第幾個時段第一個一九到十第二個十到十一第參個十五到十六第四個十六到十七')                
                    while True:
                        print('Press the button and speak')
                        button.wait_for_press()
                        print('Listening...')
                        text = recognizer.recognize()                
                        if '一' in text:
                            command+='1'
                            break               
                        elif '二' in text:
                            command+='2'
                            break
                        elif '三' in text:
                            command+='3'
                            break
                        elif '四' in text:
                            command+='4'
                            break
                        else :
                            speak("請說出第幾個時段")
                    command+='\n'
                    client.send(bytes(command,encoding='utf8'))               
                    #data=client.recv(2048)
                    #command=data.decode('utf-8')
                    print(command)
                    speak('預約完成')                
            elif '取消' in text:
                client.send(b'cancel\n')
                data=client.recv(2048)
                command=data.decode('utf-8')
                speak(command)                
                print('Press the button and speak')
                button.wait_for_press()
                print('Listening...')
                text = recognizer.recognize()                
                client.send(bytes(text,encoding='utf8'))               
                data=client.recv(2048)
                command=data.decode('utf-8')
                speak(command)                                    
            elif '再見' in text:
                client.send(b'nothing\n')
                #break
def connect_server():
    global client
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(('140.116.20.138',9000))

if __name__ == '__main__':
    #client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #client.connect(('192.168.1.31',8000))
    #connect_server()
    main()
