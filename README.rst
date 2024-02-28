Ansys SCADE actions
===================
|ansys| |CI-CD| |MIT|

.. |ansys| image:: https://img.shields.io/badge/Ansys-ffc107.svg?labelColor=black&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC
   :target: https://actions.scade.docs.pyansys.com/
   :alt: Ansys

.. |CI-CD| image:: https://github.com/ansys/scade-actions/actions/workflows/ci_cd.yml/badge.svg
   :target: https://github.com/ansys/scade-actions/actions/workflows/ci_cd.yml
   :alt: CI-CD

.. |MIT| image:: https://img.shields.io/badge/License-MIT-blue.svg
   :target: https://opensource.org/blog/license/mit
   :alt: MIT

.. readme_common_begins

A repository containing a collection of `GitHub Actions
<https://docs.github.com/en/actions>`_ to be
reused by projects in the Ansys SCADE ecosystem.

.. readme_common_ends

For more information on available actions and how to use them, see
`actions.scade.docs.pyansys.com <https://actions.scade.docs.pyansys.com>`_ .


Purpose
-------

The Ansys SCADE actions prepare a SCADE environment for executing tests.

They are driven by a Ansys SCADE version, such as ``23.1`` or ``24.1``,
instead of a Python version, such as ``3.7`` or ``3.10``.
