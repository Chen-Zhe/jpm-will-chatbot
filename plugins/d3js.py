from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings


class D3visualizationPlugin(WillPlugin):

    @route("/d3draw")
    @rendered_template("d3.html")
    def renderD3(self):
        return {}
