from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = next((it for it in data if it['id'] == id), None)
    if picture:
        return jsonify(picture), 200
    else:
        return jsonify({'error': 'Picture not found'}), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.get_json()
    print(picture)
    pictureExists = next((item for item in data if item['id'] == picture['id']), None)
    if pictureExists:
        return jsonify({'Message': f"picture with id {picture['id']} already present"}), 302
    else:
        data.append(picture)
        return jsonify({'id': picture['id']}), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture = request.get_json()
    updatedPicture = next((item for item in data if item['id'] == id), None)
    if updatedPicture:
        # Update the existing picture with the new data
        updatedPicture.update(picture)
        return jsonify({'message': f'Picture with id {id} updated successfully'}), 200
    else:
        return jsonify({'message': 'Picture not found'}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    global data
    deletedPicture = next((item for item in data if item['id'] == id), None)
    if deletedPicture:
        # Delete the picture from the data list
        data = [item for item in data if item['id'] != id]
        return jsonify({}), 204  # No content (HTTP_204_NO_CONTENT)
    else:
        return jsonify({'message': 'Picture not found'}), 404
