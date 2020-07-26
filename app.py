from wsgiref.simple_server import make_server
from tg import MinimalApplicationConfigurator, expose, TGController, response, request
import pandas as pd
import database
import pickle

from function_registrar import selectable

HOST = "localhost"
PORT = 5000

available_formats = {
    'json': 'application/json',
    'csv': 'text/csv',
    'html': 'text/html',
    'pickled pandas dataframe': 'application/octet-stream'
}


def resolve_requested_format(df: pd.DataFrame, accept_types):
    if 'application/json' in accept_types:
        return 'application/json', df.to_json()
    elif 'text/csv' in accept_types or 'application/csv' in accept_types:
        return 'text/csv', df.to_csv()
    elif 'text/html' in accept_types:
        return 'text/html', df.to_html()
    elif 'application/octet-stream' in accept_types:
        return 'application/octet-stream', pickle.dumps(df)
    else:
        return df.to_json()


class RootController(TGController):
    @expose(content_type="text/plain")
    def index(self):
        return 'data'

    @selectable("Fetch all from heart table")
    @expose()
    def heart(self):
        accept_types = [i for i in request.accept]
        response.content_type, content = resolve_requested_format(database.querier.heart_data(), accept_types)
        return content

    @selectable("Fetch all from activity summaries table")
    @expose()
    def activity_summaries(self):
        accept_types = [i for i in request.accept]
        response.content_type, content = resolve_requested_format(database.querier.activity_summaries(), accept_types)
        return content

    @selectable("Fetch all from swimming table")
    @expose()
    def swimming(self):
        accept_types = [i for i in request.accept]
        response.content_type, content = resolve_requested_format(database.querier.swimming(), accept_types)
        return content

    @selectable("Fetch all from calorie table")
    @expose()
    def calories(self):
        accept_types = [i for i in request.accept]
        response.content_type, content = resolve_requested_format(database.querier.calories(), accept_types)
        return content

    @selectable("Fetch all from swimming laps table")
    @expose()
    def swimming_laps(self):
        accept_types = [i for i in request.accept]
        response.content_type, content = resolve_requested_format(database.querier.swimming_laps(), accept_types)
        return content

    @selectable("Fetch all from swimming strokes table")
    @expose()
    def swimming_strokes(self):
        accept_types = [i for i in request.accept]
        response.content_type, content = resolve_requested_format(database.querier.swimming_strokes(), accept_types)
        return content

    @selectable("Fetch all environmental audio exposure table")
    @expose()
    def env_audio_exposure(self):
        accept_types = [i for i in request.accept]
        response.content_type, content = resolve_requested_format(database.querier.env_audio_exposure(), accept_types)
        return content

    @selectable("Fetch all from phones audio exposure table")
    @expose()
    def phones_audio_exposure(self):
        accept_types = [i for i in request.accept]
        response.content_type, content = resolve_requested_format(database.querier.phones_audio_exposure(),
                                                                  accept_types)
        return content

    @expose("json", content_type="application/json")
    def refresh(self):
        return database.update_all()

    @expose("json", content_type="application/json")
    def endpoints(self):
        result = dict()
        for endpoint_name in selectable.all:
            endpoint_details = selectable.all[endpoint_name]
            result[endpoint_name] = {
                'name': endpoint_name,
                'endpoint': "{}:{}/{}".format(HOST, str(PORT), endpoint_name),
                'description': endpoint_details['description']
            }
        return result

    @expose("json", content_type="application/json")
    def formats(self):
        return available_formats


# Configure a new minimal application with our root controller.
config = MinimalApplicationConfigurator()
config.update_blueprint({
    'root_controller': RootController()
})

# Serve the newly configured web application.
print("Health hub serving on port {}...".format(str(PORT)))
httpd = make_server('', PORT, config.make_wsgi_app())
httpd.serve_forever()
