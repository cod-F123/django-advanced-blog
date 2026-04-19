{% extends "mail_templated/base.tpl" %}

{% block subject %}
    Token verification
{% endblock subject %}

{% block html %}
    {{token}}
{% endblock html %}