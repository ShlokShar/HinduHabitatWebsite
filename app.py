from backend.api import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///website_variables.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
load_dotenv()
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")


class WebsiteVariables(db.Model):
    id = db.Column(db.String, primary_key=True)
    download_count = db.Column(db.String, nullable=False)
    review = db.Column(db.String, nullable=False)


def get_variables():
    record = WebsiteVariables.query.filter_by(id="unique_id").first()
    if record:
        return record.download_count, record.review
    return None, None


with app.app_context():
    db.create_all()  # Creates the table if it doesn't exist

# Cache settings for articles
cache_data = None
cache_time = 0
CACHE_DURATION = 3600

# Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'hinduhabitatapp@gmail.com'
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = 'hinduhabitatapp@gmail.com'
app.config['TESTING'] = False
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

mail = Mail(app)


@app.route('/')
def home():
    download_count, reviews = get_variables()
    return render_template("home.html", download_count=download_count, reviews=reviews)


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html")


@app.route("/features")
def features():
    return render_template("features.html")


@app.route("/donate")
def donate():
    return render_template('donate.html')


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("fullname")
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


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if "logged_in" not in flask.session:
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")

            if username == "admin" and password == ADMIN_PASSWORD:
                flask.session["logged_in"] = True
                return flask.redirect("/admin")
        return render_template("login.html")

    form = VariableForm()
    record = WebsiteVariables.query.filter_by(id="unique_id").first()

    if form.validate_on_submit():
        flask.flash("Form Submitted", "success")
        if record:
            record.download_count = form.var1.data
            record.review = form.var2.data
        else:
            flask.flash("record not found", "success")
            new_record = WebsiteVariables(id="unique_id", download_count=form.var1.data, review=form.var2.data)
            db.session.add(new_record)
        db.session.commit()
        flask.flash('Variables updated successfully', 'success')
        return flask.redirect("/admin")
    if record:
        form.var1.data = record.download_count
        form.var2.data = record.review

    return render_template('admin.html', form=form)


if __name__ == '__main__':
    app.run()
