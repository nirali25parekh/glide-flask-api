from flask import Flask, request,jsonify
from video_indexer import VideoIndexer
import json as json
from flask_cors import CORS,cross_origin
import config

CONFIG = {
    'SUBSCRIPTION_KEY': config.VI_SUBSCRIPTION_KEY,
    'LOCATION': config.VI_LOCATION,
    'ACCOUNT_ID': config.VI_ACCOUNT_ID
}

vi = VideoIndexer(
    vi_subscription_key=CONFIG['SUBSCRIPTION_KEY'],
    vi_location=CONFIG['LOCATION'],
    vi_account_id=CONFIG['ACCOUNT_ID']
)


def upload_file(f):
    if request.method == 'POST':
        f.save(f.filename)
        name=f.filename
        return name


def createinstance(name,language):
    video_id = vi.upload_to_video_indexer(
        input_filename=f'{name}',
        video_name=f'{name}',  # identifier for video in Video Indexer platform, must be unique during indexing time
        video_language=language
    )
    return video_id


def indexvideo(video_id,language):
    info = vi.get_video_info(
        video_id,
        video_language=language
    )
    return info


