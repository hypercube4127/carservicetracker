FROM node:22.6.0-alpine3.19 AS prod

# Set environment variables
ENV DEBUG_MODE=False
ENV TZ=Europe/Budapest
RUN ln -snf "/usr/share/zoneinfo/$TZ" /etc/localtime
RUN echo "$TZ" > /etc/timezone

RUN apk --update add bash nginx

COPY nginx.conf /etc/nginx/nginx.conf
COPY mime.types /etc/nginx/mime.types

COPY . /opt/project
WORKDIR /opt/project
RUN npm install
RUN npm run build

EXPOSE 80
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s CMD curl -f http://localhost:80
ENTRYPOINT ["nginx", "-g", "daemon off;"]

FROM prod AS dev

ENV DEBUG_MODE=True
ENV NG_CLI_ANALYTICS=False
ENV CHOKIDAR_USEPOLLING=true

RUN apk --update add git inotify-tools 
RUN  chmod +x /opt/project/*.sh && ln -s /opt/project/service.sh /usr/local/bin/service

EXPOSE 4200
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s CMD curl -f http://localhost:4200
ENTRYPOINT [ "/opt/project/docker-entrypoint.sh" ]
