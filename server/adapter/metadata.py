from collections import namedtuple
from odd_contract.models import MetadataExtension


# List[MetadataExtension(str, dict[str, object])]
def _append_metadata_extension(metadata_list: list[MetadataExtension],
                               schema_url: str, named_tuple: namedtuple):
    if named_tuple is not None:
        metadata_list.append(MetadataExtension(schema_url, named_tuple._asdict()))
