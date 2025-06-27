from backend.imports import *

with open("data.json") as file:
    data = json.load(file)


def convert_to_timezone(date_str, timezone):
    # Convert a date string to the specified timezone.
    la_tz = pytz.timezone('America/Los_Angeles')
    user_tz = pytz.timezone(timezone)
    date_obj = datetime.strptime(date_str, '%B %d %Y')
    la_time = la_tz.localize(date_obj)
    user_time = la_time.astimezone(user_tz)
    return user_time.strftime('%B %d %Y')


def adjust_festival_dates(festivals, timezone):
    # Adjust festival dates to the user's timezone.
    for festival in festivals:
        festival['festivalDate'] = convert_to_timezone(festival['festivalDate'], timezone)
    return festivals


def get_upcoming_event(user_timezone, event_type="festivals"):
    # Get the next upcoming event of a specified type.
    timezone = pytz.timezone(user_timezone)
    current_date = datetime.now(timezone)
    upcoming = []

    for event in data.get(event_type, []):
        event_date = timezone.localize(datetime.strptime(event["festivalDate"], "%B %d %Y"))
        if event_date > current_date:
            upcoming.append({
                "festivalName": event["festivalName"],
                "festivalDate": event_date
            })

    upcoming.sort(key=lambda x: x['festivalDate'])
    if upcoming:
        next_event = upcoming[0]
        return {
            "festivalName": next_event["festivalName"],
            "festivalDate": next_event["festivalDate"].strftime("%B %d, %Y")
        }
    return None


def fetch_articles():
    # Fetch the latest articles from the specified website.
    url = "https://www.hinduamerican.org/press-statements"
    image_url_pattern = r'background-image:url\((.*?)\);'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    articles = soup.find_all(class_="nectar-post-grid-item")
    article_data = []

    for article in articles[:3]:
        id = uuid.uuid4()
        image_container = article.find(class_="nectar-post-grid-item-bg")
        image_url = re.search(image_url_pattern, str(image_container)).group(1)
        title = article.find("a", class_=None).text.strip()
        link = article.find("a").get("href")
        date = article.find(class_="meta-date").text.strip()

        article_data.append({
            "id": id,
            "title": title,
            "date": date,
            "link": link,
            "image_url": image_url
        })

    return article_data
