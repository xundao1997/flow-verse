FROM docker.nju.edu.cn/node:24.17.0-bookworm-slim AS build

ENV COREPACK_HOME=/corepack

RUN mkdir -p "${COREPACK_HOME}" \
    && corepack enable \
    && corepack prepare pnpm@11.10.0 --activate \
    && chmod -R a+rX "${COREPACK_HOME}"

WORKDIR /app

COPY services/web/package.json services/web/pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY services/web/ ./
RUN pnpm run build

FROM docker.nju.edu.cn/nginx:1.30.3-alpine

ENV FLOWVERSE_API_UPSTREAM=flowverse-api:8000

COPY services/web/nginx/default.conf.template /etc/nginx/templates/default.conf.template
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 8080

HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
    CMD wget -q -O - http://127.0.0.1:8080/health/live >/dev/null || exit 1

CMD ["nginx", "-g", "daemon off;"]
