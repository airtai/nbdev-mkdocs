FROM ubuntu:latest
RUN apt update

# Add software-properties-common for add-apt-repository
RUN apt install -y software-properties-common

# Install git
RUN apt install git -y

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

# Install and configure jupyter notebook
RUN python3 -m pip install notebook
RUN python3 -m pip install jupyter_contrib_nbextensions
RUN mkdir /notebooks
EXPOSE 8888
## Install and enable black python formatter for notebooks
RUN jupyter nbextension install https://github.com/drillan/jupyter-black/archive/master.zip \
    && jupyter nbextension enable jupyter-black-master/jupyter-black
## Install jupyter theme with airt theme
RUN python3 -m pip install --no-cache-dir git+https://github.com/airtai/jupyter-themes.git
## Customize your jupyter notebook
COPY airt-neg-trans-small.png /root
COPY airt_favicons /root/airt_favicons
RUN jt -t airtd -cellw 90% -N -T --logo /root/airt-neg-trans-small.png --fav_icon_dir /root/airt_favicons
RUN rm -rf /root/airt-neg-trans-small.png /root/airt_favicons
## Set default shell and home for jupyter notebook
ENV SHELL /usr/bin/bash
ENV HOME /root
WORKDIR /notebooks

# Configure entrypoint and serve jupyter notebook
ENTRYPOINT []
CMD ["/usr/bin/bash", "-c", "jupyter notebook --notebook-dir=/notebooks --ip 0.0.0.0 --no-browser --allow-root"]
