import os

def categorize_files(directory_path):
    # Initialize lists to store files by category
    file_types = {
        'pptx': [],
        'docx': [],
        'docs': [],
        'ppt': [],
        'mp4': [],
        'mp3': [],
        'txt': [],
        'csv': [],
        'html': [],
        'css': [],
        'xml': []
    }

    # Iterate through each file in the directory
    for filename in os.listdir(directory_path):
        # Get the file extension
        ext = filename.split('.')[-1].lower()  # Ensures that the extension is in lower case

        # Check if the extension is in our dictionary and add the file to the appropriate list
        if ext in file_types:
            file_types[ext].append(filename)

    return file_types
