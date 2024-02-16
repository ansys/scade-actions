Tests actions
=============

The tests actions allow to run the test suite for a SCADE Python library.


Test library action
--------------------
This action runs the test suite for a Python library. This action accepts
markers, options, and post arguments to be passed to pytest before executing
the test session.

.. jinja:: scade-tests-pytest

    {{ description }}

    {{ inputs_table }}

    {{ outputs_table }}

Examples
++++++++

.. jinja:: scade-tests-pytest

     {% for filename, title in examples %}
     .. dropdown:: {{ title }}
        :animate: fade-in

        .. literalinclude:: examples/{{ filename }}
           :language: yaml

     {% endfor %}
