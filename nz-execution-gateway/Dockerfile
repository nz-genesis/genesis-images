FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o main app/main.go

FROM scratch
COPY --from=builder /app/main /main
EXPOSE 8080
CMD ["/main"]
