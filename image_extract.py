import os 
import easyocr
import torch

from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

img_processor = BlipProcessor.from_pretrained('Salesforce/blip-image-captioning-base')
img_model = BlipForConditionalGeneration.from_pretrained('Salesforce/blip-image-captioning-base')

def blip(path) : 

    image = Image.open(path)

    inputs = img_processor(image, return_tensors="pt")

    out = img_model.generate(**inputs)
    text = img_processor.decode(out[0] , skip_special_tokens = True)
    
    return text


def text_ocr(path) : 

    reader = easyocr.Reader(['en'])
    result = reader.readtext(path)

    return result

def image_text(path):
    result = text_ocr(path)
    if len(result) > 0:
        return result
    else:
        return bliq(path)