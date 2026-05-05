FROM golang:1.24-alpine
WORKDIR /app
RUN apk add --no-cache git
RUN git clone https://github.com/v03413/bepusdt.git .
RUN ls -la
RUN if [ -f main.go ]; then go build -o bepusdt main.go; else go build -o bepusdt ./cmd/bepusdt; fi
EXPOSE 8080
CMD ["./bepusdt"]
