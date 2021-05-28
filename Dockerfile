# This Dockerfile runs a Python 3 program in /app as the user 'appuser'
# instead of root. Java is available via OpenJDK 15.
# Usage: docker build -f Dockerfile .

# Alpine + OpenJDK
FROM openjdk:15-jdk-alpine3.12 AS base

# Inputs and Constants
ARG PYTHON_VERSION='3.9.1'

# Upload the current directory and its subdirectories containing
# your Python source code) to /app. This command ignores files and
# directories per the .dockerignore file in the current directory.
WORKDIR /app
COPY . .

# Update Alpine
RUN apk --update upgrade

# Install Alpine packages
RUN apk add --no-cache \
  bash \
  build-base \
  bzip2-dev \
  ca-certificates \
  curl `# Needed by pyenv and for monitoring` \
  git `# Needed by pyenv` \
  libffi-dev \
  libxslt-dev \
  linux-headers \
  ncurses-dev \
  openssl-dev \
  readline-dev \
  sqlite-dev 

# Run the Python program using the user and group 'appuser' (uid=1001, gid=1001)
RUN addgroup -g 1001 -S appuser && adduser -u 1001 -S appuser -G appuser
RUN chown -R appuser:appuser .
USER appuser 

# Set runtime environment variables
ENV HOME /app
ENV PYENV_ROOT $HOME/.pyenv
ENV PYTHON_VERSION $PYTHON_VERSION
ENV PATH $PYENV_ROOT/shims:$PATH:$PYENV_ROOT/bin

# This is a build-time environment variable that should not be needed in later
# versions of Python
ENV CRYPTOGRAPHY_DONT_BUILD_RUST 1

# Install pyenv
RUN curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer \
  -o pyenv-installer && \
  /bin/bash pyenv-installer && \
  rm pyenv-installer
  
# Install Python via pyenv
RUN pyenv install $PYTHON_VERSION
RUN pyenv global $PYTHON_VERSION # Not sure this is needed
RUN pyenv rehash # Not sure this is needed

# Install your Python application
RUN make install

# Remove Alpine packages that are not needed at runtime
USER root
RUN apk del \
  build-base \
  git \
  linux-headers
USER appuser

# Modify the following to start your Python application
CMD ["python3", "-m", "main.py"]