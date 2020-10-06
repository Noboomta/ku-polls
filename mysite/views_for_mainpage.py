"""simple view of index for redirect to index."""
from django.shortcuts import redirect
def index():
    """Redirect to index page."""
    return redirect("polls:index")
