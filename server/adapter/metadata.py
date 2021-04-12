from collections import namedtuple
from odd_contract.models import MetadataExtension


# List[MetadataExtension(str, dict[str, object])]
def _append_metadata_extension(metadata_list: list[MetadataExtension],
                               schema_url: str, named_tuple: namedtuple, excluded_keys: set = None):
    if named_tuple is not None and len(named_tuple) > 0:
        metadata: dict = named_tuple._asdict()
        if excluded_keys is not None:
            for key in excluded_keys:
                metadata.pop(key)
        metadata_wo_none: dict = {}
        for key, value in metadata.items():
            if value is not None:
                metadata_wo_none[key] = value
        metadata_list.append(MetadataExtension(schema_url, metadata_wo_none))
