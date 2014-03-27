# courtesy of http://en.wikipedia.org/wiki/Antipodes#Cities

antipodes = [ ['Christchurch, New Zealand', 'A Coruna, Spain'],
              ['Hamilton, New Zealand', 'Cordoba, Spain'],
              ['Hong Kong', 'La Quiaca, Argentina'],
              ['Junin, Argentina', 'Lianyungang, China'],
              ['Padang, Indonesia', 'Esmeraldas, Ecuador'],
              ['Palembang, Indonesia', 'Neiva, Colombia'],
              ['Rafaela, Argentina', 'Wuhu, China'],
              ['Segovia, Spain', 'Masterton, New Zealand'],
              ['Tauranga, New Zealand', 'Jaen, Spain'],
              ['Ulan Ude, Russia', 'Puerto Natales, Chile'],
              ['Valdivia, Chile', 'Wuhai, China'],
              ['Whangarei, New Zealand', 'Tangier, Morocco'],
              ['Xian, China', 'Santiago, Chile'],
              ['Auckland, New Zealand', 'Seville, Spain'],
              ['Auckland, New Zealand', 'Setenil de las Bodegas, Spain'],
              ['Auckland, New Zealand', 'Malaga, Spain'],
              ['Tianjin, China', 'Bahia Blanca, Argentina'],
              ['Shanghai, China', 'Salto, Uruguay'],
              ['Taipei, Taiwan', 'Asuncion, Paraguay'],
              ['Nanjing, China', 'Rosario, Argentina'],
              ['Montpellier, France', 'Waitangi, New Zealand'],
              ['Beijing, China', 'Bahia Blanca, Argentina'],
              ['Beijing, China', 'Buenos Aires, Argentina'],
              ['Shanghai, China', 'Buenos Aires, Argentina'],
              ['Bogota, Colombia', 'Jakarta, Indonesia'],
              ['Guayaquil, Ecuador', 'Medan, Indonesia'],
              ['Phnom Penh, Cambodia', 'Lima, Peru'],
              ['Dili, Timor-Leste', 'Paramaribo, Suriname'],
              ['Irkutsk, Russia', 'Punta Arenas, Chile'],
              ['Tongchuan, China', 'Licanten, Chile'],
              ['Suva, Fiji', 'Timbuktu, Mali'],
              ['Canberra, Australia', 'Azores, Portugal'],
              ['Melbourne, Australia', 'Azores, Portugal'],
              ['Cherbourg, France', 'Antipodes Islands'],
              ['Pago Pago, American Samoa', 'Zinder, Niger'],
              ['Barranquilla, Colombia', 'Christmas Island, Australia'],
              ['Doha, Qatar', 'Pitcairn Island'],
              ['Hue, Vietnam', 'Arequipa, Peru'],
              ['Da Nang, Vietnam', 'Arequipa, Peru'],
              ['Manila, Philippines', 'Cuiaba, Brazil'],
              ['Kuala Lumpur, Malaysia', 'Cuenca, Ecuador'],
              ['San Juan, Puerto Rico', 'Karratha, Australia'],
              ['Limerick, Ireland', 'Campbell Islands, New Zealand'],
              ['Arrecife', 'Norfolk Island'],
              ['Lanzarote', 'Norfolk Island'],
              ['Canary Islands', 'Norfolk Island'],
              ['Sharm el Sheikh, Egypt', 'Rapa Iti, French Polynesia'],
              ['Bangkok, Thailand', 'Lima, Peru'],
              ['Quito, Ecuador', 'Singapore'],
              ['Perth, Australia', 'Hamilton, Bermuda'],
              ['Montevideo, Uruguay', 'Seoul, South Korea'] ]


# unique locations
locs = []
for pair in antipodes:
    for l in pair:
        if l not in locs:
            locs.append(l)

# query api
from requests import get
from numpy import abs, argmin, nan
import pickle

# openweathermap.org
appid = 'aa0bffa7bbd13e7350183cfcfd3c66b38'
responses = {}
for loc in locs:
    responses[loc] = None
    q = 'http://api.openweathermap.org/data/2.5/find?q=%s&mode=json&units=imperial&APPID=%s' % (loc, appid)
    r = get(q)
    responses[loc] = r.json()
pickle.dump(responses, open('data/responses.p', 'wb'))

# responses = pickle.load(open('data/responses.p', 'rb'))

temps = []
diffs = []
for pair in antipodes:
    l1, l2 = pair
    if len(responses[l1]['list']) > 0 and len(responses[l2]['list']) > 0:
        t1 = responses[l1]['list'][0]['main']['temp']
        t2 = responses[l2]['list'][0]['main']['temp']

        temps.append([t1, t2])
        diffs.append(abs(t1 - t2))
    else:
        temps.append([nan, nan])
        diffs.append(200)

ix = argmin(diffs)

print '%s: %.1fF' % (antipodes[ix][0], temps[ix][0])
print '%s: %.1fF' % (antipodes[ix][1], temps[ix][1])
