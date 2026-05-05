FROM golang:1.24-alpine
WORKDIR /app
RUN apk add --no-cache git
RUN git clone https://github.com/v03413/bepusdt.git .
RUN go build -o bepusdt ./main
EXPOSE 8080
CMD ["./bepusdt", "start"]
