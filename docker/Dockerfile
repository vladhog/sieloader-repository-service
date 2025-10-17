FROM ghcr.io/astral-sh/uv:python3.13-alpine
LABEL authors="vladhog"

COPY annotations.py params.py pyproject.toml server.py key.pgp sierra.ini uv.lock /repository/
ADD data /repository/data
WORKDIR /repository/

RUN apk add build-base openssl-dev python3-dev bsd-compat-headers libffi-dev
RUN uv sync --locked --no-install-project --no-editable --compile-bytecode --no-cache --no-dev
ENV PATH="/repository/.venv/bin:$PATH"

RUN addgroup appgroup -g 1001 && adduser appuser -G appgroup -D -u 1001
USER appuser

EXPOSE 8060
ENTRYPOINT ["hypercorn", "server:app", "--quic-bind", "0.0.0.0:8060", "--bind", "0.0.0.0:8060", "-k", "uvloop"]