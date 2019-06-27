from scipy.spatial import distance as dist
def distance(a,b):
    pixelsPerMetric = None
    dist_roi= dist.euclidean(b,a)
    return dist_roi
