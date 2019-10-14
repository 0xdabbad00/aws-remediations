import app.logging
import boto3
from urllib.parse import unquote_plus
import s3fs
from pyarrow.filesystem import S3FSWrapper
import pyarrow.parquet as pq

logger = app.logging.get_logger()
s3client = boto3.client('s3')
fs = s3fs.S3FileSystem()


def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        bucket_uri = 's3://{}/{}'.format(bucket, key)
        logger.info('Got Event %s %s', bucket, key)
        # readobject = s3client.get_object(Bucket=bucket, Key=key)
        # pyarrow.parquet.read_table()
        # reader = pyarrow.ipc.open_file(readobject['Body'])
        dataset = pq.ParquetDataset(bucket_uri, filesystem=fs)
        table = dataset.read()
        logger.info('Found stuff {}'.format(table.num_rows))
