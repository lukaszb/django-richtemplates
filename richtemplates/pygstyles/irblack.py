# -*- coding: utf-8 -*-
"""
    Ir_Black Colorscheme
    ~~~~~~~~~~~~~~~~~~~~

    Converted by Vim Colorscheme Converter
"""
from pygments.style import Style
from pygments.token import Token, Comment, Name, Keyword, Generic, Number, Operator, String

class IrBlackStyle(Style):

    background_color = '#000000'
    styles = {
        Comment:            'noinherit #7C7C7C',
        Comment.Preproc:    'noinherit #96CBFE',

        Operator.Word:      'noinherit #ffffff',

        String:             'noinherit #A8FF60',

        Number:             'noinherit #FF73FD',

        Keyword:            'bold #6699CC',
        Keyword.Type:       'noinherit #FFFFB6',

        Name.Constant:      'noinherit #99CC99',
        Name.Variable:      'noinherit #C6C5FE',
        Name.Function:      'noinherit #FFD2A7',
        Name.Tag:           'noinherit #6699CC',
        Name.Entity:        'noinherit #E18964',
        Name.Attribute:     'noinherit #FFD2A7',

        Generic.Output:     'noinherit #070707 bg:#000000',
        Generic.Heading:    'noinherit #f6f3e8 bold',
        Generic.Subheading: 'noinherit #f6f3e8 bold',
        Generic.Traceback:  'noinherit #ffffff bg:#FF6C60 bold',
        Generic.Error:      'noinherit #ffffff bg:#ff0000',

        Token:              'noinherit #f6f3e8 bg:#000000',
    }
