FROM python:3.12.2-alpine3.19 AS base
ENV TZ=Europe/Budapest
RUN ln -snf "/usr/share/zoneinfo/$TZ" /etc/localtime && echo "$TZ" > /etc/timezone
RUN apk --update add bash curl
RUN rm -rf /var/cache/apk/*
RUN python3 -m pip install poetry==1.8.3
WORKDIR /opt/project
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s CMD curl -f http://localhost:5000/echo
SHELL ["/bin/bash", "-c"]
EXPOSE 5000
COPY pyproject.toml poetry.lock /opt/project/
RUN poetry install --no-root

FROM base AS prod
COPY . /opt/project
ENTRYPOINT [ "poetry", "run", "start" ]

FROM base AS dev
RUN apk --update add git
EXPOSE 5678
ENV PYDEVD_DISABLE_FILE_VALIDATION=1
ENV FLASK_ENV=development
ENV AUTO_RELOAD=True
ENV DEBUG_MODE=True
COPY . /opt/project
RUN chmod +x /opt/project/*.sh
RUN ln -s /opt/project/service.sh /usr/local/bin/service
ENTRYPOINT [ "/opt/project/docker-entrypoint.sh" ]