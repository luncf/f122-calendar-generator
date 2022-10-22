import argparse
from collections import namedtuple
from enum import Enum
import json
import random
import os

class SeasonLength(Enum):
    Short = 10
    Medium = 16
    Full = 22

    def __str__(self):
        return '{} [{}]'.format(self.name, self.value)

    def __repr__(self):
        return str(self)

    @staticmethod
    def from_string(i):
        try:
            return SeasonLength[i.title()]
        except KeyError:
            raise ValueError()

SeasonSettings = namedtuple("SeasonSettings", "calendar_length season_number")

def parse_input():
    parser = argparse.ArgumentParser(description='Generate your F122 Season Calendar')
    parser.add_argument('--calendar_length', nargs='?', type=SeasonLength.from_string, choices=list(SeasonLength), default=SeasonLength.Full, help='Number of races in the season.')
    parser.add_argument('--season_number', nargs='?', type=int, choices=range(1, 11), default=1, help='Season number. This will change the Grand Prix races available.')
    args = parser.parse_args()

    return SeasonSettings(args.calendar_length.value, args.season_number)

def load_grand_prix_races(season_number):
    grand_prix_races = []

    with open('grand_prix_races.json') as f:
        data = json.load(f)
        grand_prix_races = data['default_gps']

        if season_number > 1:
            grand_prix_races.extend(data['extra_gps'])

    return grand_prix_races

def generate_calendar(num_grand_prix_races, calendar_length):
    calendar = list(range(0, num_grand_prix_races))

    while (calendar_length != len(calendar)):
        next_gp_to_remove = random.randint(0, len(calendar) - 1)
        del calendar[next_gp_to_remove]

    return calendar

def print_calendar(grand_prix_races, calendar):
    ANSI_END = '\33[0m'
    ANSI_BOLD = '\33[1m'
    ANSI_RED_BG = '\33[101m'
    ANSI_GREEN_BG = '\33[102m'

    INVSIBLE_CHAR = chr(24)

    os.system("") # Required for Windows to render text colour correctly

    longest_gp_name = len(max(grand_prix_races, key=len))

    for i, grand_prix in enumerate(grand_prix_races):
        try:
            race_number = calendar.index(i)
            print(ANSI_BOLD + ANSI_GREEN_BG + '{:02d}. {:{width}}'.format(race_number + 1, grand_prix, width=longest_gp_name) + INVSIBLE_CHAR + ANSI_END)
        except ValueError:
            print(ANSI_RED_BG + '    {:{width}}'.format(grand_prix, width=longest_gp_name) + INVSIBLE_CHAR + ANSI_END)

def main():
    season_settings = parse_input()

    grand_prix_races = load_grand_prix_races(season_settings.season_number)
    calendar = generate_calendar(len(grand_prix_races), season_settings.calendar_length)

    print_calendar(grand_prix_races, calendar)

if __name__ == "__main__":
    main()