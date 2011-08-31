from webhelpers.paginate import Page as WHPage

def _makeurl(page):
    return '?page='+str(page)

class Page(WHPage):
    def __init__(self, *args, **kwargs):
        if 'url' not in kwargs:
            kwargs['url'] = _makeurl

        super(Page, self).__init__(*args, **kwargs)