FROM httpd:2.4.49
RUN apt install python-dev
RUN python -m pip install OPi.GPIO
COPY httpd.with-cgid.conf /usr/local/apache2/conf/httpd.conf
