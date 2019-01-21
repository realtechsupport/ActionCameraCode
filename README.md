# ActionCameraCode
code examples and utilities for ART384 ActionCameraCode at Uni Buffalo, Spring 2019
Getting your Google VM started

Go to: https://console.cloud.google.com/education
Enter code. Redeem

At the console
https://console.cloud.google.com/home/dashboard


Create a project name
select project
navigation menu top left
compute engine
vm instance (wait a moment)
create

-name
-region / zone (US cheaper, lower latency)
-1vCPU
-boot disk -> Ubuntu 18.04LTS
-allow default access
-allow http and https traffic
-create

Then…create an ip address
Click on your instance name
Top menu – edit

Scroll down to network interfaces – edit (via pencil icon)
External  IP type

Reserve new static IP
Type a name

Go to dashboard
Go to compute engine
Click SSH

------------------------------------------------------------------------------------------------------------------------------
Install libraries on your server.

sudo apt update
sudo apt upgrade
sudo apt install python3 python3-dev
sudo apt install python3-pip
sudo pip3 install numpy
sudo apt-get install libsm6
sudo apt-get install libxrender1
sudo pip3 install opencv-python
sudo pip3 install matplotlib
sudo pip3 install Pillow
sudo pip3 install datetime
sudo pip3 install psutil
sudo apt install ffmpeg

go to cloud console VM instances… menu on right STOP

++ install gcloud
https://cloud.google.com/sdk/docs/quickstart-debian-ubuntu

1) curl https://sdk.cloud.google.com | bash
2) source ~/.bashrc
3) gcloud init

COPY FILES using gcloud copy procedure: gcloud compute scp
(issued on your local computer !)

++ from remote instance to local computer:
gcloud compute scp <instancename>:path_to_file local_destination
gcloud compute scp awayfromhome:/home/marcbohlen/data/dummy.txt /home/realtech/Desktop/

++ from local computer to remote instance (assuming troube in in your current dir)
gcloud compute scp file local_destination <user@instancename>:path
gcloud compute scp trouble.doc marcbohlen@awayfromhome:~/data/

 >> SSH in via console, setup your workspace
mkdir code
mkdir data
edit a file with nano:
nano filename
save: ctrl O
exit: ctrl X
exit session with ‘ctrl d’
-------------------------------------------------------------------------------------------------------------------------------
