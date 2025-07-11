FROM golang:1.21-alpine AS builder
WORKDIR /src
COPY . .
RUN go build -o app main.go

FROM alpine:3.18
WORKDIR /app
COPY --from=builder /src/app .
CMD ["./app"]
