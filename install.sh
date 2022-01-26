#!/bin/bash
sudo yum update -y
wget https://github.com/JosefinDaniels/Trout-Cloud/blob/main/TroutScaper.py
sudo chmod +x TroutScaper.py
(crontab -l; echo "* * * * * python3 /home/splunker/TroutScraper.py") | sort -u | crontab -

