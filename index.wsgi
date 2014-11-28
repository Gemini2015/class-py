import sae
from Classmates import wsgi

application = sae.create_wsgi_app(wsgi.application)