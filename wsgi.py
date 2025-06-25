from app import create_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.wrappers import Response


app = create_app()
app.config['APPLICATION_ROOT'] = '/masculead/'

application = DispatcherMiddleware(
    Response('Not Found', status=404),
    {'/masculead': app}
)

if __name__ == '__main__':
    #Décommenter pour réinisialiser la base de données aux tableau par défaut
    #initialize_database()
    app.run(host="0.0.0.0", port=5000, debug=True)
