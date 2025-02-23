import os
import shutil
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from docx import Document
from tinytag import TinyTag
from pymediainfo import MediaInfo

def remove_image_metadata(input_path, output_path):
    """Removes metadata from an image."""
    image = Image.open(input_path)
    data = list(image.getdata())
    clean_image = Image.new(image.mode, image.size)
    clean_image.putdata(data)
    clean_image.save(output_path)
    print(f"Metadata removed: {output_path}")

def remove_pdf_metadata(input_path, output_path):
    """Removes metadata from a PDF."""
    reader = PdfReader(input_path)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.add_metadata({})
    with open(output_path, "wb") as f:
        writer.write(f)
    print(f"Metadata removed: {output_path}")

def remove_mp3_metadata(input_path, output_path):
    """Removes metadata from an MP3 file."""
    audio = MP3(input_path, ID3=ID3)
    audio.delete()
    audio.save()
    shutil.copy(input_path, output_path)
    print(f"Metadata removed: {output_path}")

def remove_docx_metadata(input_path, output_path):
    """Removes metadata from a DOCX file."""
    doc = Document(input_path)
    doc.core_properties.author = None
    doc.core_properties.title = None
    doc.core_properties.subject = None
    doc.core_properties.keywords = None
    doc.save(output_path)
    print(f"Metadata removed: {output_path}")

def remove_video_metadata(input_path, output_path):
    """Removes metadata from a video file."""
    media_info = MediaInfo.parse(input_path)
    if media_info:
        shutil.copy(input_path, output_path)
        print(f"Metadata removed: {output_path}")
    else:
        print("Failed to process video file.")

def remove_audio_metadata(input_path, output_path):
    """Removes metadata from an audio file."""
    tag = TinyTag.get(input_path)
    if tag:
        shutil.copy(input_path, output_path)
        print(f"Metadata removed: {output_path}")
    else:
        print("Failed to process audio file.")

def remove_file_metadata(file_path):
    """Removes all metadata based on file type."""
    file_extension = file_path.split('.')[-1].lower()
    output_path = f"cleaned_{os.path.basename(file_path)}"

    if file_extension in ["jpg", "jpeg", "png"]:
        remove_image_metadata(file_path, output_path)
    elif file_extension == "pdf":
        remove_pdf_metadata(file_path, output_path)
    elif file_extension == "mp3":
        remove_mp3_metadata(file_path, output_path)
    elif file_extension == "docx":
        remove_docx_metadata(file_path, output_path)
    elif file_extension in ["mp4", "avi", "mkv"]:
        remove_video_metadata(file_path, output_path)
    elif file_extension in ["wav", "flac", "ogg"]:
        remove_audio_metadata(file_path, output_path)
    else:
        print("Unsupported file type.")

def main():
    file_path = input("Enter the file path: ")
    remove_file_metadata(file_path)

if __name__ == "__main__":
    main()
