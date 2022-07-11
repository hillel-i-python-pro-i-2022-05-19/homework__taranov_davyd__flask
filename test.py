import csv
import io
from app import CHARACTERISTICS_URL
import urllib.request

def characteristics():
    height_list = []
    weight_list = []
    response = urllib.request.urlopen("https://drive.google.com/uc?export=download&id=1yM0a4CSf0iuAGOGEljdb7qcWyz82RBxl")
    # response = urllib.request.urlopen(CHARACTERISTICS_URL)
    with io.TextIOWrapper(response, encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)
#             height_list.append(float(row[' "Height(Inches)"']))
#             weight_list.append(float(row[' "Weight(Pounds)"']))
#         average_height = round(((max(height_list) + min(height_list)) / 2) * 2.54, 2)
#         average_weight = round(((max(weight_list) + min(weight_list)) / 2) / 2.2046, 2)
#         return f"""<p>Средний вес: {average_weight} кг</p>
#         <p>Средний рост: {average_height} см</p>
# """
