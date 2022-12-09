FROM ubuntu:latest
LABEL org.opencontainers.image.source https://github.com/airtai/nbdev-mkdocs

RUN apt update

# install security updates
RUN apt update --fix-missing --yes
RUN apt update -y && apt install --assume-yes unattended-upgrades git zip curl sudo wget vim fish \
  software-properties-common \
  && apt purge --auto-remove && apt clean && rm -rf /var/lib/apt/lists/*

# Enable unattended-upgrades
RUN dpkg-reconfigure --priority=low unattended-upgrades
# The above command will create a config file in /etc/apt/apt.conf.d/20auto-upgrades.
# Printing the contents of the configuration file. 
# If the configuration for Unattended-Upgrade is "1" then the unattended upgrade will run every 1 day. If the number is "0" then unattended upgrades are disabled.
RUN cat /etc/apt/apt.conf.d/20auto-upgrades

# Install node and npm
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && apt-get install -y nodejs \
    && apt purge --auto-remove && apt clean && rm -rf /var/lib/apt/lists/*

# Install and configure Python
## Install all necessary Python versions
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt install -y python3.7 python3.8 python3.9 python3.10
## Set Python 3.10 as default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 2
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 3
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 4
RUN update-alternatives --config python3
RUN python3 -V
## Install Python requirements
RUN apt install -y pip
COPY top_level_requirements.txt .
RUN python3 -m pip install --no-cache-dir -r top_level_requirements.txt && rm top_level_requirements.txt

RUN nbdev_install_quarto

# Install and configure jupyter notebook
RUN python3 -m pip install notebook
RUN python3 -m pip install jupyter_contrib_nbextensions

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

# Configure entrypoint and serve jupyter notebook
ENTRYPOINT []
COPY user_startup.sh /var
RUN chmod 777 /var/user_startup.sh
CMD ["/usr/bin/bash", "-c", "chown -R $USER /home/$USER && sudo -u $USER /var/user_startup.sh && sudo --preserve-env=\"$PRESERVE_ENVS\" -u $USER jupyter notebook --notebook-dir=/work --ip 0.0.0.0 --no-browser --allow-root"]

COPY set_bob_the_fish.sh /bin
RUN chmod 755 /bin/set_bob_the_fish.sh

# The below command will check and run upgrade only once while building
RUN unattended-upgrade --debug

