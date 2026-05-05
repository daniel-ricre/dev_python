FROM golang:1.21-alpine
WORKDIR /app
RUN apk add --no-cache git
RUN git clone https://github.com/v03413/bepusdt.git .
RUN go build -o bepusdt main.go
EXPOSE 8080
CMD ["./bepusdt"]
