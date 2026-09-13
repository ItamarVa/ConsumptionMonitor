# ConsumptionMonitor Home Assistant add-on image.
# The add-on build context is this folder only, so the app is fetched from a pinned
# GitHub release tarball (APP_REF). Debian/glibc is required: scrapling fetchers have
# no musllinux wheels on Alpine.
ARG APP_REF=v1.0.4
FROM ghcr.io/home-assistant/amd64-base-debian:trixie

ARG APP_REF=v1.0.4

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        curl \
        ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN curl -fsSL "https://codeload.github.com/ItamarVa/ConsumptionMonitor/tar.gz/refs/tags/${APP_REF}" \
        | tar xz --strip-components=1 -C /app \
    && python3 -m venv /app/.venv \
    && /app/.venv/bin/pip install --no-cache-dir -r /app/requirements.txt

COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
