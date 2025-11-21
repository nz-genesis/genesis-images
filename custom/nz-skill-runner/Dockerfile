FROM python:3.11-slim
LABEL maintainer="nz-genesis"
WORKDIR /app
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt || true
COPY . /app
ENTRYPOINT ["python", "-m", "nz_skill_runner"]
