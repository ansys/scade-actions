SCADE Display Actions
=====================


Execute SCADE Display command line tools on models.

Generate code
-------------

.. jinja:: display-code

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

.. jinja:: display-report

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
