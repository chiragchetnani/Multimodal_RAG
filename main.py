from image_extract import blip, text_ocr
from discriminator import categorize_files
from doc_extract import pdf, docs, doc, pptx, csv, txt
from video_extract import video_transcript
import torch
import transformers
import numpy
import pandas 
import streamlit 

# Specify the directory containing your files
directory = 'Assets/'

# Categorize files in the directory
file_category = categorize_files(directory)

# Initialize a variable to accumulate context text
context_text = ''

# Process each file type using the appropriate extraction function
# Assuming each function returns text extracted from the files

# Text extraction from documents
for ext, files in file_category.items():
    for file in files:
        file_path = f"{directory}{file}"
        if ext == 'pdf':
            context_text += [f"This data was extracted from the provided PDF by the user named {file_path}\n\n"] + pdf(file_path)
        elif ext in ['docx', 'doc']:
            context_text += doc(file_path)
        elif ext == 'pptx':
            context_text += pptx(file_path)
        elif ext == 'csv':
            context_text += csv(file_path)
        elif ext == 'txt':
            context_text += txt(file_path)

# image_extract functions return extracted texts from images
# Example for images (adjust according to actual usage)
if 'jpg' in file_category or 'png' in file_category:
    for image_format in ['jpg', 'png']:
        for image_file in file_category.get(image_format, []):
            image_path = f"{directory}{image_file}"
            context_text += text(image_path)  # Assuming 'blip' is correctly used here

# video_extract functions return transcripts
if 'mp4' in file_category:
    for video_file in file_category['mp4']:
        video_path = f"{directory}{video_file}"
        context_text += video_transcript(video_path)







    


