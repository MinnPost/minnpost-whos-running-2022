import json
import boto3
from flask import jsonify, Response, current_app
from src.extensions import cache
from src import spreadsheet
from src.candidate_tracker import bp
#from src.candidate_tracker.errors import bad_request

@bp.route("/", methods=['GET'])
@cache.cached(timeout=30, query_string=True)
def index():
    output = spreadsheet.parser()
    
    mime = 'application/json'
    ctype = 'application/json; charset=UTF-8'

    res = Response(response = output, status = 200, mimetype = mime)
    res.headers['Content-Type'] = ctype
    res.headers['Connection'] = 'keep-alive'
    return res

@bp.route("/push-s3", methods=['GET'])
def push_to_s3():
  output = spreadsheet.parser()
  s3 = boto3.client('s3')
  s3.put_object(Bucket="data.minnpost", 
                Key="projects/minnpost-whos-running-2022/candidate-tracker.json", 
                Body=output,
                ContentType='application/json; charset=UTF-8',
                ACL="public-read")
  return "Uploaded candidate-tracker.json to S3"
