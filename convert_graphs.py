from pathlib import Path

import networkx as nx

MOVIE_FOLDER = Path("./brain_networks/movie/")
STORY_FOLDER = Path("./brain_networks/story/")
DEST_FOLDER = Path("./graphs/")


# vis = vcat(0:8, 50:57) .+ 1
# somot = vcat(9:14, 58:65) .+ 1
# dorsattn = vcat(15:22, 66:72) .+ 1
# ventattn = vcat(23:29, 73:77) .+ 1
# limbic = vcat(30:32, 78:79) .+ 1
# control = vcat(33:36, 80:88) .+ 1
# default = vcat(37:49, 89:99) .+ 1
def node_location(node: int) -> str:
    if 1 <= node <= 9 or 51 <= node <= 58:
        return "vis"
    elif 10 <= node <= 15 or 59 <= node <= 66:
        return "somot"
    elif 16 <= node <= 23 or 67 <= node <= 73:
        return "dorsattn"
    elif 24 <= node <= 30 or 74 <= node <= 78:
        return "ventattn"
    elif 31 <= node <= 33 or 79 <= node <= 80:
        return "limbic"
    elif 34 <= node <= 37 or 81 <= node <= 89:
        return "control"
    elif 38 <= node <= 50 or 90 <= node <= 100:
        return "default"
    raise ValueError(f"Invalid node: {node}")


def load_graph_from_txt(file_path: str) -> list[nx.Graph]:
    graphs = [nx.Graph() for _ in range(8)]

    with open(file_path, "r") as f:
        f.readline()
        for line in f:
            data = line.split()

            n1, n2 = int(data[0]), int(data[1])
            time = int(data[2])
            weight = float(data[3])

            G = graphs[time - 1]

            # Check if the edge already exists
            if G.get_edge_data(n1, n2, default=None) is not None:
                continue

            G.add_node(n1, area=node_location(n1))
            G.add_node(n2, area=node_location(n2))
            G.add_edge(n1, n2, weight=weight)

    return graphs


def convert_grpahs(graphs_files: list[Path], _type: str):
    for file in graphs_files:
        print(f"Processing {file}")
        graphs = load_graph_from_txt(str(file))
        for i, G in enumerate(graphs):
            user_id = int(file.stem.split("_")[0])
            nx.write_gexf(G, f"{DEST_FOLDER}/{_type}_{user_id:03d}_{i + 1}.gexf")


def convert_all():
    DEST_FOLDER.mkdir(parents=True, exist_ok=True)
    convert_grpahs(list(MOVIE_FOLDER.iterdir()), "m")
    convert_grpahs(list(STORY_FOLDER.iterdir()), "s")


def main():
    convert_all()


if __name__ == "__main__":
    main()
