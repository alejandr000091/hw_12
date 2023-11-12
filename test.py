import re
from datetime import datetime

data = "Contact name: Bill, birthday: 1990-12-26"

if "ggggg" in data:
    print(data)

data_string = """
Contact name: my1, phones: 0934283855; 0934283855
Contact name: Bill, birthday: 1990-12-26
Contact name: John, birthday: 1995-12-29
Contact name: Tilda, birthday: 2000-12-30
Contact name: Marry, birthday: 2000-1-1
Contact name: Denis, birthday: 2005-1-2
Contact name: Alex, birthday: 1990-1-3
Contact name: JanKoum, birthday: 1976-1-1
"""


# pattern = re.compile(r'Contact name: (?P<name>.*?), (?:phones: (?P<phones>.*?); )?(?:birthday: (?P<birthday>.*?))?$')
# matches = pattern.finditer(data_string)

# result = []

# for match in matches:
#     info_dict = match.groupdict()
#     if "birthday" in info_dict:
#         info_dict["birthday"] = datetime.strptime(info_dict["birthday"], "%Y-%m-%d").date()
#     result.append(info_dict)

# print(result)