
from unittest import TestCase

from syncer import sync

from browser.API_VisJs import API_VisJs
from utils.Dev import Dev


class Test_API_Browser(TestCase):

    @sync
    async def setUp(self):
        self.api     = API_VisJs()
        self.url     = 'http://visjs.org/examples/network/basicUsage.html'
        if self.url != await self.api.browser.url():
            await self.api.browser.open(self.url)

    def test_add_node(self):
        node = { "id" : 'new_node',"label" : "an label" }
        self.api.remove_node(node['id'])        \
                .remove_node(node['id'])

    def test_add_edge(self):
        node_1 = { "id" : 'edge_1', "label" : "edge_1" }
        node_2 = {"id"  : 'edge_2', "label" : "edge_2" }
        (self.api.remove_nodes(['edge_1', 'edge_2'              ])
                  .add_nodes   ([node_1, node_2                 ])
                  .add_edge    ({'from':'edge_1', 'to':'edge_2' })
                  .remove_nodes(['edge_1', 'edge_2'             ]))

    def test_edges(self):
        edges = self.api.edges()
        data  = edges['_data']
        edge  = list(data.values())[0]
        assert edge['from'] == 1
        assert edge['to'  ] == 3

    def test_nodes(self):
        nodes = self.api.nodes()
        assert nodes['_data']['1'] == {'id': 1, 'label': 'Node 1'}

