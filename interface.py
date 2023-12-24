from PyInquirer import prompt
import search
import json
import os

class Interface:
    def __init__(self) -> None:
        self.format_choice = {
            'type' : 'list',
            'name': 'user_option',
            'message': 'What entry do you want?',
            'choices': ['Anime', 'Manga', 'Movie', 'Cancel']
        }
        self.entry_choice = {
            'type' : 'list',
            'name': 'user_option',
            'message': 'What entry do you want?',
            'choices': []
        }
        self.anime_status =  {
            'type' : 'list',
            'name': 'user_option',
            'message': 'What is the status?',
            'choices': ['Plan to watch', 'Watching', 'Finished', 'Dropped']           
        }
        self.manga_status =  {
            'type' : 'list',
            'name': 'user_option',
            'message': 'What is the status?',
            'choices': ['Reading', 'Finished', 'Dropped', 'Plan to read']           
        }
        self.movie_status =  {
            'type' : 'list',
            'name': 'user_option',
            'message': 'What is the status?',
            'choices': ['Plan to watch', 'Watched']           
        }
        self.score =  {
            'type' : 'list',
            'name': 'user_option',
            'message': 'What is the status?',
            'choices': ['Favorite', 'Very Good', 'Nice', 'Meh', 'Bad', 'Very Bad']           
        }
        self.anime_preset = [
            {'Reading': []},
            {'Finished': []},
            {'Dropped': []},
            {'Plan to read': []}
        ]
        self.manga_preset = [
            {'Watching': []},
            {'Finished': []},
            {'Dropped': []},
            {'Plan to watch': []}
        ]
        self.movie_preset = [
            {'Plan to watch': []},
            {'Watched': []}
        ]

        self.path = r'./Databases' #Path to Databases directory (make sure it exists)        
        self.status = False
        self.format = False
    
    def AddEntry(self) -> None:
        media_data = self.FormatChoice() #chooses the format
        
        # Check for errors in request
        if isinstance(media_data, str):
            print(media_data)
            return False

        desired_entry = self.EntryChoice(media_data)
        
        # Check if user opted for 'None'
        if desired_entry == None:
            return False

        filtered_data = self.FilterData(media_data, desired_entry)
        
        if self.format == "ANIME": 
            self.DbWrite(filtered_data, self.path + r'/anime_db.json', self.anime_preset)

        elif self.format == "MANGA": 
            self.DbWrite(filtered_data, self.path + r'/manga_db.json', self.manga_preset)

        elif self.format == "MOVIE": 
            self.DbWrite(filtered_data, self.path + r'/movie_db.json', self.movie_preset)

    def FormatChoice(self) -> list:
        format = prompt(self.format_choice)

        if format.get("user_option") == "Anime":
            self.format = "ANIME"

            anime_name = input('Please input the name of the desired anime: ').strip()
            return search.AnilistData(anime_name, self.format)["data"]["Page"]["media"] #removes  junk

        elif format.get("user_option") == "Manga":
            self.format = "MANGA"

            manga_name = input('Please input the name of the desired anime: ').strip()
            return search.AnilistData(manga_name, self.format)["data"]["Page"]["media"] #removes  junk

        elif format.get("user_option") == "Movie": 
            self.format = "MOVIE"

            movie_name = input('Please input the name of the desired movie: ').strip()
            return search.MovieSearch(movie_name)['results']

        elif format.get("user_option") == "Cancel":
            return 'Operation cancelled'

    def EntryChoice(self, entries:list) -> int: 
        # Texts for each type of midia
        if self.format == 'ANIME' or self.format == 'MANGA':
            for entry in entries:
                entry_text = '{} ({}) -- {}\n'.format(
                    entry['title']['english'], entry['title']['romaji'],
                    entry['startDate']['year'])
                self.entry_choice['choices'].append(entry_text)            
        
        elif self.format == 'MOVIE':
            for entry in entries:
                entry_text = '{} -- {}\n'.format(entry['original_title'], entry['release_date'])
                self.entry_choice['choices'].append(entry_text)
        
        self.entry_choice['choices'].append('None')
        
        #Visual stuff
        desired_entry = prompt(self.entry_choice)
        
        if desired_entry['user_option'] == 'None':
            return None
        
        return self.entry_choice['choices'].index(desired_entry['user_option'])
    
    def FilterData(self, entries:list, choosen_index:int) -> dict:
        filtered_entry = entries[choosen_index]

        if self.format == 'ANIME':
            self.status = prompt(self.anime_status)
            if self.status.get("user_option") != "Plan to watch":
                episodes = input('How many episodes have you watched? ')
                filtered_entry['episode'] = episodes
        
        elif self.format == 'MANGA':
            self.status = prompt(self.manga_status)
            if self.status.get("user_option") != "Plan to read":
                chapters = input('How many chapters have you read? ')
                filtered_entry['chapters'] = chapters
        
        elif self.format == 'MOVIE':
            #get details omitted in the previous dict
            id = filtered_entry['id']
            unfiltered_entry = search.MovieData(id)

            filtered_entry = {} # Refresh the filtered

            # Add the relevant things
            filtered_entry['genre'] = []
            for i in range(len(unfiltered_entry['genres'])):
                filtered_entry['genre'].append(unfiltered_entry['genres'][i]['name'])

            filtered_entry['countryOfOrigin'] = []
            for i in range(len(unfiltered_entry['production_countries'])):
                filtered_entry['countryOfOrigin'].append(unfiltered_entry['production_countries'][i]['name'])

            filtered_entry['title']= {}
            filtered_entry['title']['original'] = unfiltered_entry['original_title']
            filtered_entry['title']['brazilian'] = input('Insira o título em português: ')
            filtered_entry['release_date'] = unfiltered_entry['release_date']
            filtered_entry['runtime'] = unfiltered_entry['runtime']

            self.status = prompt(self.movie_status)
        
        # Score and related stuff
        if self.status.get("user_option") not in ["Plan to watch", "Plan to read"]:
            score = prompt(self.score)
            filtered_entry['score'] = score['user_option']
        else:
            filtered_entry['score'] = False

        self.status = self.status['user_option'] #Make simple string
        filtered_entry['status'] = self.status
        filtered_entry['thoughts'] = input('Any final thoughts?\n')
        return filtered_entry

    def DbWrite(self, entry: dict, target_db: str, preset: list) -> None:
        # Check if file already configured, if needed configures it
        if os.path.exists(target_db) and os.stat(target_db).st_size != 0:
            with open(target_db, 'r') as file:
                entry_db = json.load(file)
        else:
            entry_db = preset

        # Find in which category should be placed the entry
        index = None
        for i, db_status in enumerate(entry_db):
            for key, value in db_status.items():
                if self.status == key:
                    index = i

        if index is not None:
            if self.format == 'MOVIE':
                entry_db[index][self.status].append({entry['title']['original']: entry})

            else:
                entry_db[index][self.status].append({entry['title']['romaji']: entry})

            with open(target_db, 'w') as file:
                json.dump(entry_db, file, indent=2, ensure_ascii=False)
        else:
            print(f"Category with status '{self.status}' not found.")

Interface = Interface()
Interface.AddEntry()