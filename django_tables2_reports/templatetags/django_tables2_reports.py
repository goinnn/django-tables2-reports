# -*- coding: utf-8 -*-
# Copyright (c) 2012 by Pablo Martín <goinnn@gmail.com>
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

from django import template

register = template.Library()


@register.filter
def strip(value):
    return value.strip()


@register.filter
def remove_line_breaks(value):
    value = value.replace('\r\n', '\n')
    value = ' '.join([strip(line) for line in value.split('\n') if line])
    return value


class IsStringNode(template.Node):
    """Implements a node to provide an if the current variable is instance of basestring
    """
    @classmethod
    def handle_params(cls, parser, variable=None, tagname='ifstring'):
        end_tag = 'end%s' % tagname
        nodelist_true = parser.parse(('else', end_tag))
        token = parser.next_token()
        if token.contents == 'else':  # there is an 'else' clause in the tag
            nodelist_false = parser.parse((end_tag, ))
            parser.delete_first_token()
        else:
            nodelist_false = ""
        if isinstance(variable, basestring):
            variable = template.Variable('"%s"' % variable)
        return cls(variable, nodelist_true, nodelist_false)

    @classmethod
    def handle_token(cls, parser, token, tagname='ifstring'):
        bits = token.contents.split()
        if len(bits) not in (2, 3):
            raise template.TemplateSyntaxError(
                "'%s' tag takes one or two arguments" % bits[0])
        variable = bits[1]
        if '"' in variable or "'" in variable:
            variable = variable.replace('"', '').replace("'", "")
        else:  # this is a variable
            variable = parser.compile_filter(variable)
        return cls.handle_params(parser, variable, tagname)

    def __init__(self, variable, nodelist_true, nodelist_false):
        self.variable = variable
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false

    def render(self, context):
        variable = self.variable.resolve(context)
        if isinstance(variable, basestring):
            return self.nodelist_true.render(context)
        else:
            if self.nodelist_false:
                return self.nodelist_false.render(context)
        return ''


@register.tag
def ifstring(parser, token):
    """This function provides functionality for the 'ifstring' template tag.
    Usage::
      {% ifstring x %} foo {% else %} bar {% endifstring %}
    """
    return IsStringNode.handle_token(parser, token)
