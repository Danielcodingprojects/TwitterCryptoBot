from twitterbot import app, db
from twitterbot import schedules

if __name__ == '__main__':
    # db.create_all() only required once on initial set up
    schedules.scheduler.start()
    app.run(debug=False)
