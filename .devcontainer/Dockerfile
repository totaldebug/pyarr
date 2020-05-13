FROM python:latest

RUN apt update

RUN apt upgrade  -y

RUN apt install zsh -y

RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python && source
ENV PATH="/root/.poetry/bin:$PATH"

RUN wget https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh -O - | zsh || true

CMD ["zsh"]
