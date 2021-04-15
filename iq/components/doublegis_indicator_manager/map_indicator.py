#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Abstract indicator maps.

The map indicator provides information to be displayed on
Yandex maps, Google maps, etc. GIS.
Spots, markers, coverage circles, etc. can serve as an indicator.

By default, geolocation is obtained using Yandex Maps.
To determine geolocations, use API Key in requests to the Web service.
API Key can be obtained through the developer's cabinet.
The daily limit for determining the geolocation of addresses is 25,000.
Developer cabinet Yandex: https://developer.tech.yandex.ru/services/
API Key is stored in a separate file API_KEY_YANDEX_FILENAME.
"""

import itertools
import os.path
import uuid

from iq.util import log_func
from iq.util import file_func
from iq.util import txtfile_func

from iq.engine.wx import wxcolour_func
try:
    import yandex_maps
except ImportError:
    log_func.warning(u'Error importing <yandex_maps> library to determine geolocation by address')
    yandex_maps = None

try:
    import dadata
except ImportError:
    log_func.warning(u'Error importing <dadata> labrary to determine geolocation by address')
    dadata = None

import urllib.request
import urllib.parse
import json

__version__ = (0, 0, 0, 1)

# Default scale factor
DEFAULT_ZOOM = 14

GEO_LOCATOR_DEFAULT = True

# Geolocator cache
# The cache will keep the match address -> (latitude, longitude)
GEO_LOCATOR_CACHE = None

# Yandex API key
API_KEY_YANDEX_FILENAME = os.path.join(os.path.dirname(__file__), 'api_key_yandexmaps.txt')
YANDEX_GEO_LACATOR_URL_FMT = 'http://geocode-maps.yandex.ru/1.x/?geocode=%s&apikey=%s&format=json'

API_KEY_2GIS_FILENAME = os.path.join(os.path.dirname(__file__), 'api_key_2gis.txt')
DOUBLEGIS_GEO_LACATOR_URL_FMT = 'https://catalog_func.api.2gis.ru/geo/search?q=%s&format=json&limit=1&version=2.0&key=%s'

API_KEY_DADATA_FILENAME = os.path.join(os.path.dirname(__file__), 'api_key_dadata.txt')
SECRET_KEY_DADATA_FILENAME = os.path.join(os.path.dirname(__file__), 'secret_key_dadata.txt')

SPUTNIK_GEO_LOCATOR_URL_FMT = 'http://search.maps.sputnik.ru/search/addr?q=%s'


def getDefaultGeolocations(address_query, *args, **kwargs):
    """
    Get all geolocation data for the requested address by yandex maps.
    Checking geolocations from different sources sequentially:
    DaData.
    YandexMaps (by yandexmaps library).
    YandexMaps.

    :param address_query: Address.
        For example:
            Moscow, Gagarin street, 10.
    :return: [(latitude, longitude),...] Geolocation data list or empty list in case of error.
    """
    try:
        # DaData geolocator
        geo_location = getDaDataGeolocation(address_query=address_query, *args, **kwargs)
        if geo_location and geo_location[0] and geo_location[1]:
            return [geo_location]
        # Yandex geolocator
        geo_location = getYandexMapsGeolocation(address_query=address_query, *args, **kwargs)
        if geo_location and geo_location[0] and geo_location[1]:
            return [geo_location]
        # Yandex geolocations
        geo_locations = getYandexMapsGeolocations(address_query=address_query, *args, **kwargs)
        if geo_locations:
            return geo_locations

        log_func.warning(u'Not available geolocators')
    except:
        log_func.fatal(u'Error get default geolocations')
    return list()


def getDefaultGeolocation(address_query, item=0, cache=True):
    """
    Get all geolocation data for the requested address.

    :param address_query: Address.
        For example:
            Moscow, Gagarin street, 10.
    :param item: The index of the item to select.
    :param cache: Use internal cache?
    :return: (latitude, longitude) of geolocation data or (None, None) in case of error.
    """
    global GEO_LOCATOR_CACHE
    if cache:
        if GEO_LOCATOR_CACHE is None:
            GEO_LOCATOR_CACHE = dict()
        if address_query in GEO_LOCATOR_CACHE:
            # If such an address is in the cache, then we take it from the cache
            return GEO_LOCATOR_CACHE[address_query]

    geo_locations = getDefaultGeolocations(address_query)
    if geo_locations and item < len(geo_locations):
        if cache:
            # We save in the cache
            GEO_LOCATOR_CACHE[address_query] = geo_locations[item]
        return geo_locations[item]
    return None, None


def getYandexMapsGeolocations(address_query, geo_key=None):
    """
    Get all geolocation data for the requested address by yandex maps.

    :param address_query: Address.
        For example:
            Moscow, Gagarin street, 10.
    :param geo_key: Geolocator API key.
    :return: [(latitude, longitude),...] Geolocation data list or empty list in case of error.
    """
    if geo_key is None:
        geo_key = txtfile_func.loadTextFile(API_KEY_YANDEX_FILENAME).strip()

    try:
        address = urllib.parse.quote(address_query)
        url = YANDEX_GEO_LACATOR_URL_FMT % (address, geo_key)
        log_func.debug(u'Geodata retrieval URL <%s>' % url)
        response = urllib.request.urlopen(url)
        data = response.read()
        # ERROR: JSON object must be str not bytes
        #                                      V
        geo_location_data = json.loads(data.decode('utf-8'))

        find_geo = geo_location_data.get('response',
                                         dict()).get('GeoObjectCollection',
                                                     dict()).get('featureMember',
                                                                 list())
        str_geo_locations = [item.get('GeoObject', dict()).get('Point', dict()).get('pos', None) for item in find_geo]
        # [NOTE] In API Yandex Maps longitude first, then latitude,
        #                                                V
        geo_locations = [tuple([float(pos) for pos in reversed(location.split(' '))]) if location is not None else (None, None) for location in str_geo_locations]
        return geo_locations
    except Exception as e:
        log_func.fatal(u'Yandex default. Error retrieving geolocation data by address <%s>' % address_query)
    return list()


def getYandexMapsGeolocation(address_query, geo_key=None, cache=True):
    """
    Get geolocation data for the requested address.
    Library used https://github.com/begyy/Yandexmaps.
    Ubuntu installation: pip3 install Yandexmaps.

    :param address_query: Address.
        For example:
            Moscow, Gagarin street, 10.
    :param geo_key: Geolocator API key.
    :param cache: Use internal cache?
    :return: (latitude, longitude) of geolocation data or (None, None) in case of error.
    """
    if geo_key is None:
        geo_key = txtfile_func.loadTextFile(API_KEY_YANDEX_FILENAME).strip()

    global GEO_LOCATOR_CACHE
    if cache:
        if GEO_LOCATOR_CACHE is None:
            GEO_LOCATOR_CACHE = dict()
        if address_query in GEO_LOCATOR_CACHE:
            # If such an address is in the cache, then we take it from the cache
            return GEO_LOCATOR_CACHE[address_query]

    try:
        if not yandex_maps:
            log_func.warning(u'Yandexmaps library not installed. Ubuntu installation: pip3 install Yandexmaps')
            return None, None
        yandex = yandex_maps.Yandexmaps(api_key=geo_key)
        geo_location = yandex.address(address=address_query)
        # [NOTE] In API Yandex Maps longitude first, then latitude,
        #                             V
        geo_location_tuple = tuple(reversed(geo_location))
        if cache:
            # Save in the cache
            GEO_LOCATOR_CACHE[address_query] = geo_location_tuple
        return geo_location
    except Exception as e:
        log_func.fatal(u'Yandexmaps. Error retrieving geolocation data by address <%s>' % address_query)
    return None, None


def get2GISGeolocations(address_query, geo_key=None, cache=True):
    """
    Get all geolocation data for the requested address.
    Function not debugged!!!
    
    :param address_query: Address.
        For example:
            Moscow, Gagarin street, 10.
    :param geo_key: Geolocator API key.
    :param cache: Use internal cache?
    :return: [(latitude, longitude),...] Geolocation data list or empty list in case of error.
    """
    if geo_key is None:
        geo_key = txtfile_func.loadTextFile(API_KEY_2GIS_FILENAME).strip()

    global GEO_LOCATOR_CACHE
    if cache:
        if GEO_LOCATOR_CACHE is None:
            GEO_LOCATOR_CACHE = dict()
        if address_query in GEO_LOCATOR_CACHE:
            # If such an address is in the cache, then we take it from the cache
            return GEO_LOCATOR_CACHE[address_query]

    try:
        address = urllib.parse.quote(address_query)
        url = DOUBLEGIS_GEO_LACATOR_URL_FMT % (address, geo_key)
        response = urllib.request.urlopen(url)
        data = response.read()
        geo_location_data = json.loads(data)

        find_geo = geo_location_data.get('response',
                                         dict()).get('GeoObjectCollection',
                                                     dict()).get('featureMember',
                                                                 list())
        str_geo_locations = [item.get('GeoObject', dict()).get('Point', dict()).get('pos', None) for item in find_geo]
        # [NOTE] In API Yandex Maps longitude first, then latitude,
        #                                                V
        geo_locations = [tuple([float(pos) for pos in reversed(location.split(' '))]) if location is not None else (None, None) for location in str_geo_locations]
        return geo_locations
    except Exception as e:
        log_func.fatal(u'2GIS. Error retrieving geolocation data by address <%s>' % address_query)
    return list()


def getDaDataGeolocation(address_query, api_key=None, secret_key=None, cache=True):
    """
    Get geolocation data for the requested address.
    Library used https://github.com/hflabs/dadata-py.
    Ubuntu installation: pip3 install dadata

    :param address_query: Address.
        For example:
            Moscow, Gagarin street, 10.
    :param api_key: Geolocator API key.
    :param secret_key: Secret key.
    :param cache: Use internal cache?
    :return: (latitude, longitude) of geolocation data or (None, None) in case of error.
    """
    if api_key is None:
        api_key = txtfile_func.loadTextFile(API_KEY_DADATA_FILENAME).strip()
    if secret_key is None:
        secret_key = txtfile_func.loadTextFile(SECRET_KEY_DADATA_FILENAME).strip()

    global GEO_LOCATOR_CACHE
    if cache:
        if GEO_LOCATOR_CACHE is None:
            GEO_LOCATOR_CACHE = dict()
        if address_query in GEO_LOCATOR_CACHE:
            # If such an address is in the cache, then we take it from the cache
            return GEO_LOCATOR_CACHE[address_query]

    dadata_client = None
    try:
        if not dadata:
            log_func.warning(u'DaData library not installed. Ubuntu installation: pip3 install dadata')
            return None, None
        dadata_client = dadata.Dadata(token=api_key, secret=secret_key)
        geo_data = dadata_client.clean(name='address', source=address_query)
        dadata_client.close()
        dadata_client = None

        geo_latitude = geo_data.get('geo_lat', None)
        geo_latitude = float(geo_latitude.replace(',', '.')) if isinstance(geo_latitude, str) else geo_latitude
        geo_longitude = geo_data.get('geo_lon', None)
        geo_longitude = float(geo_longitude.replace(',', '.')) if isinstance(geo_longitude, str) else geo_longitude
        log_func.debug(u'Address <%s>. Geo position [%f x %f]' % (address_query, geo_latitude, geo_longitude))
        if cache:
            # Save in the cache
            GEO_LOCATOR_CACHE[address_query] = (geo_latitude, geo_longitude)
        return geo_latitude, geo_longitude
    except Exception as e:
        if dadata_client:
            dadata_client.close()
        log_func.fatal(u'DaData. Error retrieving geolocation data by address <%s>' % address_query)
    return None, None


def getSputnikGeolocations(address_query):
    """
    Get all geolocation data for the requested address
    by service http://api.sputnik.ru/maps/geocoder/.

    :param address_query: Address.
        For example:
            Moscow, Gagarin street, 10.
    :return: [(latitude, longitude),...] Geolocation data list or empty list in case of error.
    """
    try:
        address = urllib.parse.quote(address_query)
        url = SPUTNIK_GEO_LOCATOR_URL_FMT % address
        log_func.debug(u'Geodata retrieval URL <%s>' % url)
        response = urllib.request.urlopen(url)
        data = response.read()
        # ERROR: JSON object must be str not bytes
        #                                      V
        geo_location_data = json.loads(data.decode('utf-8'))

        find_address = geo_location_data.get('result',
                                             dict()).get('address', list())
        find_features = list(itertools.chain(*[item.get('features', list()) for item in find_address]))
        find_geometries = list(itertools.chain(*[item.get('geometry', dict()).get('geometries', list()) for item in find_features]))
        find_coordinates = [item.get('coordinates', list()) for item in find_geometries]
        find_coordinates = [list(reversed(item)) for item, _ in itertools.groupby(find_coordinates)]

        return find_coordinates
    except Exception as e:
        log_func.fatal(u'Sputnik. Error retrieving geolocation data by address <%s>' % address_query)
    return list()


class iqMapIndicator(object):
    """
    Abstract indicator maps. Implements a common interface to map indicators.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        pass

    def getMap(self):
        """
        Map object.
        """
        return None

    def getHTMLFilename(self):
        """
        The current HTML file of the map viewer browser.
        """
        return None

    def findGeoLocations(self, address_query):
        """
        Get geographic latitude and longitude data for an address request.

        :param address_query: Address.
        :return: [(latitude, longitude), ...] of geolocation data or [] in case of error.
        """
        return list()

    def findGeoLocation(self, address_query):
        """
        Obtain geographic latitude and longitude data for an address request.

        :param address_query: Address.
        :return: (latitude, longitude) of geolocation data or (None, None) in case of error.
        """
        return None, None

    def getMapBitmap(self, geo_latitude, geo_longitude, img_filename=None):
        """
        Get a map in the form of a picture at the specified geographic coordinates.

        :param geo_latitude: Geographic latitude.
        :param geo_longitude: Geographic longitude.
        :param img_filename: Image file to save.
            If not specified, the file is not automatically saved.
        :return: wx.Bitmap of the requested card, or None on error.
        """
        return None

    def setCircleMarker(self, geo_latitude, geo_longitude,
                        radius=100, color='blue',
                        is_fill=True, fill_color='blue',
                        popup_text=u'', tooltip_text=u''):
        """
        Adding a circle marker to the map.

        :param geo_latitude: Geographic latitude.
        :param geo_longitude: Geographic longitude.
        :param radius: The radius of the circle.
        :param color: Circle color.
        :param is_fill: Fill the inner area of the circle?
        :param fill_color: The fill color of the circle.
        :param popup_text: Marker pop-up text.
            A tooltip appears by clicking on the marker.
        :param tooltip_text: Marker tooltip text.
            A tooltip appears when you hover the mouse over the marker.
        :return: True/False.
        """
        log_func.warning(u'setCircleMarker not defined in <%s> component' % self.__class__.__name__)
        return False

    def setPinMarker(self, geo_latitude, geo_longitude,
                     color='blue', icon=None,
                     popup_text=u'', tooltip_text=u''):
        """
        Adding a pointer marker to the map.

        :param geo_latitude: Geographic latitude.
        :param geo_longitude: Geographic longitude.
        :param color: Marker color.
        :param icon: Marker icon.
        :param popup_text: Marker pop-up text.
            A tooltip appears by clicking on the marker.
        :param tooltip_text: Marker tooltip text.
            A tooltip appears when you hover the mouse over the marker.
        :return: True/False.
        """
        log_func.warning(u'setPinMarker not defined in <%s> component' % self.__class__.__name__)
        return False

    def setCircleMarkerByAddress(self, address,
                                radius=100, color='blue',
                                is_fill=True, fill_color='blue',
                                popup_text=u'', tooltip_text=u''):
        """
        Adding a marker to the map in the form of a circle at the address.

        :param address: Address.
        :param radius: Circle radius.
        :param color: Circle color.
        :param is_fill: Fill the inner area of the circle?
        :param fill_color: The fill color of the circle.
        :param popup_text: Marker pop-up text.
            A tooltip appears by clicking on the marker.
        :param tooltip_text: Marker tooltip text.
            A tooltip appears when you hover the mouse over the marker.
        :return: True/False.
        """
        geo_latitude, geo_longitude = self.findGeoLocation(address_query=address)
        return self.setCircleMarker(geo_latitude, geo_longitude,
                                    radius=radius, color=color,
                                    is_fill=is_fill, fill_color=fill_color,
                                    popup_text=popup_text, tooltip_text=tooltip_text)

    def setPinMarkerByAddress(self, address,
                              color='blue', icon=None,
                              popup_text=u'', tooltip_text=u''):
        """
        Adding an address marker to the map.

        :param address: Address.
        :param color: Marker color.
        :param icon: Marker icon.
        :param popup_text: Marker pop-up text.
            A tooltip appears by clicking on the marker.
        :param tooltip_text: Marker tooltip text.
            A tooltip appears when you hover the mouse over the marker.
        :return: True/False.
        """
        geo_latitude, geo_longitude = self.findGeoLocation(address_query=address)
        return self.setPinMarker(geo_latitude, geo_longitude,
                                 color=color, icon=icon,
                                 popup_text=popup_text, tooltip_text=tooltip_text)

    def saveMapBrowserFile(self, geo_latitude, geo_longitude,
                           zoom=DEFAULT_ZOOM, html_filename=None, rewrite=False):
        """
        Save HTML file to display the map.

        :param geo_latitude: Geographic latitude.
        :param geo_longitude: Geographic longitude.
        :param zoom: The default scale factor.
        :param html_filename: The name of the file to be saved.
            If not specified, it is generated.
        :param rewrite: Overwrite existing file?
        :return: Full name of the HTML file or None in case of error.
        """
        log_func.warning(u'saveMapBrowserFile not define in <%s> component' % self.__class__.__name__)
        return None

    def saveMapBrowserFileByAddress(self, address, zoom=DEFAULT_ZOOM,
                                    html_filename=None, rewrite=False):
        """
        Save HTML file to display the map when requested for an address.

        :param address: Address.
        :param zoom: The default scale factor.
        :param html_filename: The name of the file to be saved.
            If not specified, it is generated.
        :param rewrite: Overwrite existing file?
        :return: Full name of the HTML file or None in case of error.
        """
        log_func.warning(u'saveMapBrowserFileByAddress not define in <%s> component' % self.__class__.__name__)
        return None

    def createMap(self, geo_latitude, geo_longitude,
                  zoom=DEFAULT_ZOOM,
                  html_filename=None, rewrite=False):
        """
        Create map object.

        :param geo_latitude: Geographic latitude.
        :param geo_longitude: Geographic longitude.
        :param zoom: The default scale factor.
        :param html_filename: The name of the file to be saved.
            If not specified, it is generated.
        :param rewrite: Overwrite existing file?
        :return: Map object or None if error.
        """
        log_func.warning(u'createMap not define in <%s> component' % self.__class__.__name__)
        return None

    def createMapByAddress(self, address,
                           zoom=DEFAULT_ZOOM,
                           html_filename=None, rewrite=False):
        """
        Create a map object by address.

        :param address: Address.
        :param zoom: The default scale factor.
        :param html_filename: The name of the file to be saved.
            If not specified, it is generated.
        :param rewrite: Overwrite existing file?
        :return: Map object or None if error.
        """
        log_func.warning(u'createMapByAddress not define in <%s> component' % self.__class__.__name__)
        return None


class iqMapIndicatorManagerProto(iqMapIndicator):
    """
    Abstract manager of indicator maps.
    Implements a common interface to map indicators.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        iqMapIndicator.__init__(self, *args, **kwargs)

        # Map rendering library
        self._rendering = None
        # Map browser control
        self._browser = None

        # Map control object
        self._geo_map = None

        # The current HTML file of the map viewer browser
        self._html_filename = None

    def setRendering(self, rendering):
        """
        Set the rendering library.
        Can be folium library or own double_gis library.

        :param rendering: Map rendering library.
            Default native library double_gis.
        """
        if rendering is None:
            from .. import double_gis
            rendering = double_gis
        self._rendering = rendering

    def getMap(self):
        """
        Get map object.
        """
        return self._geo_map

    def getHTMLFilename(self):
        """
        Get the current HTML file of the map viewer browser.
        """
        return self._html_filename

    def setHTMLFilename(self, html_filename):
        """
        Set the current HTML file of the map viewer browser.
        """
        self.setMapBrowserFile(html_filename=html_filename)

    def findGeoLocations(self, address_query):
        """
        Obtain geographic latitude and longitude data for an address request.

        :param address_query: Address.
        :return: List of tuples of found locations:
             (Geographic latitude, geographic longitude)
             or (None, None) on error.
        """
        if yandex_maps and not GEO_LOCATOR_DEFAULT:
            geo_locations = [getYandexMapsGeolocation(address_query)]
        else:
            geo_locations = getDefaultGeolocations(address_query)
        return geo_locations

    def findGeoLocation(self, address_query, item=0):
        """
        Obtain geographic latitude and longitude data for an address request.

        :param address_query: Address.
        :param item: The index of the selected item.
        :return: Tuple (Geographic latitude, geographic longitude)
             or (None, None) on error.
        """
        if yandex_maps and not GEO_LOCATOR_DEFAULT:
            geo_location = getYandexMapsGeolocation(address_query)
        else:
            geo_location = getDefaultGeolocation(address_query, item=item)
        return geo_location

    def setBrowser(self, browser):
        """
        Install a browser to display the map.

        :param browser: Browser control for displaying the map.
        """
        self._browser = browser

    def genMapBrowserFilename(self):
        """
        Generate the name of the browser HTML file to display the map.

        :return: Full filename for map display.
        """
        gen_uuid = str(uuid.uuid4())
        gen_path = os.path.join(file_func.getProjectProfilePath(),
                                gen_uuid + '.html')
        return gen_path

    def createMap(self, geo_latitude, geo_longitude,
                  zoom=DEFAULT_ZOOM,
                  html_filename=None, rewrite=False, auto_save=True):
        """
        Create map object.

        :param geo_latitude: Geographic latitude.
        :param geo_longitude: Geographic longitude.
        :param zoom: The default scale factor.
        :param html_filename: The name of the file to be saved.
            If not specified, it is generated.
        :param rewrite: Overwrite existing file?
        :param auto_save: Save file automatically?
        :return: Map object, or None on error.
        """
        if geo_latitude in (None, 0) or geo_longitude in (None, 0):
            log_func.warning(u'Incomplete definition of geolocation <%s : %s>' % (geo_latitude, geo_longitude))
            return None

        try:
            self._geo_map = self._rendering.Map(location=[geo_latitude, geo_longitude],
                                                zoom_start=zoom)
            log_func.info(u'Map object created. Geolocation [%s x %s]' % (geo_latitude, geo_longitude))
            if auto_save:
                self.saveMapBrowserFile(geo_latitude, geo_longitude, zoom=zoom,
                                        html_filename=html_filename, rewrite=rewrite)
        except:
            log_func.fatal(u'Error creating map object')
            self._geo_map = None
        return self._geo_map

    def createMapByAddress(self, address,
                           zoom=DEFAULT_ZOOM,
                           html_filename=None, rewrite=False,
                           auto_save=True):
        """
        Create a map object by address.

        :param address: Address.
        :param zoom: The default scale factor.
        :param html_filename: The name of the file to be saved.
            If not specified, it is generated.
        :param rewrite: Overwrite existing file?
        :param auto_save: Save file automatically?
        :return: Map object, or None on error.
        """
        geo_latitude, geo_longitude = self.findGeoLocation(address_query=address)
        return self.createMap(geo_latitude, geo_longitude, zoom=zoom,
                              html_filename=html_filename, rewrite=rewrite,
                              auto_save=auto_save)

    def saveMapBrowserFile(self, geo_latitude, geo_longitude,
                           zoom=DEFAULT_ZOOM,
                           html_filename=None, rewrite=False):
        """
        Save HTML file to display the map.

        :param geo_latitude: Geographic latitude.
        :param geo_longitude: Geographic longitude.
        :param zoom: The default scale factor.
        :param html_filename: The name of the file to be saved.
            If not specified, it is generated.
        :param rewrite: Overwrite existing file?
        :return: Full name of the HTML file or None in case of error.
        """
        if html_filename is None:
            html_filename = self.genMapBrowserFilename()
            self._html_filename = html_filename

        if os.path.exists(html_filename) and not rewrite:
            # If the file exists and you do not need to overwrite it, then we do nothing
            return html_filename

        if geo_latitude is None or geo_longitude is None:
            log_func.warning(u'Incomplete definition of geolocation <%s : %s>' % (geo_latitude, geo_longitude))
            return None

        try:
            if self._geo_map is None:
                self._geo_map = self._rendering.Map(location=[geo_latitude, geo_longitude],
                                                    zoom_start=zoom)
            self._geo_map.save(html_filename)
            return html_filename
        except:
            log_func.fatal(u'File save error <%s>' % html_filename)
        return None

    def saveMapBrowserFileByAddress(self, address, zoom=DEFAULT_ZOOM,
                                    html_filename=None, rewrite=False):
        """
        Save HTML file to display the map when requested for an address.

        :param address: Address.
        :param zoom: The default scale factor.
        :param html_filename: The name of the file to be saved.
            If not specified, it is generated.
        :param rewrite: Overwrite existing file?
        :return: Full name of the HTML file or None in case of error.
        """
        geo_latitude, geo_longitude = self.findGeoLocation(address_query=address)
        return self.saveMapBrowserFile(geo_latitude, geo_longitude,
                                       zoom=zoom, html_filename=html_filename,
                                       rewrite=rewrite)

    def setMapBrowserFile(self, html_filename=None):
        """
        Set HTML file in browser for viewing maps.

        :param html_filename: The name of the HTML file of the browser to view the maps.
            If not specified, the last generated name is taken.
        :return: True/False.
        """
        if html_filename:
            self._html_filename = html_filename

        if not os.path.exists(self._html_filename):
            log_func.warning(u'Map viewer HTML file not found <%s>' % self._html_filename)
            return False

        url = 'file://%s' % self._html_filename
        try:
            self._browser.LoadURL(url)
            return True
        except:
            log_func.fatal(u'Error opening URL maps in browser <%s>' % url)
        return False

    def setCircleMarker(self, geo_latitude, geo_longitude,
                        radius=100, color='blue',
                        is_fill=True, fill_color='blue',
                        popup_text=u'', tooltip_text=u''):
        """
        Adding a circle marker to the map.

        :param geo_latitude: Geographic latitude.
        :param geo_longitude: Geographic longitude.
        :param radius: Circle radius.
        :param color: Circle color.
        :param is_fill: Fill the inner area of the circle?
        :param fill_color: The fill color of the circle.
        :param popup_text: Marker pop-up text.
            A tooltip appears by clicking on the marker.
        :param tooltip_text: Marker tooltip text.
            A tooltip appears when you hover the mouse over the marker.
        :return: True/False.
        """
        if self._geo_map is not None:
            try:
                color = wxcolour_func.wxColour2StrRGB(color) if color else None
                fill_color = wxcolour_func.wxColour2StrRGB(color) if fill_color else None

                marker = self._rendering.CircleMarker(location=[geo_latitude, geo_longitude],
                                                      radius=radius,
                                                      popup=popup_text if popup_text else None,
                                                      color=color if color else None,
                                                      fill=is_fill,
                                                      fill_color=fill_color if fill_color else None,
                                                      tooltip=tooltip_text if tooltip_text else None)
                marker.add_to(self._geo_map)
                log_func.debug(u'Circle marker created. Geolocation [%s x %s]' % (geo_latitude, geo_longitude))
            except:
                log_func.fatal(u'Error adding a circle marker to the map')
        else:
            log_func.warning(u'Map object not defined to add a circle marker')
        return False

    def setPinMarker(self, geo_latitude, geo_longitude,
                     color='blue', icon=None,
                     popup_text=u'', tooltip_text=u''):
        """
        Adding a pointer marker to the map.

        :param geo_latitude: Geographic latitude.
        :param geo_longitude: Geographic longitude.
        :param color: Marker color.
        :param icon: Marker icon.
        :param popup_text: Marker pop-up text.
            A tooltip appears by clicking on the marker.
        :param tooltip_text: Marker tooltip text.
            A tooltip appears when you hover the mouse over the marker.
        :return: True/False.
        """
        if self._geo_map is not None:
            try:
                color = wxcolour_func.wxColour2StrRGB(color) if color else None

                # marker_icon = None
                # if icon and color:
                #     marker_icon = folium.Icon(color=color, icon=icon)
                # elif icon and color:
                #     marker_icon = folium.Icon(color=color)

                marker = self._rendering.Marker(location=[geo_latitude, geo_longitude],
                                                popup=popup_text if popup_text else None,
                                                tooltip=tooltip_text if tooltip_text else None,
                                                icon=icon)
                marker.add_to(self._geo_map)
                # log_func.debug(u'Pin marker created. Geolocation [%s x %s]' % (geo_latitude, geo_longitude))
                return True
            except:
                log_func.fatal(u'Error adding a pointer marker to the map')
        else:
            log_func.warning(u'Map object not defined to add a pointer marker')
        return False
