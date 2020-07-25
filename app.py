from wsgiref.simple_server import make_server
import tg
from tg import MinimalApplicationConfigurator
from tg import expose, TGController
import pandas as pd
import database
import pickle


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

    @expose(content_type="text/plain")
    def page(self):
        return 'page'

    @expose()
    def heart(self):
        accept_types = [i for i in tg.request.accept]
        tg.response.content_type, content = resolve_requested_format(database.querier.heart_data(), accept_types)
        return content

    @expose(content_type="text/plain")
    def refresh(self):
        database.update_all()

# Configure a new minimal application with our root controller.
config = MinimalApplicationConfigurator()
config.update_blueprint({
    'root_controller': RootController()
})

# config.register(SQLAlchemyConfigurationComponent)
# config.update_blueprint({
#     'use_sqlalchemy': True,
#     'sqlalchemy.url': 'sqlite:///devdata.db'
# })


# config.update_blueprint({'model': Bunch(
#     DBSession=DBSession,
#     init_model=init_model
# )})

# Serve the newly configured web application.
print("Health hub serving on port 8080...")
httpd = make_server('', 5000, config.make_wsgi_app())
httpd.serve_forever()