# Templating syntax

## Jinja syntax

{{ [printing Python expression] }}

{% [non-printing Python expression] %}

{# [Comments] #}

### Expression syntax

|: Statements separator
~: String conversion and concatenation


### Statements

{% set [varname] = [value] %}
{% if ... %}
{% endif %}