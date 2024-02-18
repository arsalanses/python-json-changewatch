FROM --platform=${BUILDPLATFORM:-linux/amd64} alpine:3.19.1 as certs

ENV SUPERCRONIC_URL=https://github.com/aptible/supercronic/releases/download/v0.2.29/supercronic-linux-amd64

RUN apk --update add ca-certificates curl
RUN curl -fsSLO "$SUPERCRONIC_URL"

FROM --platform=${BUILDPLATFORM:-linux/amd64} golang:1.22.0 as builder

ARG TARGETPLATFORM
ARG BUILDPLATFORM

ARG TARGETOS
ARG TARGETARCH
ARG APP_VERSION

WORKDIR /app/
ADD . .

RUN GO111MODULE=on CGO_ENABLED=0 GOOS=${TARGETOS} GOARCH=${TARGETARCH} go build -ldflags="-s -w -X 'main.version=${APP_VERSION:-0.1.0}'" -o app main.go
# RUN GO111MODULE=on CGO_ENABLED=0 go build -o app main.go

# FROM --platform=${TARGETPLATFORM:-linux/amd64} scratch
FROM --platform=${TARGETPLATFORM:-linux/amd64} alpine:3.19.1

ENV SUPERCRONIC=supercronic-linux-amd64
ENV SUPERCRONIC_SHA1SUM=cd48d45c4b10f3f0bfdd3a57d054cd05ac96812b
ENV TZ=Asia/Tehran

WORKDIR /app/

COPY --from=builder /app/app /app/app
COPY --from=certs /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=certs --chmod=0755 ${SUPERCRONIC} ./supercronic

COPY ./my-crontab ./my-crontab

# RUN echo "${SUPERCRONIC_SHA1SUM}  ${SUPERCRONIC}" | sha1sum -c - \
#  && chmod +x "$SUPERCRONIC" \
#  && mv "$SUPERCRONIC" "/usr/local/bin/${SUPERCRONIC}" \
#  && ln -s "/usr/local/bin/${SUPERCRONIC}" /usr/local/bin/supercronic

# ENTRYPOINT ["/app/app"]
CMD [ "./supercronic", "./my-crontab"]
