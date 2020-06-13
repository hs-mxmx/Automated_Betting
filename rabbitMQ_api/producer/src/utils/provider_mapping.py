from datetime import date
from datetime import datetime

CONTENTYPE = "CONTENTYPE"
CONTENT = "CONTENT"
COUNTRY = "COUNTRY"
DATE = "DATE"
NAME = "NAME"
FILE_EXTENSION = '.json'


contentype_class = ["Application","Audio", "Example", "Image", "Message", "Model", "Multipart", "Text", "Video"]
content_class = ["Show", "Serie", "Anime", "Documental", "Sport", "Announcement"]
country_class = ["Switzerland", "Canada", "Japan", "Germany", "Australia", "UnitedKingdom", "UnitedStates", "Sweden", "Spain"]
name_class = ["Apple", "Samsung", "NASA", "Microsoft", "Dell", "Sony", "IBM", "Netflix", "Telefonica", "Intel", "HP", "Panasonic"]
date_class = str(date.today().strftime("%b-%d-%Y") + str(datetime.now().microsecond))