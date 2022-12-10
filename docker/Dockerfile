ARG BASE=ubuntu:latest
ARG PYTHON=3.10

#FROM ubuntu:latest
FROM ${BASE}
ARG PYTHON
LABEL org.opencontainers.image.source https://github.com/airtai/nbdev-mkdocs

RUN apt update

RUN if dpkg -l cuda-compat-11-2; then \
    apt-mark hold cuda-compat-11-2 cuda-cudart-11-2 cuda-nvtx-11-2 libcusparse-11-2 libnpp-11-2; \
    fi

# install security updates
RUN apt update --fix-missing --yes
RUN apt update -y && DEBIAN_FRONTEND=noninteractive apt install --assume-yes \
  apt-utils git zip curl sudo wget vim fish pip htop nano less wget \
  software-properties-common \
  && apt purge --auto-remove && apt clean && rm -rf /var/lib/apt/lists/*

RUN apt list --installed | grep nv

RUN echo continuing...

RUN apt update -y && apt upgrade -y

RUN apt list --installed | grep nv

RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update -y && DEBIAN_FRONTEND=noninteractive apt install --assume-yes \
  python3.7 \
  python3.8 \
  python3.9 \
  python3.10 \
  python3.11 \
  python3.7-distutils \
  python3.8-distutils \
  python3.9-distutils \
  python3.10-distutils \
  python3.11-distutils

## Set Python 3.9 as default
RUN python3 -m pip install --upgrade pip
RUN DEBIAN_FRONTEND=noninteractive apt install -y 
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 2
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 3
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 4
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 5
#RUN update-alternatives --config python3
RUN update-alternatives --set python3 /usr/bin/python${PYTHON}

RUN python3 -V
RUN python3 -m pip install --upgrade pip

RUN apt list --installed | grep nv

COPY top_level_requirements.txt .
RUN python3 -m pip install --no-cache-dir -r top_level_requirements.txt && rm top_level_requirements.txt

# Install node and npm
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && apt-get install -y nodejs \
    && apt purge --auto-remove && apt clean && rm -rf /var/lib/apt/lists/*

RUN nbdev_install_quarto

# Install and configure jupyter notebook
## Install and enable black python formatter for notebooks
RUN jupyter nbextension install https://github.com/drillan/jupyter-black/archive/master.zip \
    && jupyter nbextension enable jupyter-black-master/jupyter-black

## Install jupyter theme with airt theme
RUN python3 -m pip install --no-cache-dir git+https://github.com/airtai/jupyter-themes.git
EXPOSE 8888

## Customize your jupyter notebook
COPY airt-neg-trans-small.png /tmp
RUN chmod 644 /tmp/airt-neg-trans-small.png
COPY airt_favicons /tmp/airt_favicons
RUN chmod -R 755 /tmp/airt_favicons
# RUN jt -t airtd -cellw 90% -N -T --logo /root/airt-neg-trans-small.png --fav_icon_dir /root/airt_favicons
# RUN rm -rf /root/airt-neg-trans-small.png /root/airt_favicons

## Set default shell and home for jupyter notebook
ENV SHELL /usr/bin/bash

#RUN mkdir /work && mkdir /work/.config && chmod 777 /work && chmod 777 /work/.config
RUN mkdir /work && chmod 777 /work
# ENV HOME /work
WORKDIR /work

COPY nvtop-20.04 /usr/local/bin/nvtop

# Configure entrypoint and serve jupyter notebook
ENTRYPOINT []
COPY user_startup.sh /var
RUN chmod 777 /var/user_startup.sh
CMD ["/bin/bash", "-c", "chown -R $USER /home/$USER && sudo -u $USER /var/user_startup.sh && sudo --preserve-env=\"$PRESERVE_ENVS\" -u $USER jupyter notebook --ip 0.0.0.0 --no-browser --allow-root"]

COPY set_bob_the_fish.sh /bin
RUN chmod 755 /bin/set_bob_the_fish.sh

