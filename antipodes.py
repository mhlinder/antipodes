from pandas import read_fwf
from pyproj import Proj, transform
from numpy import vstack
from sklearn.neighbors import NearestNeighbors

# calculate lat & lon antipode
def antipode(lat, lon):
    newlat = -1*lat
    if lon > 0:
        newlon = lon - 180
    else:
        newlon = lon + 180
    return (newlat, newlon)

# see http://www.wunderground.com/about/faq/international_cities.asp
# for data specs
stations = read_fwf('data/station_list', header=None,
                widths = [26, 7, 5, 11, 9, 5, 5],
                names = ['Station', 'Country', 'ID', 'Lat',
                         'Lon', 'Elev', 'WMO'])
locs = stations[['Lon', 'Lat']].values

# project into Alber's Equal Area, centered on antipode of each station
p1 = Proj({'proj':'longlat', 'datum':'WGS84'})
antipodes = {}
# for i in range(len(stations)):
i = 0
station = stations.iloc[i]

# project antipode
ant = antipode(station['Lat'], station['Lon'])
# p2 = Proj({'proj':'aea', 'datum':'WGS84', 'lon_0':ant[1]})
p2 = Proj({'proj': 'aeqd', 'lat_0': ant[0], 'lon_0': ant[1]})
ant = transform(p1, p2, ant[1], ant[0])

# project other points
points = vstack(transform(p1, p2, locs[:,0], locs[:,1])).T
nbrs = NearestNeighbors(n_neighbors = 5,
        algorithm='ball_tree').fit(points)

distances, indices = nbrs.kneighbors(ant)
distances = distances[0]
indices = indices[0]

ix = indices[distances < 100000]
if len(ix) > 0:
    antipodes[i] = ix
