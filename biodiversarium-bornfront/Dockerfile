ARG NODE_VERSION=18
ARG NPM_VERSION=8.19.2

# base
FROM node:${NODE_VERSION} as banuyls-biodiversarium-born-base

WORKDIR /usr/src/app
ENV PATH /usr/src/app/node_modules/.bin:$PATH

RUN npm install -g npm@${NPM_VERSION}

COPY package*.json ./

# prod
FROM banuyls-biodiversarium-born-base as banuyls-biodiversarium-born-prod

COPY package*.json ./

ENV NODE_ENV=production

RUN npm install -g serve
RUN npm ci --only=production

COPY . ./

RUN npm run build

EXPOSE 80

CMD serve -s build -l 80

# dev
FROM banuyls-biodiversarium-born-base as banuyls-biodiversarium-born-dev

COPY package*.json ./

ENV NODE_ENV=development

RUN npm install

COPY . ./

RUN npm run build

EXPOSE 80

CMD npm start 