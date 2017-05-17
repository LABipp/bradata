bradata
#######

bradata means to make easily available **all** Brazilian government data
as a Python package.

it should be as symple as:

.. code-block:: python

    import bradata

    bradata.inep.enem.get()

and you should have all ENEM microdata in your ``/bradata\_download`` 
directory.\*

documentation is available at
`http://bradata.readthedocs.io/ <http://bradata.readthedocs.io/>`_.

\* except the ENEM module is not ready. we have a lot of work to do, and we 
would love to have contributors!

status
======

this package is in the early stages of development. the only modules we have so 
far are those that download data from:

- Tribunal Superior Eleitoral (TSE)

- Controladoria-Geral da União (CGU)

- Infraero

of which none are complete so far.

contributing
============

if you wish to contribute, check the issues. all issues are labeled by
difficulty (beginner, intermediate and advanced).

there is a list of possible data sources in
``menu-de-dados.csv``.

everything you do is yours -- it should be licensed under your own name.

check the contributing guidelines (at ``CONTRIBUTING.rst``). pull requests
not following the guidelines won't be accepted.

if you have any doubts, contact @odanoburu or @joaocarabetta (project
maintainers).

License
=======

MIT license available at ``LICENSE.txt``.

Note
----

This project has been set up using PyScaffold 2.5.7. For details and
usage information on PyScaffold see
`here <http://pyscaffold.readthedocs.org/>`_.
