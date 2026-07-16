#transforming the duration of the video drom ISO format to useable format.

from datetime import timedelta

def parse_duration(duration_str):

    duration_str = duration_str.replace("p","").replace("T","")

    components = ['D','H','M','S']
    values = {'D':0,'H':0,'M':0,'S':0}

    for component in components:
        value, duration_str = duration_str.split(component)
        values[component] = int(value)

    
    total_duration = timedelta(
        days=values["D"], hours = values["H"], minutes= values["M"], seconds=values["S"]

    )
    return total_duration

def transform_data(row):

    duration_td = parse_duration(row["Duration"])

    row["Duration"] = (datetime.min + duration_td).time()

    row["Video_Type"] = "Shorts" if duration_td.total_seconds() <= 60 else "Normal"

    return row

