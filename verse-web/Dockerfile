FROM node:20-bookworm-slim AS builder

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .

ARG VITE_APP_NAME="Verse Web"
ARG VITE_API_BASE_URL="http://localhost:8000/api/v1"
ARG VITE_REQUEST_TIMEOUT_MS=8000

ENV VITE_APP_NAME=${VITE_APP_NAME}     VITE_API_BASE_URL=${VITE_API_BASE_URL}     VITE_REQUEST_TIMEOUT_MS=${VITE_REQUEST_TIMEOUT_MS}

RUN npm run build

FROM nginx:1.27-alpine AS runtime

COPY nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
