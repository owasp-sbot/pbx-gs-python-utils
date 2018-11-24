import json

from syncer import sync

from browser.API_Browser import API_Browser


class API_VisJs():
    def __init__(self):
        self.browser = API_Browser()

    def add_nodes(self, nodes):
        for node in nodes:
            self.add_node(node)
        return self

    @sync
    async def add_node(self, node):
        method   = 'network.body.data.nodes.add'
        eval_str = '{0}({1})'.format(method,json.dumps(node))
        await self.browser.js_eval(eval_str)
        return self

    @sync
    async def add_edge(self, edge):
        method = 'network.body.data.edges.add'
        eval_str = '{0}({1})'.format(method, json.dumps(edge))
        await self.browser.js_eval(eval_str)
        return self

    def remove_nodes(self, ids):
        for id in ids:
            self.remove_node(id)
        return self
    @sync
    async def remove_node(self, id):
        method   = 'network.body.data.nodes.remove'
        eval_str = '{0}({1})'.format(method,json.dumps(id))
        await self.browser.js_eval(eval_str)
        return self

    @sync
    async def edges(self):
        return await self.browser.js_eval("edges")

    @sync
    async def nodes(self):
        return await self.browser.js_eval("nodes")
