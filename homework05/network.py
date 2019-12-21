import igraph
from api import get_friends, get_profileinfo
from igraph import Graph, plot
import numpy as np
import time

def get_network(users_ids, as_edgelist=True):
    # Создание вершин и ребер
    edges = []
    vertices = []
    sum = 0
    for i in range (len(users_ids)):
        time.sleep(0.4)
        usid = users_ids[i]
        qw = get_friends(usid, "id")
        try:
            profileinfo = get_profileinfo(usid)
            vertices.append(profileinfo['response'][0]['last_name'] + " " + profileinfo['response'][0]['first_name'])
        except:
            pass
        try:
            for j in range (qw['response']['count']):
                try:
                    manid = qw['response']['items'][j]['id']
                except:
                    continue
                for k in range (len(users_ids)):
                    if manid == users_ids[k]:
                        sum+=1
                        edges.append((i,k))
                        break
        except:
            pass
        if(sum==0):
            edges.append((i,i))
        else:
            sum=0
    # Создание графа

    g = Graph(vertex_attrs={"label":vertices},
        edges=edges, directed=False)

    # Задаем стиль отображения графа
    N = len(vertices)
    visual_style = {}
    visual_style["layout"] = g.layout_fruchterman_reingold(
        maxiter=1000,
        area=N**3,
        repulserad=N**3)

    g.simplify(multiple=True, loops=True)
    # Отрисовываем граф
    communities = g.community_edge_betweenness(directed=False)
    try:
        clusters = communities.as_clustering()
        pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
        g.vs['color'] = pal.get_many(clusters.membership)
    except:
        pass
    plot(g, **visual_style)

def plot_graph(graph):
    i=1
    # PUT YOUR CODE HERE


if __name__ == '__main__':
    ui = [991549,2183522,2350063,4939883,5397983,9416677,12889004,15159925,18634212,19806548,20910222,22586787,25848257,29656684,30052624,32271280,33986650,34831490,38064699,38567698,38729635,39047501,39380408,40604933,40742992,43391804,48060413,49899993,51477876,52085603,53926334,55684773,55751270,56442020,57353977,58893524,62941699,63531240,66592484,67117253,68523006,75696653,77860725,82175203,82640181,84213446,85671031,92407493,94035240,97551155,101273676,113873928,118900697,120055845,128228101,129034067,133518738,134360532,136137188,138532476,139900511,142079548,143127761,150572566,153929504,154752240,168900120,171494699,173393819,177858539,179208539,181692280,182809039,183313835,184642202,186282381,190310361,194963962,205140512,209092423,227441394,228147479,228274751,267857693,275641901,276265642,301237202,320696470,320848814,320899319,329072221,408107859,431090464,537477873,559574644]
    get_network(ui)
