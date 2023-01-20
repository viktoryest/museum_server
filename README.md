# Museum Server  
The Django server is used for the museum exhibition and 
implements interaction between apps on the tablet and 
web apps. 
## Installation
Install requirements:  
```shell
pip install -r requirements.txt
```  
Apply migrations:  
```shell
python manage.py migrate
```
Run server:  
```shell
python manage.py runserver
```
From [Django Documentation](https://docs.djangoproject.com/en/4.1/ref/django-admin/#:~:text=Note%20that%20the%20default%20IP%20address%2C%20127.0.0.1%2C%20is%20not%20accessible%20from%20other%20machines%20on%20your%20network.%20To%20make%20your%20development%20server%20viewable%20to%20other%20machines%20on%20the%20network%2C%20use%20its%20own%20IP%20address%20(e.g.%20192.168.2.1)%2C%200%20(shortcut%20for%200.0.0.0)%2C%200.0.0.0%2C%20or%20%3A%3A%20(with%20IPv6%20enabled).):  
>Note that the default IP address, 127.0.0.1, is not accessible 
from other machines on your network. To make your development 
server viewable to other machines on the network, use its own IP
address (e.g. 192.168.2.1), 0 (shortcut for 0.0.0.0), 0.0.0.0, 
>or :: (with IPv6 enabled).

Example:  
```shell
python manage.py runserver 0.0.0.0:8000
```
To use Django admin panel, you should create superuser:
```shell
python manage.py createsuperuser
```
and follow instructions.  

After that, you can sign in and use admin panel (IP adress and
the port are example, please, replace them on your own):
http://0.0.0.0:8000/admin/

You can see automatic documentation on 
http://127.0.0.1:8000/swagger/