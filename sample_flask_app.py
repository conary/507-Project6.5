# Import statements necessary
from flask import Flask, render_template
from flask_script import Manager
import json
import requests
# Set up application
app = Flask(__name__)

manager = Manager(app)

# Routes

@app.route('/')
def hello_world():
    return '<h1>Hello World!</h1>'

@app.route('/user/<yourname>')
def hello_name(yourname):
    return '<h1>Hello {}</h1>'.format(yourname)

@app.route('/showvalues/<name>')
def basic_values_list(name):
    lst = ["hello","goodbye","tomorrow","many","words","jabberwocky"]
    if len(name) > 3:
        longname = name
        shortname = None
    else:
        longname = None
        shortname = name
    return render_template('values.html',word_list=lst,long_name=longname,short_name=shortname)


## PART 1: Add another route /word/<new_word> as the instructions describe.
@app.route('/word/<new_word>')
def nursery_rhymes(new_word):

    baseurl = "https://api.datamuse.com/words"

    final_url = baseurl + '?' + 'rel_rhy=' + new_word
    


    result = json.loads(requests.get(final_url).text)

    final_word = result[0]['word']



    return '<h1>{}</h1>'.format(final_word)

    
## PART 2: Edit the following route so that the photo_tags.html template will render
@app.route('/flickrphotos/<tag>/<num>')
def photo_titles(tag, num):
    FLICKR_KEY = "0efc6276f91dba2f5e77fc74755d38ff" 
    baseurl = 'https://api.flickr.com/services/rest/'
    params = {}
    params['api_key'] = FLICKR_KEY
    params['method'] = 'flickr.photos.search'
    params['format'] = 'json'
    params['tag_mode'] = 'all'
    params['per_page'] = num
    params['tags'] = tag
    response_obj = requests.get(baseurl, params=params)
    trimmed_text = response_obj.text[14:-1]
    flickr_data = json.loads(trimmed_text)
    photos = flickr_data['photos']['photo']
    titles = []
    for photo in photos:
        titles.append(photo['title'])
    return render_template('photo_info.html', photo_titles=titles, num=num)




if __name__ == '__main__':
    manager.run() # Runs the flask server in a special way that makes it nice to debug
