# -*- coding: utf-8 -*-
from docutils import nodes
from docutils.parsers.rst import directives

def breakpoint(name, args, options, content, lineno, contentOffset, 
                                                     blockText, 
                                                     state, 
                                                     stateMachine):
    return [nodes.raw('', '<!--breakpoint-->', format='html')]

directives.register_directive('breakpoint', breakpoint)
