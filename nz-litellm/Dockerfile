FROM ubuntu:22.04
LABEL maintainer="nz-genesis"
WORKDIR /app
# example - no secrets here!
COPY ./entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["--help"]
