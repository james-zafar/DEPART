FROM python:latest

ENV APP_ROOT=/opt/app-root
RUN mkdir -p ${APP_ROOT}/python
USER root

ENV PYTHON_VERSION=3.10 \
    PATH=${APP_ROOT}/bin/:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    PIP_NO_CACHE_DIR=off \
    PYTHONPATH=${APP_ROOT} \
    HOME=${APP_ROOT}/src

RUN mkdir -p ${HOME}
WORKDIR ${HOME}

COPY ./requirements.txt ${HOME}/requirements.txt

COPY ./app ${HOME}/app

RUN pip install --upgrade pip && pip install --no-cache-dir -r ${HOME}/requirements.txt && \
    chown -R 1001:0 ${APP_ROOT} && \
    chmod -R 777 ${APP_ROOT}

EXPOSE 8000

user 1001

CMD [ "python", "-m",  "app.main" ]