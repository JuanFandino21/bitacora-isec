FROM node:20-alpine
WORKDIR /app
COPY package.json .
RUN npm install --only=production
COPY server.js .
ENV API_URL=http://backend:8000/api
EXPOSE 3000
CMD ["npm","start"]
