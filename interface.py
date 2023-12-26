from PyInquirer import prompt
import search
import json
import os

class UserInterface:
    #PyInquirer
    format_choice = {
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

    anime_status =  {
        'type' : 'list',
        'name': 'user_option',
        'message': 'What is the status?',
        'choices': ['Watching', 'Finished', 'Dropped', 'Plan to watch'] 
    }
    manga_status =  {
        'type' : 'list',
        'name': 'user_option',
        'message': 'What is the status?',
        'choices': ['Reading', 'Finished', 'Dropped', 'Plan to read']           
    }

    movie_status =  {
        'type' : 'list',
        'name': 'user_option',
        'message': 'What is the status?',
        'choices': ['Watched', 'Plan to watch']           
    }

    score =  {
        'type' : 'list',
        'name': 'user_option',
        'message': 'What is the status?',
        'choices': ['Favorite', 'Very Good', 'Nice', 'Meh', 'Bad', 'Very Bad']           
    }

    status = False
    format = False

    @staticmethod
    def FormatChoice() -> list:
        format = prompt(UserInterface.format_choice)

        if format.get("user_option") == "Anime":
            UserInterface.format = "ANIME"

            anime_name = input('Please input the name of the desired anime: ').strip()

            return search.AnilistData(anime_name, UserInterface.format)["data"]["Page"]["media"] #removes  junk

        elif format.get("user_option") == "Manga":
            UserInterface.format = "MANGA"

            manga_name = input('Please input the name of the desired manga: ').strip()
            return search.AnilistData(manga_name, UserInterface.format)["data"]["Page"]["media"] #removes  junk

        elif format.get("user_option") == "Movie": 
            UserInterface.format = "MOVIE"

            movie_name = input('Please input the name of the desired movie: ').strip()
            return search.MovieSearch(movie_name)['results']

        elif format.get("user_option") == "Cancel":
            return 'Operation cancelled'

    @staticmethod
    def EntryChoice(entries:list) -> int: 
        if UserInterface.format == 'ANIME' or UserInterface.format == 'MANGA':
            # Text
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
                       
        elif UserInterface.format == 'MOVIE':
            for entry in entries:
                entry_text = '{} -- {}\n'.format(entry['original_title'], entry['release_date'])
                UserInterface.entry_choice['choices'].append(entry_text)
        
        UserInterface.entry_choice['choices'].append('None')
        
        #Visual stuff
        desired_entry = prompt(UserInterface.entry_choice)
        
        if desired_entry['user_option'] == 'None':
            return None
        
        return UserInterface.entry_choice['choices'].index(desired_entry['user_option'])

    def StatusChoice() -> None:
        if UserInterface.format == 'ANIME':
            UserInterface.status = prompt(UserInterface.anime_status)
        
        elif UserInterface.format == 'MANGA':
            UserInterface.status = prompt(UserInterface.manga_status)
        
        elif UserInterface.format == 'MOVIE':
            UserInterface.status = prompt(UserInterface.movie_status)
        
        UserInterface.status = UserInterface.status['user_option'] #Make simple string

    def FinalProcessing(desired_entry:dict) -> dict:
        # Score and related stuff
        if UserInterface.status not in ["Plan to watch", "Plan to read"]:
            score = prompt(UserInterface.score)
            desired_entry['score'] = score['user_option']
        else:
            desired_entry['score'] = False

        desired_entry['status'] = UserInterface.status
        desired_entry['thoughts'] = input('Any final thoughts?\n')

        return desired_entry

class DataProcessor:
    def AnimeProcessor(desired_entry:dict) -> dict:
        #Removing junk
        desired_entry.pop('chapters')

        #Episodes stuff
        if UserInterface.status == "Plan to watch":
            desired_entry['episodes_watched'] = 0
            return desired_entry

        while True:
            try:
                #Adaptaive text
                if desired_entry['episodes'] != None:
                    episodes = int(input(f'How many episodes have you read? Total of {desired_entry["episodes"]}  '))
                
                else:
                    episodes = int(input(f'How many episodes have you read? '))
                
                #Response check
                if desired_entry['episodes'] != None:
                    if episodes > desired_entry['episodes']:
                        print('Please enter a value between 1 and {}.'.format(desired_entry['episodes']))
                    else: 
                        desired_entry['episodes_watched'] = episodes
                        break
                else:
                    break

            except ValueError:
                print('Please enter a valid numerical value for the number of episodes.')

        return desired_entry
    
    @staticmethod
    def MangaProcessor(desired_entry:dict) -> dict:   
        #Removing junk
        desired_entry.pop('duration')
        desired_entry.pop('episodes')

        #Chapters stuff
        print("Status: " + UserInterface.status)
        if UserInterface.status == "Plan to read":
                desired_entry['chapters_read'] = 0

                return desired_entry
        
        while True:
            try:
                #Adaptaive text
                if desired_entry['chapters'] != None:
                    chapters = int(input(f'How many chapters have you read? Total of {desired_entry["chapters"]}  '))
                
                else:
                    chapters = int(input(f'How many chapters have you read? '))

                # #Response check
                if desired_entry['chapters'] != None:
                    if chapters > desired_entry['chapters']:
                        print('Please enter a value between 1 and {}.'.format(desired_entry['chapters']))
                    else: 
                        desired_entry['chapters_read'] = chapters
                        break
                else:
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
            if UserInterface.format == 'ANIME':
                time_add = entry['duration']*entry['episodes_watched']

                db['List'][0]['Info']['total_time'] += time_add
                db['List'][0]['Info']['episodes_watched'] += entry['episodes_watched']
                db['List'][0]['Info']['anime_seen'] += 1

            if UserInterface.format == 'MANGA':
                db['List'][0]['Info']['chapters_read'] += entry['chapters_read']
                db['List'][0]['Info']['manga_read'] += 1

            if UserInterface.format == 'MOVIE':
                db['List'][0]['Info']['total_time'] += entry['runtime']
                db['List'][0]['Info']['watched_movies'] += 1

        if action == 'REMOVE':
            pass

class DatabaseHandler:
    path = r'../Site/Lists/Databases' #Path to Databases directory (make sure it exists)  

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
        for i, db_status in enumerate(entry_db['List']):
            for key, value in db_status.items():
                if UserInterface.status == key:
                    index = i
        
        if index is not None:
            # Add entry
            entry_db["List"][index][UserInterface.status].append(entry)

            # Info section_update
            DataProcessor.InfoUpdate(entry, entry_db, 'ADD')

            # Save to file
            with open(target_db, 'w', encoding='utf-8') as file:
                json.dump(entry_db, file, indent=2, ensure_ascii=False)
            
            print('Succefully written to file')
        else:
            print(f"Category with status '{UserInterface.status}' not found.")

class InterfaceManager:
    @staticmethod
    def AddEntry() -> None:
        media_data = UserInterface.FormatChoice() #chooses the format
        
        # Check for errors in request
        if isinstance(media_data, str):
            return False

        entry_index = UserInterface.EntryChoice(media_data)
        
        # Check if user opted for 'None'
        if entry_index == None:
            return False

        UserInterface.StatusChoice()

        # Define entry dict
        desired_entry = media_data[entry_index]
        
        # Data filtering
        if UserInterface.format == 'ANIME':
            filtered_data = DataProcessor.AnimeProcessor(desired_entry)
        
        elif UserInterface.format == 'MANGA':
            filtered_data = DataProcessor.MangaProcessor(desired_entry)
        
        elif UserInterface.format == 'MOVIE':
            filtered_data = DataProcessor.MovieProcessor(desired_entry)

        filtered_data = UserInterface.FinalProcessing(filtered_data)
        
        if UserInterface.format == "ANIME": 
            DatabaseHandler.DbWrite(filtered_data, DatabaseHandler.path + r'/anime_db.json', DatabaseHandler.anime_preset)

        elif UserInterface.format == "MANGA": 
            DatabaseHandler.DbWrite(filtered_data, DatabaseHandler.path + r'/manga_db.json', DatabaseHandler.manga_preset)

        elif UserInterface.format == "MOVIE": 
            DatabaseHandler.DbWrite(filtered_data, DatabaseHandler.path + r'/movie_db.json', DatabaseHandler.movie_preset)

InterfaceManager.AddEntry()