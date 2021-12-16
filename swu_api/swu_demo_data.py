"""swu_api

Python libary for the use of the public transport and carsharing API of the Stadtwerke Ulm / Neu-Ulm (SWU) more.

Save SWU-API data from requests to json file for further analysis.

MIT License
Copyright (c) 2021 Cedric Klimt

"""


import json
from swu_api.swu_fuctions import swu_pt_functions


class FilterError(Exception):
    """Custom Exception - Save filter."""

    def __str__(self):
        return 'Unvailde save_filter. Use all, base or live.'


class api_to_json():
    """Save SWU API data to json file."""

    def __init__(self, save_filter, folderpath):

        self.folderpath = folderpath

        if save_filter == 'all':
            __get_filter = 0
        elif save_filter == 'base':
            __get_filter = 1
        elif save_filter == 'live':
            __get_filter = 2
        else:
            raise FilterError()

        if __get_filter in [0, 1]:
            self.__save_as_json(
                data=swu_pt_functions.base_route(
                    routenumber='', contentscope='extended'),
                filename='base_route')

            self.__save_as_json(
                data=swu_pt_functions.base_stop(
                    stopnumber=0, contentscope='extended'),
                filename='base_stop')

            self.__save_as_json(
                data=swu_pt_functions.base_stop_point(
                    stoppointcode=0, contentscope='extended'),
                filename='base_stop_point')

            self.__save_as_json(
                data=swu_pt_functions.base_vehicle(
                    vehiclenumber=0, contentscope='extended'),
                filename='base_vehicle')

        if __get_filter in [0, 2]:
            self.__save_as_json(
                data=swu_pt_functions.live_stop_departures(
                    stopnumber=1000, limit=5),
                filename='live_stop_departures')

            self.__save_as_json(
                data=swu_pt_functions.live_stop_arrivals(
                    stopnumber=1000, limit=5),
                filename='live_stop_arrivals')

            self.__save_as_json(
                data=swu_pt_functions.live_stop_point_departures(
                    stoppointcode=130011, limit=5),
                filename='live_stop_point_departures')

            self.__save_as_json(
                data=swu_pt_functions.live_stop_point_arrivals(
                    stoppointcode=130011, limit=5),
                filename='live_stop_point_arrivals')

            self.__save_as_json(
                data=swu_pt_functions.live_vehicle_trip(vehiclenumber=42),
                filename='live_vehicle_trip')

            self.__save_as_json(
                data=swu_pt_functions.live_vehicle_passage(
                    vehiclenumber=42, range_value='all'),
                filename='live_vehicle_passage')

            self.__save_as_json(
                data=swu_pt_functions.live_vehicle_pattern(
                    vehiclenumber=42, contentscope='Track'),
                filename='live_vehicle_pattern')

    def __save_as_json(self, data, filename):
        """Save data in json files.

        Args:
            data (dict): Data in json-dict format.
            filename (str): Name of file to save.
        """

        if filename[-5:] == '.json':
            filename = filename[:-5]

        filepath = "{folderpath}/{filename}.json".format(
            folderpath=self.folderpath,
            filename=filename)

        json_object = json.dumps(data, indent=4, ensure_ascii=False)

        with open(filepath, "w", encoding='utf-8') as outfile:
            outfile.write(json_object)
