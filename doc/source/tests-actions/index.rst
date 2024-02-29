Test actions
============

Test actions set up Python environments for SCADE and
run the test suite for a SCADE Python library.


Create a SCADE Python virtual environment
-----------------------------------------

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


Run the test suite for a Python library
---------------------------------------
The ``Run tests basic example`` action, which is derived from
``ansys/scade-actions/tests-pytest@main``, runs the test suite for
a Python library for either a given Python interpreter or given Ansys
SCADE version. This action accepts markers, options, and post arguments
to pass to ``pytest`` before executing the test session.

Run the test suite for a given Python interpreter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. jinja:: tests-pytest

    {{ description }}

    {{ inputs_table }}

    {{ outputs_table }}

Example
+++++++

.. jinja:: tests-pytest

     {% for filename, title in examples %}
     .. dropdown:: {{ title }}
        :animate: fade-in

        .. literalinclude:: examples/{{ filename }}
           :language: yaml

     {% endfor %}


Run the test suite for a given SCADE version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. jinja:: scade-tests-pytest

    {{ description }}

    {{ inputs_table }}

    {{ outputs_table }}

Example
+++++++

.. jinja:: scade-tests-pytest

     {% for filename, title in examples %}
     .. dropdown:: {{ title }}
        :animate: fade-in

        .. literalinclude:: examples/{{ filename }}
           :language: yaml

     {% endfor %}
