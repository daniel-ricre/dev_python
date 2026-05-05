FROM golang:1.24-alpine AS builder
WORKDIR /app
RUN apk add --no-cache git
RUN git clone https://github.com/v03413/bepusdt.git .
RUN go build -o bepusdt ./main
RUN ls -la /app/web/
RUN find /app -name "*.html" 2>/dev/null

FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/bepusdt .
COPY --from=builder /app/web ./web
COPY --from=builder /app/static ./static
RUN mkdir -p /app/secure
RUN find /app -name "secure.html" -exec cp {} /app/secure/ \; 2>/dev/null || true
RUN ls -la /app/secure/
EXPOSE 8080
CMD ["./bepusdt", "start"]
