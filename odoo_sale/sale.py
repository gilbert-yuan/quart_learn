from quart import abort, Blueprint, current_app, jsonify, request

app = Quart(__name__)

@blueprint.route('/sale/', methods=['POST'])
async def check_status():
    return jsonify({'message': 'error'})

