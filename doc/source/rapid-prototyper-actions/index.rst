SCADE Rapid Prototyper Actions
=====================


Execute SCADE Rapid Prototyper command line tools on models.



Generate configuration
----------------------

.. jinja:: rapid-prototyper-generate

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

