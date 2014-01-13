# Nagios plugings

## check_cert_expire.py

Simple check for seeing if an ssl cert is about to expire.

```
Usage: check_cert_expire.py [options] url 
Example: check_cert_expire.py -w 45 -p 4343 secure.example.com

Options:
  -h, --help            show this help message and exit
  -w WARN, --warn=WARN  Warn threshold in days [default: 30]
  -c CRITICAL, --critical=CRITICAL
                        Critical threshold in days [default: 15]
  -p PORT, --port=PORT  SSL port [default: 443]
```

If changing the default warn value remember that the critical value always needs to be lower (the script will exit with 1 if you attempt to do that).


