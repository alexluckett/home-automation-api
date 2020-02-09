#!/bin/sh

echo -e "\n *** Updating pip"
apt update
apt install python-pip -y

echo -e "\n *** Installing core flask packages"
pip install Flask
pip install Flask-RESTful

echo -e "\n *** Installing API dependencies"
pip install -r ~/home_api/requirements.txt
