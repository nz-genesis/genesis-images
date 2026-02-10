FROM golang:1.21-alpine AS builder
ENV GOSUMDB=off
WORKDIR /app
COPY app/go.mod app/go.sum ./
RUN go mod download
COPY app/ .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o main main.go

FROM scratch
COPY --from=builder /app/main /main
EXPOSE 8080
CMD ["/main"]
