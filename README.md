# OpenDataDiscovery Redshift adapter (ODD Redshift adapter)

Version: 0.0.1

## OpenDataDiscovery Redshift adapter scope

ODD Redshift adapter is used OpenDataDiscovery for pull metadata to OpenDataDiscovery from AWS Amazon Redshift.

Metadata discovery process is very similar to metrics/logs/traces gathering process. We might have pull or push model.
OpenDataDiscovery use pull model for ODD Redshift adapter.

Pulling metadata directly from the source seems is the most straightforward way to gather metadata,
but it may become a nightmare to develope and maintain a centralized fleet of domain-specific crawlers.
OpenDataDiscovery introduces new entity: OpenDataDiscovery Adapter. In this case, ODD Redshift adapter.
The main goal of these adapters are to be source specific and expose only information
could be gathered from certain data source.

## Deployment

ODD Redshift adapter is Python Flask application composed to Docker image.
Web server is gunicorn. DB API library is psycopg2.
For details about image see docker-compose.yml and Dockerfile. Use this files for local tests and development.
In production Kubernetes on Amazon EKS (Amazon Elastic Kubernetes Service) can be used to run ODD Redshift adapter.
See Helm Charts files for example.

### Endpoint http://0.0.0.0:8080/entities/

ODD Redshift adapter start endpoint http://0.0.0.0:8080/entities/ by default,
and it connects to Redshift for collect metadata.  
ODD Redshift adapter provides list of available metadata entities updated after changed_since time.

### Environmental variables

ODD Redshift adapter used next environmental variables:

Cache refreshing interval (minutes), default 60:
- SCHEDULER_INTERVAL_MINUTES=60

ODD Redshift adapter used PostgreSQL driver and setting for it:
- ODD_DATA_SOURCE_NAME=odd-redshift-adapter.c4oxusiab5jk.eu-central-1.redshift.amazonaws.com
- ODD_DATA_SOURCE=postgresql://
- PGHOST=odd-redshift-adapter.c4oxusiab5jk.eu-central-1.redshift.amazonaws.com
- PGPORT=5439
- PGDATABASE=oddadapter
- PGUSER=oddadapter
- PGPASSWORD=odd-adapter-password

ODD_DATA_SOURCE_NAME is last part of DataEntityList.data_source_oddrn. By default, PGHOST.

ODD_DATA_SOURCE is full or part of Connection String. By default, "postgresql://".  
There are two accepted formats for ODD_DATA_SOURCE: plain keyword = value strings and URIs.  
Plain keyword = value strings example:  
```host=...redshift.amazonaws.com port=5439 dbname=oddadapter connect_timeout=10```  
The general form for a connection URI is:  
```postgresql://[user[:password]@][host][:port][,...][/dbname][?param1=value1&...]```  
```postgresql://oddadapter:odd-adapter-password@odd-redshift-adapter.c4oxusiab5jk.eu-central-1.redshift.amazonaws.com:5439/oddadapter?connect_timeout=10```

Or you can use additional variables:  
Redshift endpoint host (host keyword) - PGHOST=odd-redshift-adapter.c4oxusiab5jk.eu-central-1.redshift.amazonaws.com  
Redshift endpoint/database port (port keyword) - PGPORT=5439  
Redshift database name (dbname keyword) - PGDATABASE=oddadapter  
Username - PGUSER=oddadapter  
Password - PGPASSWORD=odd-adapter-password

More details see https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING

Variables for FLASK see in FLASK documentation, for example:
- FLASK_ENVIRONMENT=development

## DataModel

Knowledge about data is spread amongst many people and systems.
OpenDataDiscovery role is to provide a standard protocol how metadata can be collected and
correlated in as automated fashion as possible.
To enable many different datasources and tools to expose the metadata we need agreement
on what data should be exposed and in what format (structures).
Specification contains of high level entities:
- DataInput,
- DataTransformer (DataTransformerRun),
- DataSet
- DataQualityTest (DataQualityTest)
- DataConsumer.

Each entity has a unique url describing a place, system and an identifier in this system.

ODD Redshift adapter map Amazon Redshift metadata to OpenDataDiscovery metadata by Specification.
Mapping details and examples see below.

### BaseObject, DataEntity, DataEntityList, MetadataExtension

BaseObject and DataEntity is base components for other metadata components.
DataEntityList is list all types of DataEntity and it has data_source_oddrn.

Format ODDRN:
- DataEntityList.data_source_oddrn  
  format: f'//aws/123456789012/redshift/{ODD_DATA_SOURCE_NAME}'  
  example: "//aws/123456789012/redshift/odd-redshift-adapter.c0mxpzchxkqz.us-west-2.redshift.amazonaws.com"
- DataSet.parent_oddrn  
  format: f'{data_source_oddr}/databases/{catalog_name}/schemas/{schema_name}'  
  example: "//aws/123456789012/redshift/odd-redshift-adapter.c0mxpzchxkqz.us-west-2.redshift.amazonaws.com/databases/oddadapter/schemas/smith"
- BaseObject.oddrn for DataSet, DataSetField.parent_field_oddrn  
  format: f'{data_source_oddr}/databases/{catalog_name}/schemas/{schema_name}/tables/{table_name}'  
  example: "//aws/123456789012/redshift/odd-redshift-adapter.c0mxpzchxkqz.us-west-2.redshift.amazonaws.com/databases/oddadapter/schemas/public/tables/event"
- BaseObject.oddrn for DataSetField  
  format: f'{dataset_oddr}/columns/{column_name}'  
  example: "//aws/123456789012/redshift/odd-redshift-adapter.c0mxpzchxkqz.us-west-2.redshift.amazonaws.com/databases/oddadapter/schemas/public/tables/event/columns/eventid"
- BaseObject.oddrn for DataTransformer  
  format: f'{data_source_oddr}/databases/{catalog_name}/schemas/{schema_name}/tables/{view_name}'  
  example: "//aws/123456789012/redshift/odd-redshift-adapter.c0mxpzchxkqz.us-west-2.redshift.amazonaws.com/databases/oddadapter/schemas/public/tables/event_all"


Format DataEntity.created_at, DataEntity.updated_at and other values of datetime type:  
format: %Y-%m-%dT%H:%M:%S.ssssss  
example: 2021-03-25T06:12:13.488486  
python: datetime.isoformat()

MetadataExtension.schema_url field use definitions from file schema:  
https://raw.githubusercontent.com/opendatadiscovery/opendatadiscovery-specification/main/specification/extensions/redshift.json

### DataSet, DataSetField, DataSetFieldType

DataSet is a collection of data stored in structured format.
In ODD Redshift adapter DataSet might be a base table, view, materialized view, external table,
external view, external materialized view.

Redshift views PG_CATALOG.SVV_TABLES, PG_CATALOG.SVV_ALL_TABLES, PG_CATALOG.SVV_REDSHIFT_TABLES, PG_CATALOG.SVV_EXTERNAL_TABLES, PG_CATALOG.SVV_TABLE_INFO
maps to DataSet (and BaseObject, DataEntity, MetadataExtension) entities.

Redshift views PG_CATALOG.SVV_ALL_COLUMNS, PG_CATALOG.SVV_REDSHIFT_COLUMNS, PG_CATALOG.SVV_EXTERNAL_COLUMNS
maps to DataSetField, DataSetFieldType (and BaseObject, DataEntity, MetadataExtension) entities.


### DataTransformer

Redshift views maps to DataTransformer entity (and Dataset too).  
Column pg_catalog.svv_tables.remarks maps to DataTransformer.description.  
DataTransformer.source_code_url field is not used.  
DataTransformer.inputs field is not used (="").  
DataTransformer.outputs field is not used (="").  
Column pg_get_viewdef(pg_catalog.pg_class_info.reloid, true) maps to DataTransformer.sql field.  
DataTransformer.subtype field = DATATRANSFORMER_VIEW.  

Amazon Redshift has next types of DataTransformer:
- view,
- materialized view,
- external view,
- external materialized view

#### DataSetStat, DataSetFieldStat
#### BooleanFieldStat, ComplexFieldStat, NumberFieldStat, StringFieldStat, BinaryFieldStat, IntegerFieldStat, DateTimeFieldStat

Redshift adapter get statistic data from Redshift tables and views to BooleanFieldStat, ComplexFieldStat, 
NumberFieldStat, StringFieldStat, BinaryFieldStat, IntegerFieldStat, DateTimeFieldStat entities.

### Not used:
#### DataTransformerRun
#### DataInput, DataConsumer
#### DataSetQualityTest, DataQualityTestRun
#### LinkedUrl
