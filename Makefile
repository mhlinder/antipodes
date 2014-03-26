stations:
	curl http://www.wunderground.com/about/faq/international_cities.asp?MR=1 | awk '/<pre>/{cont = 1; next}/<\/pre>/{cont = 0}cont' | awk '/--/{cont = 1; next}cont' > data/station_list
