FROM golang:1.24-alpine
WORKDIR /app
RUN apk add --no-cache git
RUN git clone https://github.com/v03413/bepusdt.git .
RUN go build -o bepusdt ./main
RUN mkdir -p /app/secure
RUN cp -r /app/web/secure/* /app/secure/ 2>/dev/null || true
RUN find /app -name "secure.html" -exec dirname {} \; | head -1 | xargs -I{} cp -r {}/* /app/secure/ 2>/dev/null || true
EXPOSE 8080
CMD ["./bepusdt", "start"]
