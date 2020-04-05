"""Fit Activities: Purely raw, non-aggregated fit data 

Fit_Activities:
    Activity: rawfile, activity_num, Sport, Id, Notes
    Lap: rawfile, activity_num, lap_num, DistanceMeters, TotalTimeSeconds, Calories, Intensity, TriggerMethod
    Trackpoint: rawfile, activity_num, trackpoint_num, Distance, Time, AltitudeMeters
    Position: rawfile, activity_num, lap_num, trackpoint_num,  Latitude, Longitude
"""

import logging

from collections import defaultdict
from typing import List
import xml.etree.ElementTree as ET

from google_takeout.stage.products.base import ProductExtractor

NAMESPACE = {"Activities": "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"}
TABLE_XML = {
    "fit_activities_activity": {"attributes": ["Sport"], "texts": ["Id", "Notes"]},
    "fit_activities_lap": {
        "attributes": ["StartTime"],
        "texts": [
            "DistanceMeters",
            "TotalTimeSeconds",
            "Calories",
            "Intensity",
            "TriggerMethod",
        ],
    },
    "fit_activities_trackpoint": {
        "texts": ["DistanceMeters", "Time", "AltitudeMeters",]
    },
    "fit_activities_position": {"texts": ["LatitudeDegrees", "LongitudeDegrees"]},
}

LOG = logging.getLogger(__name__)


class FitActivities(ProductExtractor):
    folder_location = "Fit/Activities"
    tables = list(TABLE_XML.values())

    @staticmethod
    def get_xml_root(rawfile: str) -> ET:
        tree = ET.parse(rawfile)
        return tree.getroot()

    @staticmethod
    def find_from_root(root: ET, child: str) -> List["ET"]:
        return root.find(f"Activities:{child}", NAMESPACE)

    @staticmethod
    def findall_from_root(root: ET, child: str) -> List["ET"]:
        return root.findall(f"Activities:{child}", NAMESPACE)

    def get_text_values(self, root: ET, values: List[str]) -> dict:
        res = {}
        for value in values:
            try:
                res[value] = self.find_from_root(root, value).text
            except AttributeError:
                res[value] = None
        return res

    @staticmethod
    def get_attrib_values(root: ET, values: List[str]) -> dict:
        return {value: root.attrib.get(value) for value in values}

    def add_root_dict(
        self, data: dict, root: ET, tablename: str, table_xml: dict = TABLE_XML, **extra
    ) -> dict:
        if not root:
            return data

        attributes = table_xml.get(tablename).get("attributes") or []
        texts = table_xml.get(tablename).get("texts") or []
        data[tablename].append(
            {
                **self.get_attrib_values(root, attributes),
                **self.get_text_values(root, texts),
                **extra,
            }
        )
        return data

    def _parse_trackpoints(self, data: dict, root: ET, **extras):
        track = self.find_from_root(root, "Track")
        for t, trackpoint in enumerate(self.findall_from_root(track, "Trackpoint")):
            extras["trackpoint_num"] = t
            data = self.add_root_dict(
                data, trackpoint, "fit_activities_trackpoint", **extras,
            )

            position = data, self.find_from_root(trackpoint, "Position")
            data = self.add_root_dict(
                data, position, "fit_activities_position", **extras,
            )
        return data

    def _parse_laps(self, data: dict, root: ET, **extras):
        for l, lap in enumerate(self.findall_from_root(root, "Lap")):
            extras["lap_num"] = l
            data = self.add_root_dict(data, lap, "fit_activities_lap", **extras)
            data = self._parse_trackpoints(data, lap, **extras)
        return data

    def _parse_activities(self, data: dict, root: ET, **extras):
        activities = self.find_from_root(root, "Activities")
        for a, activity in enumerate(self.findall_from_root(activities, "Activity")):
            extras["activity_num"] = a
            data = self.add_root_dict(
                data, activity, "fit_activities_activity", **extras
            )
            data = self._parse_laps(data, activity, **extras)

        return data

    def parse_file(self, rawfile: str):
        LOG.info(f"Parsing file {rawfile}")

        root = self.get_xml_root(rawfile)
        res = self._parse_activities(defaultdict(list), root, rawfile=rawfile)

        LOG.info(
            "Found {0:,} activities, {1:,} laps, {2:,} trackpoints, {3:,} positions".format(
                len(res["fit_activities_activity"]),
                len(res["fit_activities_lap"]),
                len(res["fit_activities_trackpoint"]),
                len(res["fit_activities_position"]),
            )
        )
        return res
