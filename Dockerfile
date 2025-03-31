FROM martenseemann/quic-network-simulator-endpoint:latest AS builder

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
  apt-get install -y gnupg2 python3 python3-pip unzip

RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

RUN apt-get update && \
  apt-get install -y google-chrome-beta

RUN pip3 install selenium --break-system-packages

RUN wget -q "https://storage.googleapis.com/chrome-for-testing-public/$(google-chrome --version | awk '{print $3}')/linux64/chromedriver-linux64.zip" && \
  unzip chromedriver-linux64.zip && \
  mv chromedriver-linux64/chromedriver /usr/bin && \
  chmod +x /usr/bin/chromedriver && \
  rm chromedriver-linux64.zip

COPY run.py run_endpoint.sh /

ENTRYPOINT [ "/run_endpoint.sh" ]
