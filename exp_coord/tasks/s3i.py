from s3i.client import S3IClient

def check_s3i_message_queue(s3i_client: S3IClient):
    messages = s3i_client.receiveMessage()