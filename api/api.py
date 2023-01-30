from flask import make_response, jsonify, request, Blueprint, current_app
import housecanary
import json

bp = Blueprint('api', __name__)
house_canary_client = None

def getHouseCanaryClient():
    global house_canary_client
    if house_canary_client is None:
        api_key = current_app.config.get('HOUSE_CANARY_API_KEY')
        secret_key = current_app.config.get('HOUSE_CANARY_SECRET_KEY')
        house_canary_client = housecanary.ApiClient(api_key, secret_key)
    return house_canary_client



def call_house_canary(street_address, zipcode):
    api_response = getHouseCanaryClient().property.details((street_address, zipcode))
    return api_response.json()

def process_results(api_response):
    # Success Case
    if 'result' in api_response.keys():
        results = api_response['result']
        if results != None and 'property' in results.keys():
            property = results['property']
            if 'sewer' in property.keys():
                sewer_type = property['sewer']
                has_septic = False
                if sewer_type == 'septic':
                    has_septic = True

                #return successful
                return make_response(jsonify({'has_septic' : has_septic}), 200)

        # if results were returned, without sewer information, 204 error
        error_code = 204
        error_message = 'Septic status unknown for this address'
        return make_response(jsonify({'message': error_message}), error_code)
    elif 'message' in api_response.keys():
        if api_response['message'] == "Authentication Failed" and api_response['code'] == 401:
            error_code = 401
            error_message = "Authentication Failed with Home Canary API"
        elif api_response['message'] == 'Too Many Requests':
            error_code = 429
            error_message = 'Rate limit reached for Home Canary API. Try again later.'
        else:
            error_code = 400
            error_message = api_response['message']

    return make_response(jsonify({'message': error_message}), error_code)


def get_json(filename):
    with open (filename) as data:
        return json.load(data)
    return json.dumps({})

@bp.route('/has-septic-system')
def has_septic_system():
    # TODO: Add authentication check in the future
    street_address = request.args['address']
    zipcode = request.args['zipcode']

    optional_test_data = None
    if 'testData' in request.args:
        optional_test_data = request.args['testData']

    # TODO: Add address verification here in the future

    if optional_test_data == None:
        # call 3P api
        response =  process_results(call_house_canary(street_address, zipcode))
    else:
        # grab test data
        response = process_results(get_json('api/mockdata/' + optional_test_data + '.json'))

    response.headers["Content-Type"] = "application/json"
    return response
