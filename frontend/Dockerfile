FROM node:22.6.0-alpine3.19 AS base
ENV TZ=Europe/Budapest
ENV INSTALL_PATH=/opt/project
RUN ln -snf "/usr/share/zoneinfo/$TZ" /etc/localtime
RUN echo "$TZ" > /etc/timezone
RUN apk --update add bash
RUN mkdir -p $INSTALL_PATH
COPY ./package.json ./package-lock.json $INSTALL_PATH/
WORKDIR $INSTALL_PATH
RUN npm install

FROM base AS build
COPY . $INSTALL_PATH
RUN npm run build

FROM alpine:3.19 AS prod
EXPOSE 80
ENV INSTALL_PATH=/usr/share/nginx/html
ENV TZ=Europe/Budapest
WORKDIR $INSTALL_PATH
RUN ln -snf "/usr/share/zoneinfo/$TZ" /etc/localtime
RUN echo "$TZ" > /etc/timezone
RUN apk --update add nginx curl
COPY nginx.conf /etc/nginx/nginx.conf
COPY mime.types /etc/nginx/mime.types
COPY --from=build /opt/project/dist/cst-app/browser/ $INSTALL_PATH/
RUN set -x ; \
  addgroup -g 82 -S www-data ; \
  adduser -u 82 -D -S -G www-data www-data && exit 0 ; exit 1
RUN chown -R www-data:www-data "$INSTALL_PATH"
RUN chmod -R 0755 "$INSTALL_PATH"
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s CMD curl -f http://localhost:80
COPY envtoconfig.sh /docker-entrypoint.d/
RUN chmod +x /docker-entrypoint.d/envtoconfig.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]

FROM base AS dev
ENV NG_CLI_ANALYTICS=False
ENV CHOKIDAR_USEPOLLING=true
RUN apk --update add git inotify-tools jq
EXPOSE 4200
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s CMD curl -f http://localhost:4200
COPY . $INSTALL_PATH
RUN chmod +x $INSTALL_PATH/*.sh && ln -s $INSTALL_PATH/service.sh /usr/local/bin/service && ln -s $INSTALL_PATH/envtoconfig.sh /usr/local/bin/envtoconfig
ENTRYPOINT [ "/opt/project/docker-entrypoint.sh" ]
