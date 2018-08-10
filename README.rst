openedx-user-manager-api
========================

|pypi-badge| |travis-badge| |codecov-badge| |pyversions-badge| |license-badge|

openedx-user-manager-api is a Django app for providing a user-manager relationship API in Open edX.

Overview
--------

openedx-user-manager-api uses the pluggable django app pattern to ease installation.
To use in edx-platform, simply install the app into your virtualenv.

..code_block::

    $ pip install openedx-user-manager-api

License
-------

The code in this repository is licensed under the AGPL 3.0 unless
otherwise noted.

Please see ``LICENSE.txt`` for details.

Testing
-------

This package uses ``tox`` to run the tests against multiple combinations of python and django versions.

To run the the full test suite:

..code_block::

    $ mkvirtualenv venv
    $ make requirements
    $ make test-all


How To Contribute
-----------------

Contributions are very welcome.

Please read `How To Contribute <https://github.com/edx/edx-platform/blob/master/CONTRIBUTING.rst>`_ for details.

Even though they were written with ``edx-platform`` in mind, the guidelines
should be followed for Open edX code in general.

PR description template should be automatically applied if you are sending PR from github interface; otherwise you
can find it it at `PULL_REQUEST_TEMPLATE.md <https://github.com/open-craft/openedx-user-manager-api/blob/master/.github/PULL_REQUEST_TEMPLATE.md>`_

Issue report template should be automatically applied if you are sending it from github UI as well; otherwise you
can find it at `ISSUE_TEMPLATE.md <https://github.com/open-craft/openedx-user-manager-api/blob/master/.github/ISSUE_TEMPLATE.md>`_

Reporting Security Issues
-------------------------

Please do not report security issues in public. Please email help@opencraft.com.

Getting Help
------------

Have a question about this repository, or about Open edX in general?  Please
refer to this `list of resources`_ if you need any assistance.

.. _list of resources: https://open.edx.org/getting-help


.. |pypi-badge| image:: https://img.shields.io/pypi/v/openedx-user-manager-api.svg
    :target: https://pypi.python.org/pypi/openedx-user-manager-api/
    :alt: PyPI

.. |travis-badge| image:: https://travis-ci.org/open-craft/openedx-user-manager-api.svg?branch=master
    :target: https://travis-ci.org/open-craft/openedx-user-manager-api
    :alt: Travis

.. |codecov-badge| image:: http://codecov.io/github/edx/openedx-user-manager-api/coverage.svg?branch=master
    :target: http://codecov.io/github/open-craft/openedx-user-manager-api?branch=master
    :alt: Codecov

.. |pyversions-badge| image:: https://img.shields.io/pypi/pyversions/openedx-user-manager-api.svg
    :target: https://pypi.python.org/pypi/openedx-user-manager-api/
    :alt: Supported Python versions

.. |license-badge| image:: https://img.shields.io/github/license/open-craft/openedx-user-manager-api.svg
    :target: https://github.com/open-craft/openedx-user-manager-api/blob/master/LICENSE.txt
    :alt: License
