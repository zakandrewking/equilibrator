eQuilibrator
============

The current online version of eQuilibrator can be found at:
http://equilibrator.weizmann.ac.il/

Dependencies:
- Django 1.6.2
- MySql 5.5
- PyParsing 1.5.7 (also 2.0.1 tested)
- NLTK 2.0.4
- NumPy and SciPy
- (optional) Indigo Toolkit (https://github.com/ggasoftware/indigo)

Setup
=====

To get started:

```
mysql.server start
mysql -u root -p
> GRANT ALL ON equilibrator.* TO 'equilibrator'@'localhost' IDENTIFIED BY 'password';
> CREATE DATABASE equilibrator;
```

Edit settings.py

```
./sqlload.sh
python manage.py runserver 8080
```