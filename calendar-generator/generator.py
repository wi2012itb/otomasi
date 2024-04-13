'''
cal-ics2md
Markdown Calendar Generator

@ cc-christopher: https://github.com/cc-christopher
GPL-3.0 License

This script is used to generate a Markdown file with monthly view calendar from an .ics file.
Events are listed in collapsible format for each day.

Please refer to the README.md for information on usage.
'''

print('cal-ics2md - Markdown Calendar Generator\n\nby cc-christopher: https://github.com/cc-christopher\nGPL-3.0 License\n')
print('---------------------------------------------')
print('Loading...')

import requests
import yaml
from icalendar import Calendar
import pandas as pd
import calendar

def read_ics(file):
    """
    Read the downloaded .ics file and return the calendar object.

    Args:
        file (str): path to the .ics file.

    Returns:
        Calendar: The calendar object parsed from the .ics file.
    """
    with open(file, 'rb') as f:
        cal = Calendar.from_ical(f.read())
    return cal

def weekheader():
    """
    Generate the month table header.

    Returns:
        str: month table header
    """
    # Bahasa Indonesia days of the week
    md = "| Senin | Selasa | Rabu | Kamis | Jumat | Sabtu | Minggu |\n| --- | --- | --- | --- | --- | --- | --- |\n"
    return md

def generate_event(event):
    """
    Generate each event in collapsible format.

    Args:
        event (dict): event details from DataFrame

    Returns:
        str: markdown format of the event in collapsible format
    """
    summary = event['summary']
    start_time = event['dtstart'].strftime('%I:%M %p') 
    end_time = event['dtend'].strftime('%I:%M %p')
    location = event['location']
    # description = event['description'] # add description on collapsible
    return f'<details><summary>{summary}</summary>Waktu: {start_time} - {end_time} <br>Lokasi: {location}</details>'

def listdayofweek(month, year, df):
    """
    Generate the respective dates and events for each day in the month table

    Args:
        month (int)
        year (int)
        df (DataFrame): DataFrame containing the .ics file data

    Returns:
        str: Markdown table representation of the month, with dates and events
    """
    md = ''
    cal = calendar.monthcalendar(year, month)
    for week in cal:
        md += '| '
        for day in week:
            if day != 0:
                date = pd.Timestamp(year, month, day)
                events = df[df['dtstart'].dt.date == date.date()]
                event_count = len(events)
                md += f'{day} <br>&#10240; '
                for _, event in events.iterrows():
                    md += generate_event(event)
                for _ in range(4 - event_count):
                    md += '<br>&#10240;'
                if event_count > 0:
                    md = md[:-len('<br>&#10240;')]
                md += ' | '
            else:
                md += ' <br>&#10240;<br>&#10240;<br>&#10240;<br>&#10240;<br>&#10240; | '
        md += '\n'
    return md

def generate_calendar(start_month, start_year, end_month, end_year, df):
    """
    Generate iteratively the monthly view of the calendar for the specified period.

    Args:
        start_month (int)
        start_year (int)
        end_month (int)
        end_year (int)
        df (DataFrame): DataFrame containing the .ics file data

    Returns:
        str: Markdown representation of the calendar in monthly view
    """
    md = ''
    for year in range(start_year, end_year+1):
        for month in range(start_month if year == start_year else 1, end_month+1 if year == end_year else 13):
            md += f'### {bulan[month]} {year}\n\n'
            md += weekheader()
            md += listdayofweek(month, year, df)
            md += '\n'
    return md

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

# Bahasa Indonesia months
bulan = ['', 'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']

print('Configuring...')

# modify config.yml for the output
loc = config['CALENDAR_URL']
start_m = int(config['START_MONTH'])
start_y = int(config['START_YEAR'])
end_m = int(config['END_MONTH'])
end_y = int(config['END_YEAR'])
output = config['OUTPUT_FILE']

print('Running...')
print('---------------------------------------------')

r = requests.get(loc)
with open('calendar.ics', 'wb') as f:
    f.write(r.content)
print('.ics file saved as calendar.ics on the current directory')

cal = read_ics('calendar.ics')

print('Generating markdown file...')
data = []
for event in cal.walk('vevent'):
    data.append([event['summary'], event['dtstart'].dt, event['dtend'].dt, event['location'], event['description']])

df = pd.DataFrame(data, columns=['summary', 'dtstart', 'dtend', 'location', 'description'])

with open(output, 'w') as f:
    f.write('# Generated Calendar\n\n')
    f.write(generate_calendar(start_m, start_y, end_m, end_y, df))

print(f'Markdown file saved as {output} on the current directory')