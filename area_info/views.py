import os
import redis
import requests
from flask import request, render_template, send_from_directory
from flask.ext.thumbnails import Thumbnail
from werkzeug.routing import BaseConverter
from area_info import app
from area_info.search_client import wikipedia_geo_search, nrk_search, wikipedia_id_lookup


app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
rc = redis.StrictRedis()
Thumb = Thumbnail(app)


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app.url_map.converters['regex'] = RegexConverter


def normalize_images(nrk_content_list):
    for entry in nrk_content_list:
        cid = entry['id']
        thumbnail_url = rc.get(cid)
        if thumbnail_url is None or not \
            os.path.exists(os.path.join(app.config['MEDIA_FOLDER'], thumbnail_url.split('/')[-1])):
            image_url = entry['image']
            r = requests.get(image_url, stream=True)
            filename = '{}{}{}.png'.format(app.config['MEDIA_FOLDER'], os.path.sep, image_url.split('/')[-1])
            with open(filename, 'w') as outim:
                for line in r.iter_content():
                    outim.write(line)
            thumbnail_url = Thumb.thumbnail(filename.split('/')[-1],
                                            app.config['THUMBNAIL_SIZEs'], 'fit')
            rc.set(cid, thumbnail_url)
        entry['image'] = thumbnail_url
        yield entry


@app.route('/media/<regex("([\w\d_/-]+)?.(?:jpe?g|gif|png)"):filename>')
def media_file(filename):
    return send_from_directory(app.config['MEDIA_THUMBNAIL_FOLDER'], filename)


@app.route('/nearby/', methods=['POST'])
def nearby_list():
    latitude = float(request.form['latitude'])
    longitude = float(request.form['longitude'])
    nearby_locations = wikipedia_geo_search(latitude, longitude)
    return render_template('nearby_list.jade', **nearby_locations)


@app.route('/location/')
def location_detail():
    title = request.args.get('title')
    wikipeda_id = request.args.get('wid')
    wikipedia_content = wikipedia_id_lookup(wikipeda_id)

    nrk_content = nrk_search(title)
    nrk_content = list(normalize_images(nrk_content))
    return render_template('location_detail.jade', wikipedia_content=wikipedia_content, nrk_content=nrk_content)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.jade')
