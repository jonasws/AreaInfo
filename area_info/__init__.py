from flask import Flask


app = Flask(__name__)
app.config.from_object('area_info.default_settings')
app.config.from_envvar('AREA_INFO_SETTINGS', silent=True)


if not app.debug:
    import logging
    file_handler = logging.FileHandler('/srv/www/AreaInfo/flask.log', encoding='utf-8')
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)


import area_info.views
