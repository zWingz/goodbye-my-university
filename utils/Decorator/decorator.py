def post_required(fnc):
    def wraper(request):
        if request.method == "POST":
            return fnc(request)
    return wraper