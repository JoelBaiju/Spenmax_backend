FROM python:3.11

ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app

COPY requirement.txt /app/
RUN pip install --no-cache-dir -r requirement.txt

COPY . /app/

CMD ["daphne", "-b", "0.0.0.0","-p" ,"8000", "backend.asgi:application"]


# FROM python:3.11

# ENV PYTHONUNBUFFERED 1
# RUN mkdir /app
# WORKDIR /app

# COPY requirement.txt /app/
# RUN pip install --no-cache-dir -r requirement.txt

# COPY . /app/

# RUN apt-get update && apt-get install -y nginx

# COPY nginx.conf /etc/nginx/nginx.conf

# CMD ["nginx", "-g", "daemon off;", "daphne", "-b", "0.0.0.0","-p" ,"8001", "backend.asgi:application"]  