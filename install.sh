#!/bin/bash
sudo yum update -y
sudo pip3 install bs4
sudo pip3 install requests
wget https://raw.githubusercontent.com/JosefinDaniels/Trout-Cloud/main/TroutScaper.py
sudo chmod +x TroutScaper.py
(crontab -l; echo "* * * * * python3 /home/splunker/TroutScraper.py") | sort -u | crontab -

