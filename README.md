artsy-artwork-dl
-----------------

This is a script that takes the URL of an artwork on artsy.net,
downloads the image, and then names the file consistently
using info about the artwork

This is a script that takes the URL of an art piece from artsy.net,
downloads the image of the artwork and renames the downloaded file
to follow a filename template (given as a CLI arg) based on the
artist's name, the title of the piece, and the date of
completion.

usage
=====
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
[Fountain](https://en.wikipedia.org/wiki/Fountain_(Duchamp\)),
and have the file automatically named:
`Marcel Duchamp - Fountain - 1917.jpg`,
we can use the following command...

```
python artsy-dl.py "https://www.artsy.net/artwork/marcel-duchamp-fountain-1" "%a - %t - %d"
```




requirements
============
- python (tested with 2.7 and 3.4)

And the following python modules
- html2text
- lxml
- requests
- wget (python module)
