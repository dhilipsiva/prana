# prana

 Loosely translated Sanskrit word for 'Energy'. Just another interview challenge.


## FYI

If any python guy is reviewing my code, I would just like to point out that I am using `pipenv` to manage dependencies and virtualenv & the all-new Pipfile. Just putting it out there if you are expecting a requirements.txt (which is replaced by Pipfile standard) :P

## prerequesites

Make sure you have `pipenv` installed.

## Development

1. Goto prana folder: `cd prana` (Very important)
1. Create a new Python 3 virtialenv `pipenv --three` (Make sure you `cd`ed into prana folder first)
1. To get into shell: `pipenv shell` (To activate virtualenv)
1. Install deps `pipenv install`
1. Install Development deps `pipenv install -d`
1. Test the code `pytest -v`

## Documentation

1. To auto-generate HTML docs from source, `make html` and open `_build/html/index.html` to view HTML docs
1. To auto-generate epub docs from source, `make epub` and open `_build/epub/prana.epub` to view epub docs
1. To auto-generate PDF docs from source, `make latexpdf` and open `_build/latex/prana.pdf` to view PDF docs
