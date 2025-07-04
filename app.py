from backend.api import *

app = Flask(__name__)

# Cache settings for articles
cache_data = None
cache_time = 0
CACHE_DURATION = 3600

# Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = os.getenv("MAIL_PORT")
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_USERNAME")
app.config['TESTING'] = False
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

mail = Mail(app)


# MAIN ROUTES
@app.route('/')
def home():
    return render_template("home.html")


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message_content = f"From email: {email}\n\nMessage:\n{request.form.get('message')}"
        msg = Message(
            subject=f"Hindu Habitat Message from {name}",
            recipients=["hinduhabitatapp@gmail.com"],
            body=message_content
        )
        mail.send(msg)
        return flask.redirect("/")
    return render_template('contact.html')


@app.route("/privacy")
def privacy_policy():
    return render_template("privacy.html")


# API
@app.route("/fetch_festivals/")
def fetch_festivals():
    user_timezone = request.args.get("timezone").replace("2%", "/")
    festivals = adjust_festival_dates(data['festivals'], user_timezone)
    return jsonify({"festivals": festivals})


@app.route("/fetch_fasting/")
def fetch_fasting():
    user_timezone = request.args.get("timezone").replace("2%", "/")
    fasting = adjust_festival_dates(data['fasting'], user_timezone)
    return jsonify({"fasting": fasting})


@app.route("/get_upcoming_festival/")
def get_upcoming_festival():
    user_timezone = request.args.get("timezone").replace("2%", "/")
    next_festival = get_upcoming_event(user_timezone, "festivals")
    return jsonify(next_festival)


@app.route("/get_upcoming_fast/")
def get_upcoming_fast():
    user_timezone = request.args.get("timezone").replace("2%", "/")
    next_fast = get_upcoming_event(user_timezone, "fasting")
    return jsonify(next_fast)


@app.route('/articles', methods=['GET'])
def get_articles():
    global cache_data, cache_time

    current_time = time.time()
    if cache_data is None or current_time - cache_time > CACHE_DURATION:
        cache_data = fetch_articles()
        cache_time = current_time
    return jsonify(cache_data)


@app.route("/app-ads.txt")
def app_ads():
    return send_from_directory('static', 'app-ads.txt', mimetype='text/plain')


if __name__ == '__main__':
    app.run()
