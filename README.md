List of New Zealand birds
=========================

[New Zealand Birds Online](http://nzbirdsonline.org.nz) 
is a comprehensive record of the bird species
that occur in New Zealand, including vagrant and extinct birds. This website
is a joint project between Te Papa, the Ornithological Society of New
Zealand, and the Department of Conservation. The common and scientific names may be considered to be reliable.

Using the list
----------------
The list is presented as a csv file, suitable for
opening with Excel, or loading into databases.

The list may be [downloaded as a zip
file](https://github.com/dragonfly-science/new-zealand-birds/archive/master.zip).
This file contains a csv file with a list of all the birds on 
[New Zealand Birds Online](http://nzbirdsonline.org.nz),
giving their common name, scientific name, status, and a link to the
corresponding web page. 

The script that was used to generate the list, and this help text, are also included
in the zip file.

Licence
-------
Thanks to Colin Miskelly, the principal curator of
[New Zealand Birds Online](http://nzbirdsonline.org.nz),
this list is released into public domain under a 
[CC0 licence](https://creativecommons.org/publicdomain/zero/1.0/). You are welcome
to use this list for whatever purpose you want.

Note that the other text, image, and media content on
[New Zealand Birds Online](http://nzbirdsonline.org.nz) is copyright, and 
only the species names and status information are released into the public domain.

Generating the list
--------------------
The csv file was generated from the
[New Zealand Birds Online](http://nzbirdsonline.org.nz) website by running the script 
`python3 nzbirdsonline_index.py`. This script depends on the web-scraping package `beautifulsoup4`.

