import os
import uuid
import torch

from django.http import JsonResponse
from django.core.files.storage import default_storage
from rest_framework.decorators import api_view

from googletrans import Translator
from pytube import YouTube
from diffusers import DiffusionPipeline

def get_video_title(video_url):
    try:
        yt = YouTube(video_url)
        title = yt.title
        return title
    
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def translate_text(text, target_language='en'):
    try:
        translator = Translator()
        translation = translator.translate(text, dest=target_language)
        return translation.text

    except Exception as e:
        print(f"Error: {e}")
        return None

@api_view(['POST'])
def make_img(request):
    print(print(f"CUDA available: {torch.cuda.is_available()}"))
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    video_url = request.data.get('video_url')  # Получаем URL видео из тела запроса
    pipeline = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
    title = get_video_title(video_url)
    prompt = translate_text(title, "en")

    if prompt:
        print(f"Title: {prompt}")
        pipeline.to(device)
        image = pipeline(prompt, num_inference_steps=50).images[0]

        # Генерируем уникальное имя для изображения
        image_name = f'{uuid.uuid4()}.jpg'

        # Сохраняем изображение в папку img с уникальным именем
        img_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'img'))
        os.makedirs(img_folder_path, exist_ok=True)
        img_path = os.path.join(img_folder_path, image_name)

        # Сохраняем изображение
        with default_storage.open(img_path, 'wb') as destination:
            image.save(destination)

        # Пример возвращения ссылки на изображение
        return JsonResponse({'image_url': f'http://127.0.0.1:8000/img/{image_name}'})

    else:
        print("Failed to get the title.")
        return JsonResponse({'error': 'Failed to get the title.'}, status=400)
