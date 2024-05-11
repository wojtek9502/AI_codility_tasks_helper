FROM python:3.10

WORKDIR /app

COPY --chown=1000:1000 requirements.txt .

RUN --mount=type=secret,id=ssh_key,uid=1000,gid=1000,dst=/id_key \
    pip install \
      --no-cache \
      --requirement requirements.txt

COPY --chown=1000:1000 . .
