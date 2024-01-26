# DB manager
This is a small program I've written to manage json databases regarding anime, mangas and movies I've written.

## How to make it work?
Clone repo and create a file called settings.py, in it add the following:
```python
MovieTOKEN = 'YOUR MOVIE TOKEN FROM TMDB'
folderPath = r'DESIRED PATH, MAKE SURE IS COMPLETE'
```

## FAQ:
### Why python?
Easy to read and mantain.

### How can I make it stop pushing to origin after each comit?
Comment this line:
```python
os.system("git push origin main")        
```

### Why didn't you use AnilistPython?
Well, it's a bit overkill for the project. The only thing I really needed was the hability to search manga and anime by name.

### Roadmap
- [ ] Add support for books
- [ ] Add support for light novels (will need to write API)
- [ ] Add editing mode 