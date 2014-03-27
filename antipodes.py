from pandas import read_fwf
from pyproj import Proj, transform
from numpy import vstack
from sklearn.neighbors import NearestNeighbors

# calculate lat & lon antipode
def antipode(lon, lat):
    newlat = -1*lat
    if lon > 0:
        newlon = lon - 180
    else:
        newlon = lon + 180
    return (newlon, newlat)

# see http://www.wunderground.com/about/faq/international_cities.asp
# for data specs
stations = read_fwf('data/station_list', header=None,
                widths = [26, 7, 5, 11, 9, 5, 5],
                names = ['Station', 'Country', 'ID', 'Lat',
                         'Lon', 'Elev', 'WMO'])
locs = stations[['Lon', 'Lat']].values

# project into equirectangular, centered on antipode of each station
p1 = Proj({'proj':'longlat', 'datum':'WGS84'})

# indices of antipodes
antipodes = []

for i in range(len(stations)):
    print i
    station = stations.iloc[i]
    
    # project antipode
    ant = antipode(station['Lon'], station['Lat'])
    p2 = Proj({'proj': 'eqc', 'lon_0': ant[0]})
    ant = transform(p1, p2, ant[0], ant[1])
    
    # project other points
    points = vstack(transform(p1, p2, locs[:,0], locs[:,1])).T
    nbrs = NearestNeighbors(n_neighbors = 5,
            algorithm='ball_tree').fit(points)
    
    distances, indices = nbrs.kneighbors(ant)
    distances = distances[0]
    indices = indices[0]
    
    ixs = indices[distances < 150000]
    for ix in ixs:
        if [i, ix] not in antipodes and [ix, i] not in antipodes:
            antipodes.append([i, ix])
