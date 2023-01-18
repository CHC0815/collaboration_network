import json
from itertools import  combinations
from pyvis.network import Network
from flashgeotext.geotext import GeoText

ignore = ["University", "Ferderal"]

# edge -> weight
graph = {}
all_cities = set()
net = None
geotext = GeoText()


def load_data():
    with open('myPapers.json', 'r') as f:
        data = json.load(f)
    return data

def add_to_graph(record):
    cities = get_cities(record)
    all_cities.update(cities)
    if len(cities) <= 0:
        return # something went wrong
    if len(cities) == 1:
        # insert_edge(cities[0], cities[0])
        pass # no self loops
    else:
        # get all combinations and insert edge
        combs = combinations(cities, 2)
        for combination in combs:
            insert_edge(list(combination)[0], list(combination)[1])


def insert_edge(cityA, cityB):
    # sort citites in alphabetical order 
    if cityB < cityA:
        cityA, cityB = cityB, cityA
    key = f"{cityA}~{cityB}"
    if not key in graph:
        graph[key] = 0
    graph[key] += 1

# get collaborating cities in this record
def get_cities(record) -> list[str]:
    cities = set()
    affiliations = record["AD"]
    for aff in affiliations:
        # try:
        #     city = aff.split(',')[2] # get city out of affiliation string
        #     city = city.lstrip().rstrip()
        #     city = city.replace(".", "")
        #     cities.add(city)
        # except:
        #     pass # ignore
        result = geotext.extract(input_text = aff)
        if not "cities" in result:
            continue
        for city in result['cities']:
            if city in ignore:
                continue
            cities.add(city)
    return list(cities)

def gen_network():
    global net
    net = Network(height="750px", width="100%",
        bgcolor="#222222",
        font_color="white",
        select_menu=True,
        filter_menu=True
    )

    # net.add_nodes(all_cities)
    for city in all_cities:
        net.add_node(city, label=city)
    
    for edge in graph:
        cityA = edge.split('~')[0]
        cityB = edge.split('~')[1]
        weight = graph[edge]
        net.add_edge(cityA, cityB, weight=weight)
        net.add_edge(cityB, cityA, weight=weight)

def show_network():
    net.toggle_physics(True)
    net.show("graph.html")


def main():
    data = load_data()
    for record in data:
        add_to_graph(record)

    json.dump(graph, open("graph.json", "w"))

    gen_network()
    show_network()


if __name__ == "__main__":
    main()