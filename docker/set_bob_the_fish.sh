#!/usr/bin/fish

# setup Bob the fish
curl --insecure -L https://get.oh-my.fish > install_omf
chmod 777 install_omf
./install_omf --noninteractive
rm install_omf
echo omf install bobthefish | fish

set -Ux theme_powerline_fonts no
set -Ux theme_color_scheme terminal
set -Ux PATH . /home/davor/.local/bin $PATH

exec fish

