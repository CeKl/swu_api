"""swu_api

Python libary for the use of the public transport and carsharing API of the Stadtwerke Ulm / Neu-Ulm (SWU).

MIT License
Copyright (c) 2021 Cedric Klimt

"""

from requests import get
from requests.exceptions import RequestException
import datetime


def do_request(endpoint, params, mode):
    """Function for webrequest at SWU API.

    Args:
        endpoint (str): API-Endpoint
        params (dict): parameters for API call
        mode (int): request mode. 0 = public transport / 1 = carsharing

    Returns:
        dict: Data from API.
    """

    if mode == 1:
        api_interface = 'mobility/v1'
    elif mode == 2:
        api_interface = 'sharing/v2'

    try:
        data = get(
            'https://api.swu.de/{api_interface}/{endpoint}'.format(api_interface=api_interface, endpoint=endpoint), params=params)
    except RequestException as e:
        print(e)

    return data.json()


class ContenscopeError(Exception):
    """Custom Exception - contentscope."""

    def __str__(self):
        return 'Unvalide contentscope. Try minimal, basic or extended.'


class StopnumberError(Exception):
    """Custom Exception - stopnumber."""

    def __str__(self):
        return 'Unvalide stopnumber.'


class StoppointcodeError(Exception):
    """Custom Exception - stoppointcode."""

    def __str__(self):
        return 'Unvalide stoppointcode.'


class RangeError(Exception):
    """Custom Exception - range."""

    def __str__(self):
        return 'Unvalide range_value. Try all or upcoming.'


class swu_pt_functions():
    """General functions to access the SWU API for public transport.

    Raises:
        ContenscopeError: Unvalide contentscope. Try minimal, basic or extended.
        StopnumberError: Unvalide stopnumber.
        StoppointcodeError: Unvalide stoppointcode.
        RangeError: Unvalide range_value. Try all or upcoming.

    Returns:
        dict: Requestet data.
    """

    @staticmethod
    def base_route(routenumber=0, contentscope='basic'):
        """Basedata: Route.

        Args:
            routenumber (int, optional): Routnumber; 0 = all routes. Defaults to 0.
            contentscope (str, optional): Information level. Defaults to 'basic'.

        Raises:
            ContenscopeError: Unvalide contentscope.

        Returns:
            dict: Requestet data.
        """

        payload = {}
        if routenumber == 0:
            routenumber = ''
        payload['RouteNumber'] = str(routenumber)

        if contentscope in ['minimal', 'basic', 'extended']:
            payload['ContentScope'] = contentscope
        else:
            raise ContenscopeError()

        endpoint = 'route/attributes/BaseData'
        route_data = do_request(endpoint=endpoint, params=payload, mode=1)

        return route_data

    @staticmethod
    def base_stop(stopnumber=0, contentscope='basic'):
        """Basedata: Stop.

        Args:
            stopnumber (int, optional): Stopnumber (4-digits); 0 = all stops. Defaults to ''.
            contentscope (str, optional): Information level. Defaults to 'basic'.

        Raises:
            StopnumberError: Unvalide stopnumber.
            ContenscopeError: Unvalide contentscope.

        Returns:
            dict: Requestet data.
        """

        payload = {}
        if stopnumber != 0 and len(stopnumber) != 4:
            # TODO hier 2 exceptions einführen
            raise StopnumberError()

        if stopnumber == 0:
            stopnumber = ''
        payload['StopNumber'] = str(stopnumber)

        if contentscope in ['minimal', 'basic', 'extended']:
            payload['ContentScope'] = contentscope
        else:
            raise ContenscopeError()

        endpoint = 'stop/attributes/BaseData'
        stop_data = do_request(endpoint=endpoint, params=payload, mode=1)

        return stop_data

    @staticmethod
    def base_stop_point(stoppointcode=0, contentscope='basic'):
        """Basedata: StopPoint (Platform of Stop).

        Args:
            stoppointcode (int, optional): Code of stoppoint (6-digits); 0 = all. Defaults to 0.
            contentscope (str, optional): Information level. Defaults to 'basic'.

        Raises:
            StopnumberError: Unvalide Stopnumber.
            ContenscopeError: Unvalide contentscope.

        Returns:
            dict: Requestet data.
        """

        payload = {}
        if stoppointcode != 0 and len(stoppointcode) != 6:
            # TODO hier 2 exceptions einführen
            raise StoppointcodeError()

        if stoppointcode == 0:
            stoppointcode = ''
        payload['StopPointCode'] = stoppointcode

        if contentscope in ['minimal', 'basic', 'extended']:
            payload['ContentScope'] = contentscope
        else:
            raise ContenscopeError()

        endpoint = 'stoppoint/attributes/BaseData'
        stop_point_data = do_request(endpoint=endpoint, params=payload, mode=1)

        return stop_point_data

    @staticmethod
    def base_vehicle(vehiclenumber=0, contentscope='basic'):
        """Basedata: Vehicle.

        Args:
            vehiclenumber (int, optional): Number of the vehicle. Defaults to 0.
            contentscope (str, optional): Information level. Defaults to 'basic'.

        Raises:
            ContenscopeError: Unvalide contentscope.

        Returns:
            dict: Requestet data.
        """

        payload = {}
        if vehiclenumber == 0:
            vehiclenumber = ''
        payload['VehicleNumber'] = vehiclenumber

        if contentscope in ['minimal', 'basic', 'extended']:
            payload['ContentScope'] = contentscope
        else:
            raise ContenscopeError()

        endpoint = 'vehicle/attributes/BaseData'
        vehicle_data = do_request(endpoint=endpoint, params=payload, mode=1)

        return vehicle_data

    @staticmethod
    def live_stop_departures(stopnumber, limit=5):
        """Livedata: Stop - Departures.

        Args:
            stopnumber (int): Stopnumber (4-digits).
            limit (int, optional): Number of returned departures. Defaults to 5.

        Raises:
            StopnumberError: Unvalide Stopnumber.

        Returns:
            dict: Requestet data.
        """

        payload = {}
        if len(str(stopnumber)) != 4:
            raise StopnumberError()

        payload['StopNumber'] = str(stopnumber)
        payload['Limit'] = str(limit)

        endpoint = 'stop/passage/Departures'
        stop_departures_data = do_request(
            endpoint=endpoint, params=payload, mode=1)

        return stop_departures_data

    @staticmethod
    def live_stop_arrivals(stopnumber, limit=5):
        """Livedata: Stop - Arrivals.

        Args:
            stopnumber (int): Stopnumber (4-digits).
            limit (int, optional): Number of returned departures. Defaults to 5.

        Raises:
            StopnumberError: Unvalide stopnumber.

        Returns:
            dict: Requestet data.
        """

        payload = {}
        if len(str(stopnumber)) != 4:
            raise StopnumberError()

        payload['StopNumber'] = str(stopnumber)
        payload['Limit'] = str(limit)

        endpoint = 'stop/passage/Arrivals'
        stop_arrivals_data = do_request(
            endpoint=endpoint, params=payload, mode=1)

        return stop_arrivals_data

    @staticmethod
    def live_stop_point_departures(stoppointcode, limit=5):
        """Livedata: StopPoint - Departures.

        Args:
            stoppointcode (int): Code of stoppoint (6-digits).
            limit (int, optional): Number of returned departures. Defaults to 5.

        Raises:
            StoppointcodeError: Unvalide stoppointcode.

        Returns:
            dict: Requestet data.
        """

        payload = {}
        if len(str(stoppointcode)) != 6:
            raise StoppointcodeError()

        payload['StopPointCode'] = str(stoppointcode)
        payload['Limit'] = str(limit)

        endpoint = 'stoppoint/passage/Departures'
        stop_point_departures_data = do_request(
            endpoint=endpoint, params=payload, mode=1)

        return stop_point_departures_data

    @staticmethod
    def live_stop_point_arrivals(stoppointcode, limit=5):
        """Livedata: StopPoint - Arrivals.

        Args:
            stoppointcode (str): Code of stoppoint (6-digits).
            limit (int, optional): Number of returned departures. Defaults to 5.

        Raises:
            StoppointcodeError: Unvalide stoppointcode.

        Returns:
            dict: Requestet data.
        """

        payload = {}
        if len(str(stoppointcode)) != 6:
            raise StoppointcodeError()

        payload['StopPointCode'] = str(stoppointcode)
        payload['Limit'] = str(limit)

        endpoint = 'stoppoint/passage/Arrivals'
        stop_point_arrivals_data = do_request(
            endpoint=endpoint, params=payload, mode=1)

        return stop_point_arrivals_data

    @staticmethod
    def live_vehicle_trip(vehiclenumber=0):
        """Livedata: Vehicle - Trip.

        Args:
            vehiclenumber (str, optional): Number of the vehicle; 0 = all. Defaults to 0.

        Returns:
            dict: Requestet data.
        """

        payload = {}
        payload['VehicleNumber'] = str(vehiclenumber)

        endpoint = 'vehicle/trip/Trip'
        vehicle_trip_data = do_request(
            endpoint=endpoint, params=payload, mode=1)

        return vehicle_trip_data

    @staticmethod
    def live_vehicle_passage(vehiclenumber, range_value='all'):
        """Livedaten: Vehicle - Passage 

        Args:
            vehiclenumber (int): Number of the vehicle.
            range_value (str, optional): Range of returned values. Choose between 'all'or 'upcoming'. Defaults to 'all'.

        Raises:
            RangeError: Unvalide range_value.

        Returns:
            dict: Requestet data.
        """

        payload = {}
        payload['VehicleNumber'] = str(vehiclenumber)

        if range_value in ['all', 'upcoming']:
            payload['Range'] = range_value
        else:
            raise RangeError()

        endpoint = 'vehicle/trip/Passage'
        vehicle_passage_data = do_request(
            endpoint=endpoint, params=payload, mode=1)

        return vehicle_passage_data

    @staticmethod
    def live_vehicle_pattern(vehiclenumber, contentscope='Track'):
        """Livedaten: Vehicle - pattern 

        Args:
            vehiclenumber (int): Number of the vehicle.
            contentscope (str, optional): Information level. Choose 'Stops', 'Track' or 'Carriageway'. Defaults to 'Track'.

        Raises:
            ContenscopeError: Unvalide contentscope.

        Returns:
            dict: Requestet data.
        """

        payload = {}
        payload['VehicleNumber'] = str(vehiclenumber)

        if contentscope in ['Stops', 'Track', 'Carriageway']:
            payload['ContentScope'] = contentscope
        else:
            raise ContenscopeError()

        endpoint = 'vehicle/trip/Pattern'
        vehicle_pattern_data = do_request(
            endpoint=endpoint, params=payload, mode=1)

        return vehicle_pattern_data


class swu_cs_functions():
    """General functions to access the SWU API for carsharing.

    Returns:
        dict: Requestet data.
    """

    @staticmethod
    def basic_info():
        """Get basic info of the carsharing API.

        Returns:
            dict: Requestet data.
        """

        basic_info_data = do_request(endpoint='gbfs.json', params={}, mode=2)

        basic_info_data['last_updated_dt'] = datetime.datetime.fromtimestamp(
            basic_info_data['last_updated'])

        return basic_info_data

    @staticmethod
    def system_info():
        """Get information of the system swu2go.

        Returns:
            dict: Requestet data.
        """

        system_info_data = do_request(
            endpoint='system_information.json', params={}, mode=2)

        system_info_data['last_updated_dt'] = datetime.datetime.fromtimestamp(
            system_info_data['last_updated'])

        return system_info_data

    @staticmethod
    def station_info():
        """Get information of all stations.

        Returns:
            dict: Requestet data.
        """

        station_info_data = do_request(
            endpoint='station_information.json', params={}, mode=2)

        station_info_data['last_updated_dt'] = datetime.datetime.fromtimestamp(
            station_info_data['last_updated'])

        return station_info_data

    @staticmethod
    def station_status():
        """Get current status of all stations.

        Returns:
            dict: Requestet data.
        """

        station_status_data = do_request(
            endpoint='station_status.json', params={}, mode=2)

        station_status_data['last_updated_dt'] = datetime.datetime.fromtimestamp(
            station_status_data['last_updated'])

        for _, station in enumerate(station_status_data['data']['stations']):
            station['last_reported_dt'] = datetime.datetime.fromtimestamp(
                station['last_reported'])

        return station_status_data
