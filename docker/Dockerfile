FROM ghcr.io/astral-sh/uv:python3.13-alpine
LABEL authors="vladhog"

COPY annotations.py params.py pyproject.toml server.py key.pgp sierra.ini uv.lock /repository/
ADD data /repository/data
WORKDIR /repository/

RUN apk add --no-cache build-base
RUN apk add --no-cache openssl-dev
RUN apk add --no-cache python3-dev
RUN apk add --no-cache bsd-compat-headers
RUN apk add --no-cache libffi-dev

RUN uv sync --locked --no-install-project --no-editable --compile-bytecode --no-cache --no-dev
ENV PATH="/repository/.venv/bin:$PATH"

RUN addgroup appgroup -g 1001 && adduser appuser -G appgroup -D -u 1001
USER appuser

EXPOSE 8060
ENTRYPOINT ["hypercorn", "server:app", "--quic-bind", "0.0.0.0:8060", "--bind", "0.0.0.0:8060", "-k", "uvloop"]