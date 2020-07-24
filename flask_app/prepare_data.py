from geopy.geocoders import Yandex
from geopy.extra.rate_limiter import RateLimiter
from geopy import distance
import math

lon_center, lat_center = 55.753595, 37.621031

geolocator = Yandex(api_key='9169aca7-b00e-4539-ab1d-e7bb613cfee2')


def house_geo(address):
    location = geolocator.geocode(address)
    return location.latitude, location.longitude


def center_distance(address):
    return distance.distance(house_geo(address), (lon_center, lat_center)).km


def subway_distance(address, subway):
    location = geolocator.geocode(f'Moscow, {subway}')
    subway_geo = (location.latitude, location.longitude)
    return distance.distance(house_geo(address), subway_geo).km


def azimute(long, lat):
    # pi - число pi, rad - радиус сферы (Земли)
    rad = 6372795

    # координаты двух точек
    llat1 = lat
    llong1 = long

    llat2 = lat_center
    llong2 = lon_center

    # в радианах
    lat1 = llat1 * math.pi / 180.
    lat2 = llat2 * math.pi / 180.
    long1 = llong1 * math.pi / 180.
    long2 = llong2 * math.pi / 180.

    # косинусы и синусы широт и разницы долгот
    cl1 = math.cos(lat1)
    cl2 = math.cos(lat2)
    sl1 = math.sin(lat1)
    sl2 = math.sin(lat2)
    delta = long2 - long1
    cdelta = math.cos(delta)
    sdelta = math.sin(delta)

    # вычисления длины большого круга
    y = math.sqrt(
        math.pow(cl2 * sdelta, 2) + math.pow(cl1 * sl2 - sl1 * cl2 * cdelta,
                                             2))
    x = sl1 * sl2 + cl1 * cl2 * cdelta
    ad = math.atan2(y, x)
    dist = ad * rad

    # вычисление начального азимута
    x = (cl1 * sl2) - (sl1 * cl2 * cdelta)
    y = sdelta * cl2
    z = math.degrees(math.atan(-y / x))

    if (x < 0):
        z = z + 180.

    z2 = (z + 180.) % 360. - 180.
    z2 = - math.radians(z2)
    anglerad2 = z2 - ((2 * math.pi) * math.floor((z2 / (2 * math.pi))))
    angledeg = (anglerad2 * 180.) / math.pi

    return round(angledeg, 3)
