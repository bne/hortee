======
hortee
======

Django application for tracking plants over time

Build
=====

::

  sudo aptitude install python-setuptools
  git clone git://github.com/bne/hortee.git
  cd hortee/
  ./configure
  python bootstrap.py
  bin/buildout
  touch data/hortee.db
  bin/django syncdb

Develop
=======

::

  bin/django test
  bin/django runserver

etc...







