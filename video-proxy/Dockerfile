ARG NODE_VERSION=18
ARG NPM_VERSION=8.19.2

FROM node:${NODE_VERSION} as banuyls-biodiversarium-video-proxy-signed

WORKDIR /usr/src/app
ENV PATH /usr/src/app/node_modules/.bin:$PATH

COPY package*.json ./

ENV NODE_ENV=production

RUN npm install -g npm@${NPM_VERSION}

RUN npm ci --only=production

COPY . .
EXPOSE 80

CMD node index.js


FROM alpine:3.17 as banuyls-biodiversarium-video-proxy-vlc

RUN apk add vlc

RUN adduser -k /vlc -D -u 1000 vlc

WORKDIR /vlc

COPY entrypoint.sh entrypoint.sh

USER "vlc"

ENTRYPOINT ["/vlc/entrypoint.sh"]
