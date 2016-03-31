from django.shortcuts import redirect
def post_required(fnc):
    def wraper(request):
        if request.method == "POST":
            return fnc(request)
    return wraper


def admin_required(fnc):
    def wraper(request):
        if request.user.is_superuser:
            return fnc(request)
        else:
            return redirect("/")
    return wraper