Query actions
=============

The query actions allow for querying Ansys SCADE installations
and Python environments.


Get SCADE directory action
--------------------------

.. jinja:: get-scade-dir

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


Get SCADE Python version
------------------------

.. jinja:: get-scade-python

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
