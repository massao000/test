import re
from pydub.utils import which
import streamlit as st
import os
import base64
import pandas as pd
from pydub import AudioSegment
from pydub.silence import split_on_silence
import subprocess
import wave
import io

# 音声ファイルの変換
class VoiceConversion:
    """
    音声ファイルをwavに変換する
    """

    def __init__(self, sound_fname, fname):
        """
        sound_fname : 音声ファイル名
        """
        self.sound_fname = sound_fname
        self.fname = fname
    
    def check_mp3_mp4(self):
        print(self.fname)
        if "mp3" in self.fname:
            print("mp3")
            return self.conversion_mp3(self.sound_fname)
        elif "mp4" in self.fname:
            print("mp4")
            return self.conversion_mp4(self.sound_fname)
        else:
            print("wav")
            return self.conversion_wav(self.sound_fname)

    def conversion_wav(self, s):
        sound = AudioSegment.from_file(s, "wav")
        so = sound.export("output.wav", format="wav")
        return sound, so

    def conversion_mp3(self, s):
    
        sound = AudioSegment.from_mp3(s)
        so = sound.export("output.wav", format="wav")
        return sound, so

    def conversion_mp4(self, s):
        # https://githubja.com/jiaaro/pydub
        sound = AudioSegment.from_file(s, "mp4")
        so = sound.export("output.wav", format="wav")
        return sound, so


uploader = st.file_uploader("", type=['mp4', 'mp3', 'wav'])

st.write(uploader)
st.write(uploader.read)
st.write(uploader.name)
st.audio(uploader)

# nowp = os.path.dirname(__file__)
# st.write(nowp)

d = st.button("test")
if d == True:
    # subprocess.call(['ffmpeg', '-i', uploader.name,
    #                'audio.wav'])
    sound2 = VoiceConversion(uploader, uploader.name)
    print(sound2)
    xx = sound2.check_mp3_mp4()
    # st.write(xx)
    print(type(xx[0]))
    print(xx[1])

    # メモリ上の処理
    bytesio = io.BytesIO()

    # wf = wave.open(xx, mode='rb')
    # print('type: ', type(wf))
    # st.audio(wf)

    # wavデータの分割（無音部分で区切る）
    chunks = split_on_silence(xx[0], min_silence_len=2000, silence_thresh=-40, keep_silence=1000)
    print(chunks)


    # # 分割したデータ毎にファイルに出力
    z = []
    for i, chunk in enumerate(chunks):
        
        d = chunk.export(f"outputi{i}.wav", format="wav")
        z.append(d)
    print(z)
    
    for i in z:
        d = AudioSegment.from_file(i, "wav")
        st.write(d)

    
st.download_button(label="test", data=wf.readframes(-1), file_name="test.wav")

# DLlink
def file_download_link(file, filenaem):
    csv = file.to_csv(index=False)  
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filenaem}.csv">download</a>'
    return href

df = pd.read_csv(r'webUI_streamlit\test.csv')
st.markdown(file_download_link(df, "test"), unsafe_allow_html=True)

df = pd.read_csv(r'webUI_streamlit\test copy.csv')
st.markdown(file_download_link(df, "test2"), unsafe_allow_html=True)