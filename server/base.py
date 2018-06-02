import aiohttp_jinja2


class Controllers(object):
    def __init__(self, mongo):
        self.mongo = mongo
        self.db = mongo['gbf']
        self.render = aiohttp_jinja2.render_template
