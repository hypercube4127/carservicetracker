FROM python:3.12.2-alpine3.19 AS prod

# Set environment variables
ENV TZ=Europe/Budapest
ENV DEBUG_MODE=False

RUN ln -snf "/usr/share/zoneinfo/$TZ" /etc/localtime && echo "$TZ" > /etc/timezone
RUN apk --update add bash curl
RUN rm -rf /var/cache/apk/*
RUN python3 -m pip install poetry==1.8.3

WORKDIR /opt/project

COPY . /opt/project
RUN chmod +x /opt/project/*.sh
RUN ln -s /opt/project/service.sh /usr/local/bin/service

RUN poetry install --no-root

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s CMD curl -f http://localhost:5000/echo
SHELL ["/bin/bash", "-c"]
EXPOSE 5000
ENTRYPOINT [ "/opt/project/docker-entrypoint.sh" ]

#####
###   From this point on, there are only modifications that are necessary for development
###   If you want to use prod only image please use ´docker build -t ${IMAGE_NAME} --target prod .´ command
#####

FROM prod AS dev
RUN apk --update add git

EXPOSE 5678

ENV PYDEVD_DISABLE_FILE_VALIDATION=1
ENV FLASK_ENV=development
ENV AUTO_RELOAD=True
ENV DEBUG_MODE=True