import io
import os
import streamlit as st
import requests
import glob
import time
from PIL import Image
from gtts import gTTS
from googletrans import Translator
from model import get_caption_model, generate_caption
import pyttsx3
import base64
import warnings

translator = Translator()
try:
    os.mkdir("temp")
except:
    pass


@st.cache(allow_output_mutation=True)
def get_model():
    return get_caption_model()

caption_model = get_model()


def predict():
    
    text = generate_caption('tmp.jpg', caption_model)

    st.markdown('#### Predicted Captions:')
    st.write(text)

    out_lang = st.selectbox("Select your output language",
    ("English", "Hindi", "Bengali", "korean", "Chinese", "Japanese"),)
    if out_lang == "English":
        output_language = "en"
    elif out_lang == "Hindi":
        output_language = "hi"
    elif out_lang == "Bengali":
        output_language = "bn"
    elif out_lang == "korean":
        output_language = "ko"
    elif out_lang == "Chinese":
        output_language = "zh-cn"
    elif out_lang == "Japanese":
        output_language = "ja"

    def text_to_speech(output_language, text):
        translation = translator.translate(text, src='en', dest=output_language)
        trans_text = translation.text
        tts = gTTS(trans_text, lang=output_language,slow=False)
        try:
            my_file_name = text[0:20]
        except:
            my_file_name = "audio"
        tts.save(f"temp/{my_file_name}.mp3")
        return my_file_name, trans_text

    if st.button("convert"):
        result, output_text = text_to_speech(output_language, text)
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()
        st.markdown(f"## Your audio:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)
        st.markdown(f"## Output text:")
        st.write(f" {output_text}")



def get_prediction():
    global text
    text = generate_caption('tmp.jpg', caption_model)

    st.markdown('#### Predicted Captions:')
    st.write(text)

def audio():
    global my_file_name
    speech = gTTS(text, lang = 'en', slow = False)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    speech.save(f"temp/{my_file_name}.mp3")
    return my_file_name


def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )

   
st.title('Image Captioner')



img_file_buffer = st.camera_input("Take a picture")

if img_file_buffer is not None:
    img = img_file_buffer.read()
    img = Image.open(io.BytesIO(img))
    img = img.convert('RGB')
    img.save('tmp.jpg')
    st.image(img)
    get_prediction()
    audio()
    autoplay_audio(f"temp/{my_file_name}.mp3")
    os.remove('tmp.jpg')

st.markdown('<center style="opacity: 70%">OR</center>', unsafe_allow_html=True)

img_upload = st.file_uploader(label='Upload Image', type=['jpg', 'png', 'jpeg'])

if img_upload != None:
    img = img_upload.read()
    img = Image.open(io.BytesIO(img))
    img = img.convert('RGB')
    img.save('tmp.jpg')
    st.image(img)
    predict()
    os.remove('tmp.jpg')


def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) == n:
        for f in mp3_files:
            os.remove(f)
            print("File is been Removed")

remove_files(3)

