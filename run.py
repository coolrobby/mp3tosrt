import os
import streamlit as st
import aeneas.executetask
from aeneas.tools import execute_task
from aeneas.textfile import TextFile
from aeneas.audiofile import AudioFile
from aeneas.task import Task

# 上传 MP3 和文本文件
st.title("生成SRT字幕文件")
uploaded_mp3 = st.file_uploader("上传 1.mp3 文件", type=["mp3"])
uploaded_txt = st.file_uploader("上传 1.txt 文件", type=["txt"])

if uploaded_mp3 and uploaded_txt:
    mp3_path = os.path.join("uploads", "1.mp3")
    txt_path = os.path.join("uploads", "1.txt")
    
    # 保存上传的文件
    with open(mp3_path, "wb") as f:
        f.write(uploaded_mp3.getbuffer())
    
    with open(txt_path, "wb") as f:
        f.write(uploaded_txt.getbuffer())

    # 读取文本文件内容
    with open(txt_path, "r", encoding="utf-8") as f:
        text_content = f.read()

    # 准备 Aeneas 的配置
    config_string = "task_language=eng|is_text_type=plain|os_task_file_format=srt|os_audio_file=" + mp3_path + "|os_text_file=" + txt_path
    
    # 创建 Aeneas 的任务并执行
    task = Task(config_string=config_string)
    execute_task(task)
    
    # 保存生成的 SRT 字幕文件
    srt_filename = "output.srt"
    task.save(os.path.join("uploads", srt_filename))
    
    # 显示生成的字幕内容
    st.subheader("生成的 SRT 字幕内容:")
    with open(os.path.join("uploads", srt_filename), "r", encoding="utf-8") as f:
        srt_content = f.read()
    
    st.text(srt_content)
    
    # 提供下载按钮
    st.download_button(
        label="下载 SRT 字幕文件",
        data=srt_content,
        file_name=srt_filename,
        mime="text/srt"
    )
