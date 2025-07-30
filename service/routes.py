"""
Controller for routes
"""
import json
import os
from flask import jsonify, url_for, abort
from service import app
from service.common import status

COUNTERS_FILE = "counters.json"


# Function to load counters from file
def load_counters_from_file():
    """Loads counters from the JSON file"""
    if not os.path.exists(COUNTERS_FILE):
        return {}
    try:
        with open(COUNTERS_FILE, "r", encoding="utf-8") as json_file:
            return json.load(json_file)
    except json.JSONDecodeError:
        app.logger.warning(
            f"Error decoding {COUNTERS_FILE}. Init with empty counters."
        )  # noqa: E501
        return {}
    except Exception as ex:  # pylint: disable=broad-except
        app.logger.error(
            f"An unexpected error occurred while loading {COUNTERS_FILE}: {ex}"  # noqa: E501
        )
        return {}


# Function to save counters to file
def save_counters_to_file(data):
    """Saves counters to the JSON file"""
    try:
        with open(COUNTERS_FILE, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4)
    except Exception as ex:  # pylint: disable=broad-except
        app.logger.error(f"Err saving to {COUNTERS_FILE}: {ex}")


COUNTER = load_counters_from_file()


############################################################
# Health Endpoint
############################################################
@app.route("/health")
def health():
    """Health Status"""
    return jsonify(dict(status="OK")), status.HTTP_200_OK


############################################################
# Index page
############################################################
@app.route("/")
def index():
    """Returns information abut the service"""
    app.logger.info("Request for Base URL")
    return jsonify(
        status=status.HTTP_200_OK,
        message="Hit Counter Service",
        version="1.0.0",
        url=url_for("list_counters", _external=True),
    )


############################################################
# List counters
############################################################
@app.route("/counters", methods=["GET"])
def list_counters():
    """Lists all counters"""
    app.logger.info("Request to list all counters...")

    counters = [  # noqa: E501
        dict(name=count[0], counter=count[1]) for count in COUNTER.items()
    ]

    return jsonify(counters)


############################################################
# Create counters
############################################################
@app.route("/counters/<name>", methods=["POST"])
def create_counters(name):
    """Creates a new counter"""
    app.logger.info("Request to Create counter: %s...", name)

    if name in COUNTER:
        return abort(status.HTTP_409_CONFLICT, f"Counter '{name}' exists")

    COUNTER[name] = 0
    save_counters_to_file(COUNTER)

    location_url = url_for("read_counters", name=name, _external=True)
    return (
        jsonify(name=name, counter=0),
        status.HTTP_201_CREATED,
        {"Location": location_url},
    )


############################################################
# Read counters
############################################################
@app.route("/counters/<name>", methods=["GET"])
def read_counters(name):
    """Reads a single counter"""
    app.logger.info("Request to Read counter: %s...", name)

    if name not in COUNTER:
        return abort(status.HTTP_404_NOT_FOUND, f"Counter '{name}' not found")

    counter = COUNTER[name]
    return jsonify(name=name, counter=counter)


############################################################
# Update counters
############################################################
@app.route("/counters/<name>", methods=["PUT"])
def update_counters(name):
    """Updates a counter"""
    app.logger.info("Request to Update counter: %s...", name)

    if name not in COUNTER:
        return abort(status.HTTP_404_NOT_FOUND, f"Counter '{name}' not found")

    COUNTER[name] += 1
    save_counters_to_file(COUNTER)

    counter = COUNTER[name]
    return jsonify(name=name, counter=counter)


############################################################
# Delete counters
############################################################
@app.route("/counters/<name>", methods=["DELETE"])
def delete_counters(name):
    """Deletes a counter"""
    app.logger.info("Request to Delete counter: %s...", name)

    if name in COUNTER:
        COUNTER.pop(name)
        save_counters_to_file(COUNTER)

    return "", status.HTTP_204_NO_CONTENT


############################################################
# Utility for testing
############################################################
def reset_counters():
    """Removes all counters while testing"""
    global COUNTER  # pylint: disable=global-statement
    if app.testing:
        COUNTER = {}
        if os.path.exists(COUNTERS_FILE):
            try:
                os.remove(COUNTERS_FILE)
                app.logger.info(f"Removed {COUNTERS_FILE} during reset.")
            except Exception as ex:  # pylint: disable=broad-except
                app.logger.error(
                    f"Err removing {COUNTERS_FILE} during reset: {ex}"
                )  # noqa: E501
        # Or, alternatively, write an empty JSON object:
        # save_counters_to_file({})
