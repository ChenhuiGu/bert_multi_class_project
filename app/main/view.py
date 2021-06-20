import traceback
from flask import request
from app.main import main
from utils.srf_log import logger


@main.route('/index', methods=['GET','POST'])
def credit_answer():
    try:
        pass
    except Exception as e:
        logger.error('url: %s, exception: %s', request.url, traceback.format_exc())



























