SCADE Suite Actions
===================

Execute SCADE Suite command line tools on models.


Generate code
-------------

.. jinja:: suite-code

    {{ description }}

    {{ inputs_table }}

    {{ outputs_table }}

    Example
    +++++++

    {% for filename, title in examples %}
    .. dropdown:: {{ title }}
       :animate: fade-in

       .. literalinclude:: examples/{{ filename }}
          :language: yaml

    {% endfor %}

Check model
-----------

.. jinja:: suite-check

    {{ description }}

    {{ inputs_table }}

    {{ outputs_table }}

    Example
    +++++++

    {% for filename, title in examples %}
    .. dropdown:: {{ title }}
       :animate: fade-in

       .. literalinclude:: examples/{{ filename }}
          :language: yaml

    {% endfor %}

Create report
-------------

.. jinja:: suite-report

    {{ description }}

    {{ inputs_table }}

    {{ outputs_table }}

    Example
    +++++++

    {% for filename, title in examples %}
    .. dropdown:: {{ title }}
       :animate: fade-in

       .. literalinclude:: examples/{{ filename }}
          :language: yaml

    {% endfor %}
