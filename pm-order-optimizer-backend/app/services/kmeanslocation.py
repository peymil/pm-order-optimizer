from sklearn.cluster import KMeans
from typing import List
from ..schemas.order_schemas import GroupedPoint, OrderSchema
from k_means_constrained import KMeansConstrained
from math import floor


def cluster_with_kmeans(points: List[OrderSchema], n_clusters: int) -> List[GroupedPoint]:
    kmeans = KMeans(
        init="k-means++",
        n_clusters=n_clusters,
        max_iter=300,
    ).fit(list(map(lambda point: (point.lon, point.lat), points)))
    labels = kmeans.labels_

    grouped_points = []

    for n in range(len(points)):
        grouped_point = GroupedPoint()
        grouped_point.x = points[n].lon
        grouped_point.y = points[n].lat
        grouped_point.group = labels[n]
        grouped_points.append(grouped_point)

    return grouped_points


def cluster_with_constrained_kmeans(points: List[OrderSchema], n_clusters: int) -> List[GroupedPoint]:
    kmeans = KMeansConstrained(
        n_clusters=n_clusters,
        size_min=floor(len(points) / n_clusters),
        size_max=floor(len(points) / n_clusters) + 2,
        random_state=0
    ).fit(list(map(lambda point: (point.lon, point.lat), points)))
    labels = kmeans.labels_
    grouped_points = []

    for n in range(len(points)):
        grouped_point = GroupedPoint()
        grouped_point.x = points[n].lon
        grouped_point.y = points[n].lat
        grouped_point.group = labels[n]
        grouped_points.append(grouped_point)

    return grouped_points
