FROM python:3.10
ENV PYTHONUNBUFFERED=1

ARG WORKDIR=/wd
ARG USER=user
ARG UID=1000

WORKDIR ${WORKDIR}

RUN useradd --system ${USER} --uid=${UID} && \
    chown --recursive ${USER} ${WORKDIR}

RUN apt update && apt upgrade -y

COPY --chown=${USER} requirements.txt requirements.txt

RUN pip install --upgrade pip && \
    pip install --requirement requirements.txt

COPY --chown=${USER} ./app.py app.py
COPY --chown=${USER} ./db db
COPY --chown=${USER} ./settings.py settings.py

USER ${USER}

ENTRYPOINT [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

#ENTRYPOINT FLASK_APP=app flask run --host=0.0.0.0