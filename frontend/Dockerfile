# Dockerfile for React frontend (Vite)
FROM node:18-alpine

# set working directory
WORKDIR /app

# copy package manifests and install dependencies
COPY package.json package-lock.json* yarn.lock* ./
RUN npm install

# copy rest of the source
COPY . .

EXPOSE 3000

# start dev server by default; override in production
CMD ["npm", "run", "dev"]
