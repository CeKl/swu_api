"""swu_api

Python libary for the use of the public transport and carsharing API of the Stadtwerke Ulm / Neu-Ulm (SWU).

Collection of functions that help in processing and requesting API data.

MIT License
Copyright (c) 2021 Cedric Klimt

"""

from swu_api.swu_fuctions import swu_pt_functions
from swu_api.swu_fuctions import swu_cs_functions
from reptaskorg import RepTaskOrgTH


class SearchParameterError(Exception):
    """Custom Exception - search parameter."""

    def __init__(self):
        message = 'Unvailde serach_parameter. Use StopPointCode or StopNumber.'
        super().__init__(message)


class NoElementError(Exception):
    """Custom Exception - serach parameter."""

    def __init__(self, search_data):
        message = 'No data found. Check requested data {data}.'.format(
            data=search_data)
        super().__init__(message)


class NoStationError(Exception):
    """Custom Exception - station id."""

    def __init__(self, station_id):
        message = 'No station with station id {station_id} found.'.format(
            station_id=station_id)
        super().__init__(message)


class swu_api_pt_helper():
    """Functions to help with the SWU-API for public transport."""

    def __init__(self, use_buffer=True, buffer_refresh_time=None):
        """Set startvalues and setup buffer.

        Args:
            use_buffer (bool, optional): Use buffer to reduce requests. Defaults to True.
            buffer_refresh_time (list, optional): Interval to update buffer in minutes. For details see reptaskorg. Defaults to None = [0, 30].
        """

        self.swu_api_pt_instance = swu_pt_functions()

        if use_buffer:
            self.buffer = True
            self.buffer_base_stop = {}
            self.buffer_base_vehicle = {}
            self.buffer_base_route = {}

            if buffer_refresh_time is None:
                buffer_refresh_time = [0, 30]

            self.buffer_refresh_task = RepTaskOrgTH(
                self.refersh_buffer, minute=buffer_refresh_time)

            self.refersh_buffer()

        else:
            self.buffer = False

    def refersh_buffer(self):
        """Fill buffer with new data."""

        self.buffer_base_stop = self.__swu_base_stop()
        self.buffer_base_vehicle = self.__swu_base_vehicle()
        self.buffer_base_route = self.__swu_base_route()

        print('public transport buffer refresh done')

    def __swu_base_stop(self):
        return self.swu_api_pt_instance.base_stop(stopnumber=0, contentscope='extended')

    def __swu_base_vehicle(self):
        return self.swu_api_pt_instance.base_vehicle(vehiclenumber=0, contentscope='extended')

    def __swu_base_route(self):
        return self.swu_api_pt_instance.base_route(routenumber=0, contentscope='extended')

    def get_station_info(self, serach_parameter, serach_term):
        """Get basic data of a station with searchterm for searchparameter.

        Args:
            serach_parameter (str): Parameter to serach. Use StopPointCode, StopNumber or StopName.
            serach_term (str): Term to serach for parameter.

        Raises:
            SearchParameterError: Unvailde serach parameter.

        Returns:
            dict: Data for requested station.
        """

        output = {}

        if serach_parameter not in ['StopPointCode', 'StopNumber', 'StopName']:
            raise SearchParameterError()

        if self.buffer:
            search_data = self.buffer_base_stop['StopAttributes']['StopData']
        else:
            search_data = self.__swu_base_stop()['StopAttributes']['StopData']

        for _, entry in enumerate(search_data):
            if serach_parameter in ['StopNumber', 'StopName']:
                if entry[serach_parameter] == serach_term:
                    output = entry
                    break
            else:
                for _, stoppoint_entry in enumerate(entry['StopPoints']):
                    if stoppoint_entry['StopPointCode'] == serach_term:
                        output = entry
                        break

        return output

    def get_vehicle_info(self, vehiclenumber):
        """Get basic data of a vehicle.

        Args:
            vehiclenumber (int): Number of the vehicle.

        Raises:
            NoElementError: No entry found in data.

        Returns:
            dict: Data for requested vehicle.
        """

        output = {}

        if self.buffer:
            search_data = self.buffer_base_vehicle['VehicleAttributes']['VehicleData']
        else:
            search_data = self.__swu_base_vehicle(
            )['VehicleAttributes']['VehicleData']

        for _, entry in enumerate(search_data):
            if entry['VehicleNumber'] == vehiclenumber:
                output = entry
                break

        if output == {}:
            raise NoElementError(search_data)

        return output

    def get_route_direction(self, routenumber):
        """Get direcction of a route.

        Args:
            routenumber (int): Number of the route.

        Raises:
            NoElementError: No entry found in data.

        Returns:
            dict: Data for requested routedirection.
        """

        output = {}

        if self.buffer:
            search_data = self.buffer_base_route['RouteAttributes']['RouteData']
        else:
            search_data = self.__swu_base_route(
            )['RouteAttributes']['RouteData']

        for _, entry in enumerate(search_data):
            if entry['RouteNumber'] == routenumber:
                output = entry['RouteDirections']
                break

        if output == {}:
            raise NoElementError(search_data)

        return output

    def get_route(self, routenumber, direction):
        """Get route for given routenumber an direction.

        Args:
            routenumber (int): Number of the route.
            direction (int): Direction of the route. For details see get_route_direction().

        Raises:
            NoElementError: No entry found in data.

        Returns:
            dict: Data for the requested route.
        """

        output = {}

        if self.buffer:
            search_data = self.buffer_base_route['RouteAttributes']['RouteData']
        else:
            search_data = self.__swu_base_route(
            )['RouteAttributes']['RouteData']

        for _, entry in enumerate(search_data):
            if entry['RouteNumber'] == routenumber:
                for _, direction_entry in enumerate(entry['RoutePattern']):
                    if direction_entry['PatternDirection'] == direction:
                        output = direction_entry['StopPoints']
                        break

        if output == {}:
            raise NoElementError(search_data)

        return output


class swu_api_cs_helper():
    """Functions to help with the SWU-API for carsharing."""

    def __init__(self, use_buffer=True, buffer_refresh_time=None):
        """Set startvalues and setup buffer.

        Args:
            use_buffer (bool, optional): Use buffer to reduce requests. Defaults to True.
            buffer_refresh_time (list, optional): Interval to update buffer in minutes. For details see reptaskorg. Defaults to None = [0, 30].
        """

        self.swu_api_cs_instance = swu_cs_functions()

        if use_buffer:
            self.buffer = True
            self.buffer_station_info = {}
            self.buffer_station_status = {}

            if buffer_refresh_time is None:
                buffer_refresh_time = [0, 30]

            self.buffer_refresh_task = RepTaskOrgTH(
                self.refersh_buffer, minute=buffer_refresh_time)

            self.refersh_buffer()

        else:
            self.buffer = False

    def refersh_buffer(self):
        """Fill buffer with new data."""

        self.buffer_station_info = self.__swu_station_info()
        self.buffer_station_status = self.__swu_station_status()

        print('carsharing buffer refresh done')

    def __swu_station_info(self):
        return self.swu_api_cs_instance.station_info()

    def __swu_station_status(self):
        return self.swu_api_cs_instance.station_status()

    def get_station_details(self, station_id):
        """Get details of a station for a given station id.

        Args:
            station_id (str): Id of station.

        Raises:
            NoStationError: Station id not found.

        Returns:
            dict: Data for requested station.
        """

        output = {}

        if self.buffer:
            search_data_1 = self.buffer_station_info['data']['stations']
            search_data_2 = self.buffer_station_status['data']['stations']
        else:
            search_data_1 = self.__swu_station_info()['data']['stations']
            search_data_2 = self.__swu_station_status()['data']['stations']

        for _, entry in enumerate(search_data_1):
            if entry['station_id'] == station_id:
                output = entry
                break

        for _, entry in enumerate(search_data_2):
            if entry['station_id'] == station_id:
                output.update(entry)
                break

        if output == {}:
            raise NoStationError(station_id)

        return output
