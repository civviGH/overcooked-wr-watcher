from slugify import slugify
import csv

class Entry:

    def __init__(self, csv_row):
        self.game = csv_row[0]
        self.dlc = csv_row[1]
        self.level = csv_row[2]
        self.player_count = csv_row[3]
        self.place = csv_row[4]
        self.player = csv_row[5] # this is also the team name if player_count > 0
        self.score = csv_row[6]
        self.url = csv_row[7]

    def has_team_entry(self, team_name):
        if self.player_count == 1:
            return False
        return self.player.casefold() == team_name.casefold()

class Level:

    def __init__(self, entry):
        self.game = entry.game
        self.dlc = entry.dlc
        self.level = entry.level
        self._entries = [entry]

    def add(self, entry):
        self._entries.append(entry)

    def has_team_entry(self, team_name):
        for e in self._entries:
            if e.has_team_entry(team_name):
                return True
        return False

    def get_team_placement(self, team_name):
        if not self.has_team_entry(team_name):
            return -1
        for e in self._entries:
            if e.has_team_entry(team_name):
                return e.place

    def __eq__(self, other):
        if not isinstance(other, (Level,Entry)):
            return NotImplemented
        return self.game == other.game and self.dlc == other.dlc and self.level == other.level

    def __str__(self):
        return f"{self.game} - {self.dlc} - {self.level}"

    def slug(self):
        return slugify(f"{self.game} {self.dlc} {self.level}")

class DataPoint:

    def __init__(self, csv_filename, team_name):

        self._entries = []
        self._levels = []
        self._team_name = team_name
        
        with open (csv_filename, "r") as csv_data:
            csv_reader = csv.reader(csv_data, delimiter=",")
            next(csv_reader) # skip first line with column names
            for row in csv_reader:
                self._entries.append(Entry(row))

        # sort the entries into levels for easy queries       
        level = Level(self._entries[0])
        for entry in self._entries:
            if entry == level:
                level.add(entry)
            else:
                self._levels.append(level)
                level = Level(entry)

        # calculate a list of all levels the team is on, and its placement
        placed_levels = [l for l in self._levels if l.has_team_entry(self._team_name)]
        self._levels_with_placements = {}
        for pl in placed_levels:
            self._levels_with_placements[pl.slug()] = {
                'placement' : pl.get_team_placement(self._team_name),
                'level' : pl
            }

    def get_placement_dict(self):
        return self._levels_with_placements

    def diff(self, other_dp):
        out_msg = []
        # possible cases:
        # 1 complete new level not in list
        # 2 placement within a level changed
        for level_slug, info in other_dp.get_placement_dict().items():
            if level_slug not in self._levels_with_placements:
                out_msg.append(self.create_new_record_message(info))
                continue
            placement = info['placement']
            old_placement = self._levels_with_placements[level_slug]['placement']
            if old_placement != placement:
                out_msg.append(self.create_placement_change_message(info, old_placement))
        if len(out_msg) == 0:
            return None
        return out_msg

    def get_report(self):
        out_msg = []
        for _, info in self._levels_with_placements.items():
            out_msg.append(self.create_new_record_message(info))
        return out_msg

    def create_new_record_message(self, info):
        # boilerplate for URL
        game_slug = slugify(info['level'].game)
        if game_slug == "all-you-can-eat":
            game = "ayce"
        else:
            game = game_slug
        dlc = slugify(info['level'].dlc)
        stage = slugify(info['level'].level)
        url = f"https://overcooked.greeny.dev/{game}/{dlc}/{stage}"

        placement = info['placement']
        msg = f"New record for Team {self._team_name} on {info['level']}, placing {placement} \n{url}"

        return msg

    # this seems quite redundant with ^ 
    def create_placement_change_message(self, info, old_placement):
        # boilerplate for URL
        game_slug = slugify(info['level'].game)
        if game_slug == "all-you-can-eat":
            game = "ayce"
        else:
            game = game_slug
        dlc = slugify(info['level'].dlc)
        stage = slugify(info['level'].level)
        url = f"https://overcooked.greeny.dev/{game}/{dlc}/{stage}"

        placement = info['placement']
        msg = f"Placement changed for Team {self._team_name} on {info['level']} from {old_placement} to {placement} \n{url}"

        return msg