FROM golang:1.24-alpine
WORKDIR /app
RUN apk add --no-cache git
RUN git clone https://github.com/v03413/bepusdt.git .
RUN go build -o bepusdt ./main
RUN mkdir -p /app/secure
RUN find /app -path "*/secure/secure.html" -exec sh -c 'cp -r $(dirname {})/* /app/secure/' \;
RUN ls -la /app/secure/
EXPOSE 8080
CMD ["./bepusdt", "start"]
