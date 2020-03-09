FROM python:3.8-slim

COPY ./ /work

RUN apt-get update \
&& apt-get install gcc ffmpeg -y \
&& apt-get clean

WORKDIR work

RUN pip install --user -r requirements.txt

RUN export PYTHONPATH=${PYTHONPATH}:/work/app

ENTRYPOINT ["/bin/bash", "/work/run.sh"]

CMD []

