# Ubuntu image with all the required packages for using pyenv and its virtualenv plugin
FROM basavyr/ubuntu:latest

SHELL ["/bin/bash", "-c"]

ENV PYTHON_VERSION 3.8.6

# Set-up necessary Env vars for PyEnv
ENV PYENV_ROOT /root/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

# Install pyenv
RUN set -ex \
    && curl https://pyenv.run | bash \
    && pyenv update \
    && pyenv install $PYTHON_VERSION \
    && pyenv global $PYTHON_VERSION \
    && pyenv rehash

COPY /scripts/reader_entrypoint.sh .

COPY log-reader/dfcti_log_reader.py /exec/reader/
COPY log-reader/test_reader.py /exec/reader/
COPY log/reader/Pipfile /exec/reader/

RUN chmod +x entrypoint.sh

CMD ["./reader_entrypoint.sh"]
