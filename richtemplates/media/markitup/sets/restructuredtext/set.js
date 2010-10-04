// -------------------------------------------------------------------
// markItUp!
// -------------------------------------------------------------------
// Copyright (C) 2008 Jay Salvat
// http://markitup.jaysalvat.com/
// -------------------------------------------------------------------
// ReStructured Text
// http://docutils.sourceforge.net/
// http://docutils.sourceforge.net/rst.html
// -------------------------------------------------------------------
// Mark Renron <indexofire@gmail.com>
// http://www.indexofire.com
// -------------------------------------------------------------------
// Jannis Leidel <jannis@leidel.info>
// http://enn.io
// -------------------------------------------------------------------
// Based on django-markitup's boundled set
var INDENT = '    ';

mySettings = {
	nameSpace: 'ReST',
	previewParserPath:	'/markitup/preview/',
	onShiftEnter: {keepDefault:false, openWith:'\n\n'},
	onTab: {keepDefault:false, replaceWith:'    '},
	markupSet: [
		{name:'Level 1 Heading', key:'1', placeHolder:'Your title Here...', closeWith:function(markItUp) { return miu.markdownTitle(markItUp, '#'); } },
		{name:'Level 2 Heading', key:'2', placeHolder:'Your title here...', closeWith:function(markItUp) { return miu.markdownTitle(markItUp, '*'); } },
		{name:'Level 3 Heading', key:'3', placeHolder:'Your title here...', closeWith:function(markItUp) { return miu.markdownTitle(markItUp, '='); } },
		{name:'Level 4 Heading', key:'4', placeHolder:'Your title here...', closeWith:function(markItUp) { return miu.markdownTitle(markItUp, '-'); } },
		{name:'Level 5 Heading', key:'5', placeHolder:'Your title here...', closeWith:function(markItUp) { return miu.markdownTitle(markItUp, '^'); } },
		{name:'Level 6 Heading', key:'6', placeHolder:'Your title here...', closeWith:function(markItUp) { return miu.markdownTitle(markItUp, '"'); } },
		{separator:'---------------' },
		{name:'Bold', key:'B', openWith:'**', closeWith:'**', placeHolder:'Input Your Bold Text Here...'},
		{name:'Italic', key:'I', openWith:'`', closeWith:'`', placeHolder:'Input Your Italic Text Here...'},
		{separator:'---------------' },
		{name:'Bulleted List', openWith:'- ' },
		{name:'Numeric List', openWith:function(markItUp) { return markItUp.line+'. '; } },
		{separator:'---------------' },
		{name:'Picture', key:'P', openWith:'.. image:: ', placeHolder:'Link Your Images Here...'},
		{name:'Link', key:"L", openWith:'`', closeWith:'`_ \n\n.. _`Link Name`: [![Url:!:http://]!]', placeHolder:'Link Name' },
		{name:'Quotes', openWith:'    '},
		//{name:'Code', openWith:'\n:: \n\n	 '},
		{name:'Code', openWith:'\n.. code-block:: python \n\n    '},
        {name:'Indent', className:'indent', replaceWith: function(markItUp) { return miu.indentText(markItUp); } },
        {name:'Dedent', className:'dedent', replaceWith: function(markItUp) { return miu.dedentText(markItUp); } }
	]
};

// mIu nameSpace to avoid conflict.
miu = {
	markdownTitle: function(markItUp, character) {
		heading = '';
		n = $.trim(markItUp.selection||markItUp.placeHolder).length;
		for(i = 0; i < n; i++) {
			heading += character;
		}
		return '\n'+heading;
	},
    indentText: function(markItUp) {
        var splitted = markItUp['selection'].split('\n');
        var new_val = '';
        for (i=0; i<splitted.length; i++) {
            new_val += INDENT + splitted[i];
            if (i < splitted.length-1) new_val += '\n';
        }
        return new_val;
    },
    dedentText: function(markItUp) {
        var splitted = markItUp['selection'].split('\n');
        var new_val = '';
        var can_dedent = true;
        for (i=0; i<splitted.length; i++){
            var line = splitted[i];
            var firstpart = line.substring(0, INDENT.length);
            if (line !== '' && firstpart !== INDENT){
                console.log('line: ' + line);
                console.log('subs: ' + firstpart);
                can_dedent = false;
            }
            new_val += line.substring(INDENT.length, line.length);
            if (i < splitted.length-1) new_val += '\n';
        }
        if (can_dedent)
            return new_val;
        else
            return markItUp['selection'];
    }
};

