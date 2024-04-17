import logging
from dataset.data_cleaner import DataCleaner
from dataset.data_exporter import DataExporter
from dataset.main import DataFramework

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',filename="logs/data.log")

dataset_path = './data/HKS2023.csv' 
framework = DataFramework(dataset_path)
datacleaner = DataCleaner()
dataExporter = DataExporter()

framework.df = datacleaner.clean_data(framework.df)
framework.df = framework.filter_data("NetTime", lambda x: x != 0)
orginal_data = framework.df.copy()

# Oppgave a
framework.df = orginal_data
framework.df = framework.sort_column_numeric("NetTime", True)
framework.df = framework.df.head(13)
dataExporter.export_data(framework.df, "./data/topp13.xlsx", "excel")
print(framework.df)

# Oppgave b
for klasse in ['Pulje F1', 'Pulje B1', 'Pulje B4', 'Pulje F6']:
    print(f"Topp 10 i {klasse}")
    framework.df = orginal_data

    framework.df = framework.filter_data("GroupdName", lambda x: x == klasse)
    framework.df = framework.sort_column_numeric("NetTime", True)
    dataExporter.export_data(framework, f"./data/topp10/{klasse}.xlsx", "excel")
    print(framework.df.get(["Firstname", "Surname", "NameFormatted", "NetTime", "GroupdName"]).head(10))

# Oppgave c
m = 10
def find_top_for_name_range(func, lagreSom):
    framework.df = orginal_data

    framework.df = framework.filter_data("NameFormatted", func )
    framework.df = framework.sort_column_numeric("NetTime", True)
    dataExporter.export_data(framework, f"./data/topp10/{lagreSom}.xlsx", "excel")
    return framework.df.copy()

print(f"Topp {m} lag for opp til 6 tegn:")
print(find_top_for_name_range(lambda x:  len(x) <= 6, "oppTil6").get(["NameFormatted", "NetTime"]).head(m))

print(f"Topp {m} lag mellom 7 og 10 tegn:")
print(find_top_for_name_range(lambda x: 7 <= len(x) <= 10, "syvTil10").get(["NameFormatted", "NetTime"]).head(m))

print(f"Topp {m} lag med mer enn 10 tegn:")
print(find_top_for_name_range(lambda x:  len(x) > 10, "merEnn10").get(["NameFormatted", "NetTime"]).head(m))

# Oppgave d
framework.df = orginal_data.copy()

oppTil60 = len(framework.filter_data("NetTime", lambda x: x/60000 < 60))
framework.df = orginal_data.copy()

fra60Til90 = len(framework.filter_data("NetTime", lambda x: 90 > x/60000 >= 60))

framework.df = orginal_data.copy() 
merEnn90 = len(framework.filter_data("NetTime", lambda x: x/60000 > 90))

import seaborn as sns
import matplotlib.pyplot as plt

sns.barplot(x=["Under 60 min", "60-90 min", "Over 90 min"], y=[oppTil60, fra60Til90, merEnn90])
plt.title("Antall deltakere i ulike tidsintervaller")
plt.show()
print(oppTil60, fra60Til90, merEnn90)

# oppgave e
framework.df = orginal_data.copy()
framework.df = framework.filter_data("ClubTeamFormatted", lambda x: x=="#Undervisning")
utdanning = framework.sort_column_numeric("NetTime", True)

print(f'Vinner i #utdanning: {utdanning.get(["Firstname", "Surname", "NameFormatted", "NetTime", "ClubTeamFormatted"]).head(1)}')

elvebakken = framework.filter_data("NameFormatted", lambda x: x=="Elvebakken Vgs 1")
elvebakkenTid = elvebakken.get("NetTime").values[0]
antallOver = len(framework.filter_data("NetTime", lambda x: x < elvebakkenTid))
print(f'Elvebakken VGS 1 sin plassering: {antallOver+1}')


