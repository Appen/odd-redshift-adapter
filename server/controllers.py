import logging

from datetime import datetime
from typing import List, Tuple, Any, Dict

import pytz
from flask import Response
from odd_contract import ODDController
from odd_contract.encoder import JSONEncoder

from cache import RedshiftDataCache
from oddrn import generate_catalog_oddrn


class OpenDataDiscoveryController(ODDController):
    __encoder = JSONEncoder()
    __empty_cache_response = Response(status=503, headers={"Retry-After": "30"})

    def __init__(self, host_name: str, redshift_data_cache: RedshiftDataCache):
        self.__host_name = host_name
        self.__redshift_data_cache = redshift_data_cache

    def get_data_entities(self, changed_since: Dict[str, Any] = None):
        try:
            changed_since = pytz.UTC.localize(datetime.strptime(changed_since["changed_since"], "%Y-%m-%dT%H:%M:%SZ")) \
                if changed_since["changed_since"] is not None and changed_since["changed_since"] != "" else None
        except Exception:
            changed_since = None

        data_entities = self.__redshift_data_cache.retrieve_data_entities(changed_since=changed_since)

        if data_entities is None:
            logging.warning("DataEntities cache has never been enriched")
            return self.__empty_cache_response
        else:
            if data_entities[0] is not None:
                logging.info(f"Get {len(data_entities[0])} DataEntities from cache to endpoint")
            else:
                logging.warning(f"Get empty DataEntities from cache to endpoint")

        return self.__build_response(data_entities)

    def __build_response(self, data: Tuple[List, datetime]):
        return Response(
            response=self.__encoder.encode({
                "data_source_oddrn":
                    generate_catalog_oddrn(self.__redshift_data_cache.retrieve_aws_account(), self.__host_name),
                "items":
                    data[0]
            }),
            headers={"Last-Modified": data[1].strftime("%a, %d %b %Y %H:%M:%S GMT")},
            content_type="application/json",
            status=200
        )
