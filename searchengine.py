from app import create_app
from app.models import Artobject
 #from app.models import db_session

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'Artobject': Artobject}  
