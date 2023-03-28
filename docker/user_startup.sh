#!/usr/bin/bash

jt -t airtd -cellw 90% -N -T  --logo /tmp/AIRT_logo_blue_white.png --fav_icon_dir /tmp/airt_favicons

jupyter nbextension install https://github.com/airtai/jupyter-docstring-gen/archive/main.zip --user

jupyter nbextension enable jupyter-black-master/jupyter-black
jupyter nbextension enable jupyter-docstring-gen-main/jupyter-docstring-gen

