#!/usr/bin/python3
""" Starts a Flask web application. """

from flask import Flask, render_template
from models import storage
from models.state import state
from sqlalchemy.orm import scoped_session, sessionmaker

# creates an instance of the Flask class and assigns it to the variable app
app = Flask(__name__)

# Teardown app context to remove the
# current SQLAlchemy session after each requst
@app.teardown_appcontext
def teardown(exception):
    """Remove the current SQLAlchemy session."""
    storage.close()

#Define the route for '/states_list'
@app.route("/states_list", strict_slashes=False)
def states_list():
    """Displays an HTML page with a list of all state objects in DBStorage.

    states are sorted by name.
    """
    # Fetch all state objects from the DBStorage and sort them by name (A->Z)
    state = sorted(storage.all(state).value(), key=lambda s: s.name)

    # Render the template and pass the list of states to the template
    return render_template("7-states_list.html", states=states)

if __name__ == "__main__":
    # Start the Flask development server
    # Listen on all available network interface (0.0.0.0) and port 5000
    app.run(host="0.0.0.0", port=5000)
