def handle_upload_file(f):
    with open('static/upload/'+f.name,'wb+')as destination:
        for c in f.chunks():
            destination.write(c)