from flask_frozen import Freezer
from AgileX import init_app
import os

app = init_app()

freezer = Freezer(app)

def absoluteFilePaths():
    directory ="AgileX/build/"
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            yield "/"+(os.path.join(dirpath, f))[13:]

@freezer.register_generator
def product_url_generator():
    # URLs as strings
    yield '/dashapp/'
    yield '/doc/'

@freezer.register_generator
def product_url_generator2():
    items = list(absoluteFilePaths())
    i=0
    while i < len(items):
        items[i] = items[i].replace("\\","/")
        if '.git' in items[i] or 'index' in items[i]:
            items.remove(items[i])
        else:
            i+=1
    # print(items)
    return items

@freezer.register_generator
def product_url_generator3():
    # URLs as strings
    yield '/dashapp/../'
    yield '/dashapp/_dash-component-suites/'



if __name__ == '__main__':
    freezer.run(debug=True)
    # freezer.freeze()