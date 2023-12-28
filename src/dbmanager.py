from PyInquirer import prompt
import search
import json
import click
import os

class UserInterface:
    #PyInquirer
    media_format_choice = {
        'type' : 'list',
        'name': 'user_option',
        'message': 'What entry do you want?',
        'choices': ['Anime', 'Manga', 'Movie', 'Cancel']
    }
    entry_choice = {
        'type' : 'list',
        'name': 'user_option',
        'message': 'What entry do you want?',
        'choices': []
    }

    anime_media_status =  {
        'type' : 'list',
        'name': 'user_option',
        'message': 'What is the media_status?',
        'choices': ['Watching', 'Finished', 'Dropped', 'Plan to watch'] 
    }
    manga_media_status =  {
        'type' : 'list',
        'name': 'user_option',
        'message': 'What is the media_status?',
        'choices': ['Reading', 'Finished', 'Dropped', 'Plan to read']           
    }

    movie_media_status =  {
        'type' : 'list',
        'name': 'user_option',
        'message': 'What is the media_status?',
        'choices': ['Watched', 'Plan to watch']           
    }

    score =  {
        'type' : 'list',
        'name': 'user_option',
        'message': 'What is the media_status?',
        'choices': ['Favorite', 'Very Good', 'Nice', 'Meh', 'Bad', 'Very Bad']           
    }

    media_status = False
    media_format = False

    @click.group()
    def cli():
        pass

    @staticmethod
    def media_formatChoice() -> list:
        media_format = prompt(UserInterface.media_format_choice)
        media_format = media_format.get("user_option")

        if media_format == "Anime":
            UserInterface.media_format = "ANIME"

        elif media_format == "Manga":
            UserInterface.media_format = "MANGA"

        elif media_format == "Movie": 
            UserInterface.media_format = "MOVIE"

        elif media_format == "Cancel":
            UserInterface.media_format = "CANCEL"

    @staticmethod
    def EntryChoice(entries:list) -> int: 
        if UserInterface.media_format == 'ANIME' or UserInterface.media_format == 'MANGA':
            for entry in entries:
                # Adaptative text
                if entry['title']['english'] != None and entry['title']['romaji'] :
                    entry_text = '{} ({}) -- {}\n'.format(
                        entry['title']['english'], entry['title']['romaji'],
                        entry['startDate']['year'])
                    
                elif entry['title']['english'] == None:
                    entry_text = '{} -- {}\n'.format(entry['title']['romaji'],
                        entry['startDate']['year'])
                
                elif entry['title']['english'] == None:
                    entry_text = '{} -- {}\n'.format(entry['title']['english'],
                        entry['startDate']['year'])
                UserInterface.entry_choice['choices'].append(entry_text) 
                       
        elif UserInterface.media_format == 'MOVIE':
            for entry in entries:
                entry_text = '{} -- {}\n'.format(entry['original_title'], entry['release_date'])
                UserInterface.entry_choice['choices'].append(entry_text)
        
        UserInterface.entry_choice['choices'].append('None')
        
        #Visual stuff
        desired_entry = prompt(UserInterface.entry_choice)
        desired_entry = desired_entry.get("user_option")
        
        if desired_entry == 'None':
            return None
        
        return UserInterface.entry_choice['choices'].index(desired_entry)

    def media_statusChoice() -> None:
        if UserInterface.media_format == 'ANIME':
            UserInterface.media_status = prompt(UserInterface.anime_media_status)
        
        elif UserInterface.media_format == 'MANGA':
            UserInterface.media_status = prompt(UserInterface.manga_media_status)
        
        elif UserInterface.media_format == 'MOVIE':
            UserInterface.media_status = prompt(UserInterface.movie_media_status)
        
        UserInterface.media_status = UserInterface.media_status['user_option'] #Make simple string

    def FinalProcessing(desired_entry:dict, score, thoughts_ignore) -> dict:
        desired_entry['media_status'] = UserInterface.media_status
        desired_entry['thoughts'] = False

        # Score
        if score != None:
            desired_entry['score'] = score
        
        else:
            if UserInterface.media_status not in ["Plan to watch", "Plan to read"]:
                score = prompt(UserInterface.score)
                desired_entry['score'] = score['user_option']
            else:
                desired_entry['score'] = None
        
        # Thoughts
        if thoughts_ignore == True:
            desired_entry['thoughts'] = None

        else:
            desired_entry['thoughts'] = input('Any final thoughts?\n')

        return desired_entry

class DataProcessor:
    @staticmethod
    def AnimeProcessor(desired_entry:dict, episodes_watched) -> dict:
        #Removing junk
        desired_entry.pop('chapters')

        #Episodes stuff
        if episodes_watched != None:
            desired_entry['episodes_watched'] = episodes_watched

            return desired_entry

        if UserInterface.media_status == "Plan to watch":
            desired_entry['episodes_watched'] = 0
            return desired_entry

        while True:
            try:
                #Adaptaive text
                if desired_entry['episodes'] != None:
                    episodes_watched = int(input(f'How many episodes have you watched? Total of {desired_entry["episodes"]}: '))
                
                else:
                    episodes_watched = int(input(f'How many episodes have you watched? '))
                
                #Response check
                if desired_entry['episodes'] != None:
                    if episodes_watched > desired_entry['episodes']:
                        print('Please enter a value between 1 and {}.'.media_format(desired_entry['episodes']))
                    else: 
                        desired_entry['episodes_watched'] = episodes_watched
                        break
                else:
                    desired_entry['episodes_watched'] = episodes_watched
                    break

            except ValueError:
                print('Please enter a valid numerical value for the number of episodes.')

        return desired_entry
    
    @staticmethod
    def MangaProcessor(desired_entry:dict, chapters_read=None) -> dict:   
        #Removing junk
        desired_entry.pop('duration')
        desired_entry.pop('episodes')

        #Chapters stuff
        if chapters_read != None:
            desired_entry['chapters_read'] = chapters_read

            return desired_entry

        elif UserInterface.media_status == "Plan to read":
                desired_entry['chapters_read'] = 0

                return desired_entry
        
        while True:
            try:
                #Adaptaive text
                if desired_entry['chapters'] != None:                    chapters_read = int(input(f'How many chapters have you read? Total of {desired_entry["chapters"]}:  '))
                
                else:
                    chapters_read = int(input(f'How many chapters have you read? '))

                # #Response check
                if desired_entry['chapters'] != None:
                    if chapters_read > desired_entry['chapters']:
                        print('Please enter a value between 1 and {}.'.media_format(desired_entry['chapters']))
                    else: 
                        print(chapters_read)
                        desired_entry['chapters_read'] = chapters_read
                        break
                else:
                    desired_entry['chapters_read'] = chapters_read
                    break

            except ValueError:
                print('Please enter a valid numerical value for the number of chapters.')

        return desired_entry

    @staticmethod    
    def MovieProcessor(desired_entry:dict) -> dict:
        #get details omitted in the previous dict
        id = desired_entry['id']
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
        filtered_entry['title']['english'] = unfiltered_entry['original_title']
        filtered_entry['title']['brazilian'] = input('Insira o título em português: ')
        filtered_entry['release_date'] = unfiltered_entry['release_date']
        filtered_entry['runtime'] = unfiltered_entry['runtime']

        return filtered_entry

    @staticmethod
    def InfoUpdate(entry:dict, db:dict, action:str):
        if action == 'ADD':
            if UserInterface.media_format == 'ANIME':
                time_add = entry['duration']*entry['episodes_watched']

                db['List'][0]['Info']['total_time'] += time_add
                db['List'][0]['Info']['episodes_watched'] += entry['episodes_watched']
                db['List'][0]['Info']['anime_seen'] += 1

            if UserInterface.media_format == 'MANGA':
                db['List'][0]['Info']['chapters_read'] += entry['chapters_read']
                db['List'][0]['Info']['manga_read'] += 1

            if UserInterface.media_format == 'MOVIE':
                db['List'][0]['Info']['total_time'] += entry['runtime']
                db['List'][0]['Info']['watched_movies'] += 1

        if action == 'REMOVE':
            pass

class DatabaseHandler:
    path = r'./Databases' #Path to Databases directory (make sure it exists)  

    #PyInquirer
    anime_preset = {"List": [
        {'Info': {'total_time': 0, 'episodes_watched': 0, 'anime_seen': 0}},
        {'Watching': []},
        {'Finished': []},
        {'Dropped': []},
        {'Plan to watch': []}
    ]}

    manga_preset = {"List": [
        {'Info': {'chapters_read': 0, 'manga_read': 0}},
        {'Reading': []},
        {'Finished': []},
        {'Dropped': []},
        {'Plan to watch': []}
    ]}
    movie_preset = {"List": [
        {'Info': {'total_time': 0, 'watched_movies': 0}},
        {'Plan to watch': []},
        {'Watched': []}
    ]}

    @staticmethod
    def DbWrite(entry: dict, target_db: str, preset: list) -> None:
        # Check if file already configured, if needed configures it
        if os.path.exists(target_db) and os.stat(target_db).st_size != 0:
            with open(target_db, 'r', encoding='utf-8') as file:
                entry_db = json.load(file)
        else:
            entry_db = preset

        # Find in which category should be placed the entry
        index = None
        for i, db_media_status in enumerate(entry_db['List']):
            for key, value in db_media_status.items():
                if UserInterface.media_status == key:
                    index = i
        
        if index is not None:
            # Add entry
            entry_db["List"][index][UserInterface.media_status].append(entry)

            # Info section_update
            DataProcessor.InfoUpdate(entry, entry_db, 'ADD')

            # Save to file
            with open(target_db, 'w', encoding='utf-8') as file:
                json.dump(entry_db, file, indent=2, ensure_ascii=False)
            
            print('Succefully written to file')
        else:
            print(f"Category with media_status '{UserInterface.media_status}' not found.")

    def DbLoad(target_db:str) -> dict:
        if os.path.exists(target_db) and os.stat(target_db).st_size != 0:
            with open(target_db, 'r', encoding='utf-8') as file:
                return json.load(file)
        else:
            return "Error: file without necessary info!"

class InterfaceManager:
    @staticmethod
    @UserInterface.cli.command()
    @click.option('--media_format', default=None, help='Possible formats: Anime, Manga, Movie, Cancel')
    @click.option('--media_name', default=None, help='Media name')
    @click.option("--amount", type=int, default=None, help='Only valid for Anime and Manga, the amount of them you saw')
    @click.option("--media_status", default=None, help='See valid media_status for each entry')
    @click.option("--score",  default=None, help='Score selection. Possible values: Favorite, Very Nice, Nice, Meh, Bad, Very bad')
    @click.option("--entry_ignore", type=bool, default=False, help='Ignore manual entry selection, first apperance selected')
    @click.option("--thoughts_ignore", type=bool, default=False, help='Ignore thoughts definition')
    def AddEntry(media_format, media_name, amount, media_status, score, entry_ignore, thoughts_ignore) -> None:
        #Verify args
        if media_format != None:
            media_format = media_format.upper()
            if media_format not in ["ANIME", "MANGA", "MOVIE"]:
                print("Invalid media_format")
                media_format = None
        
        if amount != None:
            if type(amount) != int:
                print("Invalid amount")
                amount = None
        
        #media_status check later in code
        if score != None:
            if score not in ['Favorite', 'Very Nice', 'Nice', 'Meh', 'Bad', 'Very bad']:
                print("Invalid score!")
                score = None

        # media_format choose
        if media_format == None:
            UserInterface.media_formatChoice() #chooses the media_format
        
        else:
            UserInterface.media_format = media_format
        
        #Check if cancelled
        if UserInterface.media_format == "CANCEL":
            print("Operation cancelled!")
            return "Operation cancelled!"

        # Search entries
        if media_name == None:
            media_name = input('Please input the name of the desired media: ').strip()
        
        if UserInterface.media_format == "ANIME":
            media_data =  search.AnilistData(media_name, UserInterface.media_format)["data"]["Page"]["media"] #removes  junk

        elif UserInterface.media_format == "MANGA":
            media_data =  search.AnilistData(media_name, UserInterface.media_format)["data"]["Page"]["media"] #removes  
        
        elif UserInterface.media_format == "MOVIE":
            media_data = search.MovieSearch(media_name)['results']
        
        else:
            print("Invalid media_format!")
            return "Error: Invalid media_format"

        # Check if media was found
        if media_data == []:
            print("Couldn't find the desired media!")
            return "Error: entry not found"

        # Choosing entry
        if entry_ignore == True:
            entry_index = 0
        
        else:
            entry_index = UserInterface.EntryChoice(media_data)

        if entry_index == None:
            print("Operation cancelled!")
            return "Operation cancelled!"

        # Define entry dict
        desired_entry = media_data[entry_index]
        
        # media_status choice
        # Check media_status arg validity
        if media_status != None:            
            if media_format == "ANIME":
                if media_status not in UserInterface.anime_media_status["choices"]:
                    media_status = None
            
            elif media_format == "MANGA":
                if media_status not in UserInterface.manga_media_status["choices"]:
                    media_status = None
            
            elif media_format == "MOVIE":
                if media_status not in UserInterface.movie_media_status["choices"]:
                    media_status = None
            
            else:
                media_status = None

        if media_status == None:
            UserInterface.media_statusChoice()
        
        else:
            UserInterface.media_status = media_status
        
        # Data filtering
        if UserInterface.media_format == 'ANIME':
            filtered_data = DataProcessor.AnimeProcessor(desired_entry, amount)
        
        elif UserInterface.media_format == 'MANGA':
            filtered_data = DataProcessor.MangaProcessor(desired_entry, amount)
        
        elif UserInterface.media_format == 'MOVIE':
            filtered_data = DataProcessor.MovieProcessor(desired_entry)

        filtered_data = UserInterface.FinalProcessing(filtered_data, score, thoughts_ignore)
        
        if UserInterface.media_format == "ANIME": 
            DatabaseHandler.DbWrite(filtered_data, DatabaseHandler.path + r'/anime_db.json', DatabaseHandler.anime_preset)

        elif UserInterface.media_format == "MANGA": 
            DatabaseHandler.DbWrite(filtered_data, DatabaseHandler.path + r'/manga_db.json', DatabaseHandler.manga_preset)

        elif UserInterface.media_format == "MOVIE": 
            DatabaseHandler.DbWrite(filtered_data, DatabaseHandler.path + r'/movie_db.json', DatabaseHandler.movie_preset)

    def RemoveEntry():
        pass

    if __name__ == '__main__':
        UserInterface.cli()