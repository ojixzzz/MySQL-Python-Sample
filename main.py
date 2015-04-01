import falcon
from tes import TesResource

app = falcon.API()
app.add_route('/apis/v1/tes', TesResource())
