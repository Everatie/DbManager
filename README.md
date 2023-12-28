# DB manager
This is a small program I've written to manage json databases regarding anime, mangas and movies.

## FAQ:
### Why python?
Easy to read and to mantain.

### Why didn't you use AnilistPython?
Well, it's a bit overkill for the project. The only thing I really needed was the hability to search manga and anime by their name.

### Setup:
To get started, create a file named `secret.py` and add the following line: 

```python
MovieTOKEN = "YOURMOVIETOKEN"
```

Replace "YOURMOVIETOKEN" with your own TMDB token, which you can obtain from  ([The Movie Database API]: https://developer.themoviedb.org/v4/reference/auth-create-access-token).

Then, set the folder where the files will be saved (see dbHandler path variable). Make sure that the dir do exist!

### Roadmap?
- [x] Search APIs working
- [x] AddEntry functional
- [x] PyInquirer
- [x] Saving working
- [x] Class rework
- [x] Click integration
- [ ] Numpy implementation 
- [ ] RemoveEntry
- [ ] EditEntry 