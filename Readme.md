#vnstat-pelican-control

This is 'just' a plugin for [Freifunk-Mainz/gatestats](https://github.com/Freifunk-Mainz/gatestats):

* connects to the gateways from `config.py`
* executes `vnstati` commands for specified interfaces
* downloads the images
* generates a new [pelican](http://getpelican.com) post per gateway
* runs pelican to create site
