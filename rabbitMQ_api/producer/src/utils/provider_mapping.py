from datetime import date
from datetime import datetime
from random import randint

CONTENTYPE = "CONTENTYPE"
CONTENT = "CONTENT"
COUNTRY = "COUNTRY"
DATE = "DATE"
NAME = "NAME"
PRICE = "PRICE"
FILE_EXTENSION = '.json'


contentype_class = ["Application","Audio", "Example", "Image", "Message", "Model", "Multipart", "Text", "Video"]
content_class = ["Show", "Serie", "Anime", "Documental", "Sport", "Announcement"]
country_class = ["Switzerland", "Canada", "Japan", "Germany", "Australia", "UnitedKingdom", "UnitedStates", "Sweden", "Spain"]
name_class = ["Apple", "Samsung", "NASA", "Microsoft", "Dell", "Sony", "IBM", "Netflix", "Telefonica", "Intel", "HP", "Panasonic"]
date_class = str(date.today().strftime('%Y-%m-%d') + '_' + str(datetime.now().microsecond))
price_class_min = 10000
price_class_max = 1000000