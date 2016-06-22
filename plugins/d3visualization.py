from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings


class D3visualization(WillPlugin):

    @route("/visualize/<graph_id>", method="GET")
    @rendered_template("d3.html")
    def renderD3(self, graph_id):

        return {"data": self.load(graph_id)}
