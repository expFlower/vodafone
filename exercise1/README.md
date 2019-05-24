
# Install Wordpress in Docker with Nginx and MariaDB

## Start-up

To get started, after you clone this repo, run `docker-compose up -d` and then visit http://localhost:8080/

Please note that we are using docker-compose file format 3.7, please ensure that your docker engine is at 18.06.0+ 

Please see [docker-compose file versions](https://docs.docker.com/compose/compose-file/compose-versioning/) for more details

#### Ports used:

`8080`: HTTP - redirects to HTTPs

`8443`: HTTPS - Supports both TLS v1.2 and v1.3

`3306`: Standard MySQL/ Maria DB

## Design notes:


#### Wordpress:

[Official docker wordpress:alpine image](https://docs.docker.com/samples/library/wordpress/) with all defaults.
This is alpine image of wordpress, used to keep the image size as small as possible
This image automatically populates the wp-config.php configuration. 

This is a base setup, if you indeed to run any live site using this setup you are **STRONGLY** advised to follow and 
implement [wordpress-hardening](https://wordpress.org/support/article/hardening-wordpress/)

I'd also strong recommending tuning PHP-FPM settings depending on your workload. 


#### Nginx:

[Official docker nginx:alpine image.](https://docs.docker.com/samples/library/nginx/) This is alpine image of wordpress,
 used to keep the image size as small as possible.
 
Nginx is configured with the following:

* Micro caching
* HTTPS enabled
* Redirect HTTP to HTTPS
* TLS only. Strong cyphers. 
See [Mozilla - ssl-config-generator](https://mozilla.github.io/server-side-tls/ssl-config-generator/)
* dhparam. 
See [Mozilla - Server_Side_TLS#DHE_handshake_and_dhparam](https://wiki.mozilla.org/Security/Server_Side_TLS#DHE_handshake_and_dhparam)
* OCSP configured but we only have self sign certs it is currently ignored.  
See [Mozilla - Server_Side_TLS#OCSP_Stapling](https://wiki.mozilla.org/Security/Server_Side_TLS#OCSP_Stapling) 

* HSTS enabled. See [Mozilla -Server_Side_TLS#HSTS:_HTTP_Strict_Transport_Security](https://wiki.mozilla.org/Security/Server_Side_TLS#HSTS:_HTTP_Strict_Transport_Security)
* Numerous HTTP header settings including:

  *`Strict-Transport-Security`HSTS (ngx_http_headers_module is required) (15768000 seconds = 6 months)*
  
  *`X-Content-Type-Options nosniff;` Prevents browsers from trying to "guess" MIME types and such, forcing them to use what the server tells them.*
   
  *`X-Frame-Options SAMEORIGIN;`Stops your site from being included in iframes on other sites*
 
  *`X-Xss-Protection "1" always;`Activates cross-scripting (XSS) protection in browsers.*
  
  *`Referrer-Policy same-origin;`Makes the site always send referrer information to other sites.*
  
  *`Content-Security-Policy "default-src 'self';";` Content to come from the site's own origin, trusted domains can be added if needed.*


A self-signed certificate was generated using the following:

`openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ./nginx-selfsigned.key -out ./nginx-selfsigned.crt -subj "/C=GB/ST=London/L=London/O=DemoCorp/OU=Org/CN=localhost"`


The dhparam key was generate using the following:

`openssl dhparam -out /etc/nginx/dhparam.pem 4096`


