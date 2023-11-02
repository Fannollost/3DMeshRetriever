import scipy as sp
import numpy as np
import csv
import open3d as o3d


def get_features(features_path, mesh_path):
    with open(features_path, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for i, row in enumerate(csv_reader):
            if i == 0:
                continue
            filepath = row[0] + "/" + row[1]
            if filepath == mesh_path:
                label = row[0]
                row.pop(0)
                row.pop(0)
                features = [float(feature.replace(" ", "")) for feature in row if feature != " "]
                return features, label
        else:
            raise RuntimeError(f"Mesh path {mesh_path} not found in mini-database.")


def get_all_features(features_path, exclude=None):
    total_features = []
    labels = []
    paths = []
    with open(features_path, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        
        for i, row in enumerate(csv_reader):
            if i == 0:
                continue # Skip header row
            filepath = row[0] + "/" + row[1]
            if exclude and filepath == exclude:
                continue # Exclude shape from returned features list if specified
            label = row[0]
            row.pop(0)
            row.pop(0)
            features = [float(feature.replace(" ", "")) for feature in row if feature != " "]
            total_features.append(features)
            labels.append(label)
            paths.append(filepath)
    
    return np.array(total_features), labels, paths


def load_meshes(meshpaths):
    # Load meshes
    meshes = []
    for i, meshpath in enumerate(meshpaths):
        mesh = o3d.io.read_triangle_mesh("normalisedDB/" + meshpath)
        mesh.compute_vertex_normals()

        # Add translation offset
        mesh.translate((i * 0.7 + int(i>0), 0, 0))
        meshes.append(mesh)

    return meshes


def visualize(meshes):
    o3d.visualization.draw_geometries(
        meshes,
        width=1280,
        height=720,
    )


def main():
    # Parameters
    query_path = "Bed/D00110.obj"
    features_path = "Max/miniDB/features.csv"
    features_pathOLD = "featuresnormalised.csv"
    k = 3

    # Load feature vector for query shape and db shapes
    query_features, query_label = get_features(features_pathOLD, query_path)
    features_total, labels, paths = get_all_features(features_pathOLD, exclude=query_path)

    # Build KDTree
    print("Building KDTree... ", end="")
    kdtree = sp.spatial.KDTree(features_total)
    print("Finished.")

    # Do query
    knn_distances, knn_indices = kdtree.query(query_features, k=k)
    print(
        f"{k} nearest neighbors for shape {query_path} (label='{query_label}'):\n",
        "\n".join([("    " + str(paths[i]) + f" (label='{labels[i]}', distance={dist})") for i, dist in zip(knn_indices, knn_distances)]),
        sep=""
    )

    # Visualize results
    meshes = load_meshes([query_path] + [paths[i] for i in knn_indices])
    visualize(meshes)


if __name__ == "__main__":
    main()
