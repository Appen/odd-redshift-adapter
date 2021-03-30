from odd_contract.models import DataEntity, DataTransformerRun
from adapter import CallMetadataNamedtuple, _data_set_metadata_schema_url_call
from adapter.metadata import _append_metadata_extension
# from adapter.type import CALL_TYPES_SQL_TO_ODD
from app.oddrn import generate_call_oddrn  # , generate_function_oddrn, generate_schema_oddrn


def _map_call(data_source_oddrn: str, calls: list[tuple]) -> list[DataEntity]:
    data_entities: list[DataEntity] = []

    for call in calls:
        mcall: CallMetadataNamedtuple = CallMetadataNamedtuple(*call)

        call_catalog: str = mcall.database.strip()
        # call_schema: str = mcall.schema_name
        call_name: str = mcall.querytxt.strip()
        # function_schema: str = mcall.function_schema
        # function_name: str = mcall.function_name

        # schema_oddrn: str = generate_schema_oddrn(data_source_oddrn, call_catalog, call_schema)
        call_oddrn: str = generate_call_oddrn(data_source_oddrn, call_catalog, call_name)

        data_entity: DataEntity = DataEntity()
        data_entities.append(data_entity)

        data_entity.oddrn = call_oddrn
        data_entity.name = call_name
        # data_entity.owner = schema_oddrn

        data_entity.metadata = []
        _append_metadata_extension(data_entity.metadata, _data_set_metadata_schema_url_call, mcall)

        data_entity.created_at = mcall.starttime
        data_entity.updated_at = mcall.endtime

        data_entity.data_transformer_run = DataTransformerRun()

        # data_entity.data_transformer_run.transformer_oddrn = \
        #     generate_function_oddrn(data_source_oddrn, call_catalog, function_schema, function_name)
        data_entity.data_transformer_run.start_time = mcall.starttime
        data_entity.data_transformer_run.end_time = mcall.endtime
        # data_entity.data_transformer.status_reason = mcall.status_reason
        if mcall.aborted is not None:
            data_entity.data_transformer_run.status = 'ABORTED' if mcall.aborted == 1 else 'SUCCESS'

    return data_entities
