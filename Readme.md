#vnstat-pelican-control

This is 'just' a plugin for [Freifunk-Mainz/gatestats](https://github.com/Freifunk-Mainz/gatestats):

* `stat.py` connects to the gateways from `config.py`
* executes `vnstati` commands for specified interfaces
* downloads the images
* generates a new [pelican](http://getpelican.com) post
* runs pelican to create site
