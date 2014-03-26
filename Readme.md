#vnstat-pelican-control

This is 'just' a plugin for [Freifunk-Mainz/gatestats](https://github.com/Freifunk-Mainz/gatestats):

* connects to the gateways from `config.py`
* executes `vnstati` commands for specified interfaces
* downloads the images
* generates a new [pelican](http://getpelican.com) post per gateway
* runs pelican to create site

##command-line

This plugin now features a command-line interface, to enter a specific date:

The first flag specifies if you want to entry absolute values, or relative values. Use **a** and **r** for that.
If this one is omitted, relative values are assumed.

The second one replaces the the field from the current Date if **a** is used, or subtracts the given number from the current date (if **r** is used). Use **-d** for day, **-m** for month and **-y** for year.

###examples

Let's assume today is the *23.05.1942* (DD.MM.YYYY)

* generate posts for yesterday:
    * `python3 main.py r -d 1`
    * **22.05.1942**
    * or absolute:
        * `python3 main.py a -d 22`

* generate posts for the day before yesterday:
    * `python3 main.py r -d 2`
    * **21.05.1942**
    * or absolute:
        * `python3 main.py a -d 21`


* generate posts for the first day of the month:
    * `python3 main.py a -d 1`
    * **01.05.1942**
    * or relative:
        * `python3 main.py r -d 22`

* generate posts for this day last month:
    * `python3 main.py a -m 4`
    * **01.04.1942**
    * or relative:
        * `python3 main.py r -m 1`

Use `python3 main.py --help` for an overview
