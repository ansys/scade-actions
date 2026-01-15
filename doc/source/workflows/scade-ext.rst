GitHub Workflow for SCADE Python Extensions
###########################################

You can use the GitHub workflow for SCADE Python Extensions to develop a SCADE Python library,
for example `ansys-scade-apitools <https://github.com/ansys/scade-apitools>`_.
You can also use it to create an extension, such as a code generator wrapper or a SCADE IDE Python custom extension.

The workflow accepts inputs to specify repository properties used in jobs and options to deactivate a given job.

Inputs
======

.. list-table::
   :widths: 30 40 10 10 10
   :header-rows: 1

   * - **Name**
     - **Description**
     - **Type**
     - **Required**
     - **Default**
   * - documentation-cname
     - Documentation's CNAME, for example ``apitools.scade.docs.pyansys.com``.
     - String
     - True
     -
   * - library-name
     - Name of the library, for example ``ansys-scade-apitools``.
     - String
     - True
     -
   * - repository-name
     - Name of the repository, for example ``ansys/scade-apitools``.
     - String
     - True
     -
   * - main-python-version
     - Python version used for the workflow, unless specified otherwise.
     - String
     - False
     - ``"3.12"``
   * - build-wheelhouse-versions
     - List of Python versions as a JSON list.
     - String
     - False
     - ``"['3.10']"``
   * - scade-tests-versions
     - List of Ansys SCADE versions as a JSON list.
     - String
     - True
     - ``"['25.1']"``
   * - python-tests-os
     - List of OS versions as a JSON list.
     - String
     - True
     - ``"['ubuntu-latest']"``
   * - python-tests-versions
     - List of Python versions as a JSON list.
     - String
     - False
     - ``"['3.10']"``

.. Note::

    A Boolean ``dry-test`` input, ``false`` by default, verifies the workflow configuration. The jobs log a message instead of executing their actions.

Outputs
=======

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - **Name**
     - **Description**
   * - to-release
     - Returns ``true`` if the public release action should be executed at the end of the workflow; otherwise, it returns ``false``.

       **Note:** The returned value is always ``false`` for private repositories.

Secrets
=======

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - **Name**
     - **Description**
   * - PYANSYS_CI_BOT_TOKEN
     - Used to perform a git commit and push.
   * - PYANSYS_CI_BOT_USERNAME
     - Defines the user for a git commit and push.
   * - PYANSYS_CI_BOT_EMAIL
     - Defines the email for a git commit and push.
   * - CODECOV_TOKEN
     - Used to upload coverage reports to ``Codecov``.
   * - PYANSYS_PYPI_PRIVATE_PAT
     - Used to release library artifacts to the PyAnsys private index. It addresses private repositories only.

Permissions
===========

Some workflow jobs require ``read`` or ``write`` permissions.

.. list-table::
   :widths: 30 20 50
   :header-rows: 1

   * - **Name**
     - **Permission**
     - **Jobs**
   * - attestations
     - write
     - build-wheelhouse, build-library
   * - contents
     - read
     - labeler, build-wheelhouse, build-library
   * -
     - write
     - changelog-fragment, update-changelog, doc-deploy-pr
   * - id-token
     - write
     - build-wheelhouse, build-library, release
   * - pull-requests
     - write
     - build-wheelhouse, build-library, release

Control
=======

The workflow defines an optional Boolean input for each job to control its activation. This input is named ``skip-<job-name>``, for example, ``skip-build-wheelhouse``. The default value is ``false``.

Example
=======

.. code:: yaml

   dry-test:
     uses: ansys/scade-actions/.github/workflows/ci_cd_python_extensions.yml@main
     permissions:
       attestations: write
       contents: write
       id-token: write
       pull-requests: write
     with:
       documentation-cname: 'apitools.scade.docs.pyansys.com'
       library-name: 'ansys-scade-apitools'
       repository-name: 'scade-apitools'
       # actions not executed
       dry-test: true
     secrets: inherit

Jobs
====

The following table summarizes the jobs, their dependencies, and the actions that are used.
For more information, see the workflow itself: ``.github/workflows/scade-ext-workflow.yml``.

.. Note:: The table does not list common actions such as ``checkout`` or ``download-artifact``.

.. list-table::
   :widths: 30 40 40
   :header-rows: 1

   * - **Job**
     - **Dependencies**
     - **Actions**
   * - check-actions-security
     -
     - `ansys/actions/check-actions-security <https://actions.docs.ansys.com/version/stable/vulnerability-actions/#check-actions-security-action>`_
   * - pr-name
     - check-actions-security
     - `ansys/actions/check-pr-title <https://actions.docs.ansys.com/version/stable/style-actions/index.html#pull-request-title-action>`_
   * - labeler
     - pr-name
     - `micnncim/action-label-syncer <https://github.com/micnncim/action-label-syncer>`_

       `actions/labeler <https://github.com/actions/labeler>`_
   * - changelog-fragment
     - labeler
     - `ansys/actions/doc-changelog <https://actions.docs.ansys.com/version/stable/doc-actions/index.html#doc-changelog-action>`_
   * - code-style
     - pr-name
     - `ansys/actions/code-style <https://actions.docs.ansys.com/version/stable/style-actions/index.html#code-style-action>`_
   * - doc-style
     - pr-name
     - `ansys/actions/doc-style <https://actions.docs.ansys.com/version/stable/style-actions/index.html#doc-style-action>`_
   * - check-vulnerabilities
     - pr-name
     - `ansys/actions/check-vulnerabilities <https://actions.docs.ansys.com/version/stable/vulnerability-actions/#check-vulnerabilities-action>`_
   * - update-changelog
     - check-actions-security
     - `ansys/actions/doc-deploy-changelog <https://actions.docs.ansys.com/version/stable/doc-actions/index.html#doc-deploy-changelog-action>`_
   * - build-wheelhouse
     - code-style
     - `ansys/actions/build-wheelhouse <https://actions.docs.ansys.com/version/stable/build-actions/index.html#build-wheelhouse-action>`_
   * - scade-tests
     - build-wheelhouse
     - `ansys/scade-actions/scade-tests-pytest <https://actions.scade.docs.pyansys.com/version/stable/tests-actions/index.html#run-the-test-suite-for-a-given-scade-version>`_

       `codecov/codecov-action <https://github.com/codecov/codecov-action>`_
   * - python-tests (skipped by default)
     - build-wheelhouse
     - `ansys/actions/tests-pytest <https://actions.docs.ansys.com/version/stable/tests-actions/index.html#test-library-action>`_
   * - doc-build
     - doc-style
     - `ansys/actions/doc-build <https://actions.docs.ansys.com/version/stable/doc-actions/index.html#doc-build-action>`_
   * - doc-deploy-pr
     - doc-build
     - `ansys/actions/doc-deploy-pr <https://actions.docs.ansys.com/version/stable/doc-actions/index.html#doc-deploy-pr-action>`_
   * - build-library
     - python-tests, scade-tests, doc-build, check-vulnerabilities
     - `ansys/actions/build-library <https://actions.docs.ansys.com/version/stable/build-actions/index.html#build-library-action>`_
   * - release
     - build-library, update-changelog
     - `ansys/actions/release-pypi-private <https://actions.docs.ansys.com/version/stable/release-actions/index.html#release-pypi-private-action>`_

       `ansys/actions/release-github <https://actions.docs.ansys.com/version/stable/release-actions/index.html#release-github-action>`_
   * - doc-deploy-dev
     - build-library
     - `ansys/actions/doc-deploy-dev <https://actions.docs.ansys.com/version/stable/doc-actions/index.html#doc-deploy-dev-action>`_
   * - doc-deploy-stable
     - release
     - `ansys/actions/doc-deploy-stable <https://actions.docs.ansys.com/version/stable/doc-actions/index.html#doc-deploy-stable-action>`_
