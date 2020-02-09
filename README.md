# Home Automation API

A collection of my private API endpoints to control my home. As this is so unique to my home, this is not designed to 
be a re-usable product. This is open sourced purely so that others might take inspiration or knowledge for their projects.

*API endpoints:*
- Turn on/off RF controlled lights
- Turn off an LG WebOS smart TV

# Installation
1) Install Raspbian on a Raspberry PI
2) `git clone https://github.com/alexluckett/home-automation-api.git -b master --single-branch ~/home_api`
2) `sudo ~/home_api/install_api.sh`
3) `nohup ~/home_api/start_api.sh &`

##git clone user@git-server:project_name.git -b branch_name --single-branch /your/folder

As of 3, API is started and running in the background. Create a service and start the 3 on boot if needed.