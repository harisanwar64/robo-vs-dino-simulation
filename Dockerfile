FROM python:3.7.9
ADD . /robo-vs-dino-simulation
WORKDIR /robo-vs-dino-simulation
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python3", "run.py"]