PATH = r'C:\Users\leohr\Documents\Projetos\florense\florense\order_files'


def handle_uploaded_file(f, order, room, product):
    with open('{}\{}\{}\{}'.format(PATH), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
