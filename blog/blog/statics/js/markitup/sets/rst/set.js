// -------------------------------------------------------------------
// markItUp!
// -------------------------------------------------------------------
// Copyright (C) 2008 Jay Salvat
// http://markitup.jaysalvat.com/
// -------------------------------------------------------------------
// MarkDown tags example
// http://en.wikipedia.org/wiki/Markdown
// http://daringfireball.net/projects/markdown/
// -------------------------------------------------------------------
// Feel free to add more tags
// -------------------------------------------------------------------

mySettings = {
    nameSpace: 'ReST',
    // previewParserPath: '/posts/preview',
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
        {name:'Code', openWith:'\n.. code-block:: [![Language:!:]!]\n\n    '},
        // {name:'Preview', className:'preview', call:'preview'}
        {name:'Preview', className:'preview', 
         beforeInsert:function(markItUp) { 
                var a = $('<form id="preview" method="POST" target="previewpp" action="/posts/preview"><textarea name="content">'+markItUp.textarea.value+'</textarea></form>');
                $('#bobafett').html(a);
                $('#preview').submit();
            } 
        },
        {separator:'---------------' },
        {name:'Break Point', className:'breakpoint', openWith:'.. breakpoint::\n'},
        {name:'Video from Youtube', className:'youtube', openWith:'.. youtube:: [![Code (?v=<code>):!:]!]\n'},
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
    }
};
