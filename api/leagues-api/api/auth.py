from flask import request, Response, current_app
from functools import wraps
import json
import logging
from firebase_admin import auth
def loggedIn(func):
    @wraps(func)
    def check_token(*args, **kwargs):
        if current_app.config['DISABLE_AUTH']:
            return func(*args, **kwargs)
        elif "X-Forwarded-Authorization" in request.headers:
            logging.debug("Heder")
            logging.debug(request.headers)
            authstr = str(request.headers['X-Forwarded-Authorization'])
            
            authArr = authstr.split(" ")

            token = ''

            if( len(authArr) == 2):
                token = authArr[1]

                if token == 'undefined':
                    logging.warn("Authorization token is undefined")

                logging.debug("Authorizaton token: " + token)

                try:
                    user=None
                    user = auth.verify_id_token(token)
                    
                    if user:
                        request.user = user
                        logging.info(f"User: {request.user}")
                    else:
                        logging.warn("validateToken failed")
                        return Response(status=401)

                        
                except Exception as ex:
                    logging.warn(f"{ex}")
                    return Response(status=401)

        elif "Authorization" in request.headers:

            authstr = str(request.headers['Authorization'])
        
            authArr = authstr.split(" ")

            token = ''

            if( len(authArr) == 2):
                token = authArr[1]

                if token == 'undefined':
                    logging.warn("Authorization token is undefined")

                logging.debug("Authorizaton token: " + token)

                try:
                    user=None
                    user = auth.verify_id_token(token)
                    
                    if user:
                        request.user = user
                        logging.info(f"User: {request.user}")
                    else:
                        logging.warn("validateToken failed")
                        return Response(status=401)

                        
                except Exception as ex:
                    logging.warn(f"{ex}")
                    return Response(status=401)

            else:
                logging.warn("Authorization header is not formatted correctly")
                logging.debug("Authorization header: " + auth)
                return Response(status=401)

        else:
            logging.warn("No Authorization key in request header")
            return Response(status=401)

        return func(*args, **kwargs)
    return check_token