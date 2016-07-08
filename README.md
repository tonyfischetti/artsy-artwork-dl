artsy-artwork-dl
=================

This is a script that takes the URL of an art piece from
[artsy.net](http://www.artsy.net),
downloads the image of the artwork and renames the downloaded file
to follow a filename template (given as a CLI arg) based on the
artist's name, the title of the piece, and the date of
completion.

usage
-----
The two command line arguments are the URL to the artwork on artsy
and the string that describes what to name the file of the downloaded
image.

The formatting string is allowed to be anything the can be a valid filename
on your system. Additionally, there are three format specifiers that are
allowed:
- `%a`   which will be replaced with the name of the artist
- `%t`   which will be replaced with the title of the piece
- `%d`   which will be replaced with the date of the piece

For example, if we wanted to download an image of the
[Fountain](https://en.wikipedia.org/wiki/Fountain_(Duchamp)),
and have the file automatically named:
`Marcel Duchamp - Fountain - 1917.jpg`,
we can use the following command...

```
python artsy-dl.py "https://www.artsy.net/artwork/marcel-duchamp-fountain-1" "%a - %t - %d"
```

This script also has support for placing the images in directories. For
example, if we wanted to download an image of
[this piece](https://www.artsy.net/artwork/kay-sage-white-silence), and
place it in a directory called `Kay Sage paintings` (even if the directory
doesn't exist yet) and name it `White Silence (1941)`, we can do...

```
python artsy-dl.py "https://www.artsy.net/artwork/kay-sage-white-silence" "%a paintings/%t (%d)"
```

You can nest directories as well; let's say we wanted to download a bunch of
images of [James Turrell's](https://www.artsy.net/artist/james-turrell) work
and we wanted to organize it by year...

```
python artsy-dl.py "https://www.artsy.net/artwork/james-turrell-prado-white" "%a/%d/%t"
python artsy-dl.py "http://www.artsy.net/artwork/james-turrell-raethro-green-1" "%a/%d/%t"
python artsy-dl.py "https://www.artsy.net/artwork/james-turrell-sloan-red-1" "%a/%d/%t"
```

This created a directory called `James Turrell` and two subdirectories,
`1968` and `1967` because two of the pieces were done in the same year.



requirements
------------
- python (tested with 2.7 and 3.4)

And the following python modules
- html2text
- lxml
- requests
- wget (python module)
