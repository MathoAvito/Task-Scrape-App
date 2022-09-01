from flask import Blueprint

views = Blueprint('views', __name__)


@views.route('/')  # homepage
def home():
    return "<h1>Test</h1>"
