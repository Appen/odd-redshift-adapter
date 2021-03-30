from odd_contract.models import DataEntity, DataTransformer
from adapter import FunctionMetadataNamedtuple, _data_set_metadata_schema_url_function
from adapter.metadata import _append_metadata_extension
from adapter.type import FUNCTION_TYPES_SQL_TO_ODD
from app.oddrn import generate_function_oddrn, generate_schema_oddrn


def _map_function(data_source_oddrn: str, functions: list[tuple]) -> list[DataEntity]:
    data_entities: list[DataEntity] = []

    for function in functions:
        mfunction: FunctionMetadataNamedtuple = FunctionMetadataNamedtuple(*function)

        function_catalog: str = mfunction.database_name
        function_schema: str = mfunction.schema_name
        function_name: str = mfunction.function_name

        schema_oddrn: str = generate_schema_oddrn(data_source_oddrn, function_catalog, function_schema)
        function_oddrn: str = generate_function_oddrn(
            data_source_oddrn, function_catalog, function_schema, function_name)

        data_entity: DataEntity = DataEntity()
        data_entities.append(data_entity)

        data_entity.oddrn = function_oddrn
        data_entity.name = function_name
        data_entity.owner = schema_oddrn

        data_entity.metadata = []
        _append_metadata_extension(data_entity.metadata, _data_set_metadata_schema_url_function, mfunction)

        # data_entity.created_at = mfunction.create_time
        # data_entity.updated_at = mfunction.update_time

        data_entity.data_transformer = DataTransformer()

        # data_entity.data_transformer.description = mfunction.remarks
        # data_entity.data_transformer.source_code_url = None
        data_entity.data_transformer.sql = mfunction.prosrc

        if mfunction.argument_type is not None:
            data_entity.data_transformer.inputs = mfunction.argument_type.split(', ')
        if mfunction.result_type is not None:
            data_entity.data_transformer.outputs = mfunction.result_type.split(', ')

        data_entity.data_transformer.subtype = FUNCTION_TYPES_SQL_TO_ODD[mfunction.function_type] \
            if mfunction.function_type in FUNCTION_TYPES_SQL_TO_ODD \
            else 'DATATRANSFORMER_JOB'  # DATATRANSFORMER_UNKNOWN

    return data_entities
