from twitterbot import app, db
from twitterbot import schedules
from flask_alembic import Alembic

if __name__ == '__main__':
    # db.create_all()  # only required once on initial set up
    schedules.scheduler.start()
    # alembic = Alembic()
    # alembic.init_app(app)
    # alembic.revision('added tweet and transaction db models')
    # alembic.upgrade()
    app.run(debug=False)
