import pydub
import PyPDF2
import docx
import os 
from pptx import Presentation
import easyocr
import librosa
import torch

from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration , Speech2TextProcessor , Speech2TextForConditionalGeneration

model = Speech2TextForConditionalGeneration.from_pretrained('facebook/s2t-small-librispeech-asr')
processor = Speech2TextProcessor.from_pretrained('facebook/s2t-small-librispeech-asr')

def get_transcriptions(path) : 

    data , sr = librosa.load(path , sr = None) 

    if sr != 16000 : data = librosa.resample(
        data , 
        orig_sr = sr , 
        target_sr = 16000
    )

    text = ''

    audio_chunks = [
        data[index : index + int(1e5)]
        for index 
        in range(0 , len(data) , int(1e5))
    ]

    for chunk in audio_chunks : 

        inputs = processor(
            chunk , 
            sampling_rate = 16000 , 
            return_tensors = 'pt'
        )

        input_features = inputs.input_features      
        
        with torch.no_grad() : generated_ids = model.generate(inputs=input_features)
        transcription = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

        text += transcription

    return text


def get_text_from_audio(path) : 

    if path.endswith('mp3') : 

        audio = pydub.AudioSegment.from_mpr(path)
        new_path = f'{path}.wav'

        audio.export(new_path , format = 'wav')

        text = get_transcriptions(new_path)

    else : text = get_transcriptions(path)

    return text