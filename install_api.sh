echo "Updating pip"
apt update
apt install python-pip -y

echo "Installing core flask packages"
pip install Flask
pip install Flask-RESTful

echo "Installing API dependencies"
pip install pywebostv
pip install RPi.GPIO

