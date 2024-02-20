Tests actions
=============

The tests actions allow to setup Python environments for SCADE and
run the test suite for a SCADE Python library.


Create SCADE Python virtual environment action
----------------------------------------------

.. jinja:: create-scade-venv

    {{ description }}

    {{ inputs_table }}

    {{ outputs_table }}

    Examples
    ++++++++

    {% for filename, title in examples %}
    .. dropdown:: {{ title }}
       :animate: fade-in

       .. literalinclude:: examples/{{ filename }}
          :language: yaml

    {% endfor %}


Test library action
--------------------
This action runs the test suite for a Python library and a given Python
interpreter. This action accepts markers, options, and post arguments to be
passed to pytest before executing the test session.

.. jinja:: tests-pytest

    {{ description }}

    {{ inputs_table }}

    {{ outputs_table }}

Examples
++++++++

.. jinja:: tests-pytest

     {% for filename, title in examples %}
     .. dropdown:: {{ title }}
        :animate: fade-in

        .. literalinclude:: examples/{{ filename }}
           :language: yaml

     {% endfor %}


SCADE Test library action
-------------------------
This action runs the test suite for a Python library and a given version of
Ansys SCADE. This action accepts markers, options, and post arguments to be
passed to pytest before executing the test session.

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
