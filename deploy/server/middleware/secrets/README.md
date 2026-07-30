# Runtime secrets

This directory intentionally contains no credential values. Create these four files on the target server before starting Compose:

- `postgres_password`
- `redis_password`
- `minio_root_user`
- `minio_root_password`

The parent `.gitignore` excludes every other file in this directory. Restrict file permissions to the deployment account and never commit, print, or copy the values into `.env` or `compose.yml`.
