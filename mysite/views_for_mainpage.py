from django.shortcuts import redirect
def index():
    return redirect("polls:index")
