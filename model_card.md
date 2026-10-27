# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

My recommender works like a points game. Every song in the catalog has the same kinds of information about how it sounds:

- **Genre:** what style it is, like pop, lofi, or rock.
- **Mood:** the feeling it gives off, like happy, chill, or intense.
- **Energy:** how calm or intense it feels.
- **Tempo:** how fast it is, in beats per minute.
- **Valence:** how cheerful or sad it sounds.
- **Danceability:** how easy it is to dance to.
- **Acousticness:** how much it sounds like real instruments rather than electronic ones.

The user describes what they like using those same seven things, for example "happy pop songs with a lot of energy that aren't very acoustic."

Then every song gets a score out of 100 points:

- **Genre (25 points) and mood (20 points):** a song gets all of these points if it matches what the user asked for, and none if it doesn't. There is no partial credit.
- **The other five (55 points total):** these are worth more the closer the song is to what the user wants. A song that is almost exactly as energetic as the user asked for gets nearly all of the energy points. A song that is much calmer gets only a few. Energy and cheerfulness are worth 15 points each, tempo and danceability 10 each, and acousticness 5.

After every song has a score, the recommender lines them up from highest to lowest. It skips the song the user is already listening to and suggests the top five. Each suggestion comes with a short list of reasons, like "genre match (+25)" or "energy close to target (+14.7)," so the user can see why it was picked.

**Changes from the starter logic:** the starter code did not score songs at all. It just returned the first few songs in the file. The starter's user profile only had genre, mood, energy, and a yes/no "likes acoustic" setting. I added tempo, cheerfulness, and danceability. I also changed acoustic sound from a yes/no question to a sliding scale. I made genre and mood the biggest factors because they are the clearest signals of taste. I also added the reasons so every recommendation can be explained.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
