import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from fastapi import APIRouter
from src.core.utils import Connector


router = APIRouter(
    prefix="/service",
    tags=["Service"],
    responses={404: {"description": "Not found"}},
)

def dijktra(response):
    nodes = []
    left = []
    right = []
    gas_price = []

    for service in response:
        nodes.append(service['kilometer'])
    
    for service in response:
        left.append(service['left'])

    for service in response:
        right.append(service['right'])

    for service in response:
        gas_price.append(service['gas_price'])

    for service in response:
        gas_price.append(service['right'])

    G=nx.Graph()

    for i in range(0,np.size(nodes)):
        G.add_node(nodes[i])

    for i in range(0,np.size(left)):
        G.add_weighted_edges_from([(left[i],right[i],gas_price[i])])

    pos=nx.shell_layout(G)

    nx.draw(G,pos,with_labels=True, node_color='white', edge_color='b', node_size=800, alpha=0.5)

    edge_labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels)
    plt.draw()
    plt.pause(1)
    plt.close()

    path=nx.dijkstra_path(G, source=start, target=end)
    return {"start": start, "end": end, "path":path}


@router.get("/service-area/{start}/{end}")
def read_root(start: str, end: str):
    header = {
            #If i need bearer token to connect
            #'Authorization': f'Bearer {APIKEY}'
            'Content-Type': 'application/json',
            'cache-control': 'no-cache',
        }
    connector = Connector(header, verify_ssl=False)
    response = connector.get('http://localhost:8000/api/adventure/servicearea/')
    return dijktra(response)

