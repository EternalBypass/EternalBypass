```
This guide is part of EternalBypass.
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```
#How to use NoVNC
##A guide for Linux
###Requirements:
NoVNC installed \
Certbot Installed \
Any VNC server

##Table of contents:
  - Installing and testing the tools
- Getting an domain
 - Getting a valid certificate
 - Using that certificate
 - Finished!

First, you will need to install [NoVNC](https://novnc.com/info.html). You will also need to install LetsEncrypts [Certbot](https://certbot.eff.org/), to create an certificate so that NoVNC will be encrypted.
And last, but not least you will need a VNC server. I used x11vnc, just because it was easy to set up. First, you need to make
sure that NoVNC will work in the first place. To test this, run `x11vnc --forever --usepw`. This will ask for a password to set. After that,
you will have an VNC server running on your machine on port 5900, if no other server is running, and nothing went wrong. After that, start
NoVNC by running `novnc`. It will give you an link to go to. Once there, just make sure it all works.

After all of this, you will need to get an domain. I would recomend noip.com because it is free, and any domain under .hopto.org is unblocked, 
at least at my school. With NoVNC, it will set up your current public IP to be the server for the domain. So now, you need to get an certificate. 
To do that, you need to run `sudo certbot certonly` and enter the requested details. After that, take not of where the certificate
is located. Now, you need to forward some ports. Forward your external port 443 to internal port 6080 to your computer. After this,
run NoVNC like so: `novnc --cert path/to/cert --key path/to/key`. And if all is done right, you can access your computer
from the domain from anywhere!