FROM nablascom/cuda-pytorch:latest

COPY . .
COPY ./src .

RUN mkdir img
RUN chmod -R 777 img

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu124

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
