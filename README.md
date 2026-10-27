# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world recommendation systems like Spotify and YouTube analyze user behavior, content features, and preferences to predict what users may enjoy next. My recommender will use a simpler content-based approach that compares songs based on genre, mood, energy, tempo, valence, danceability, and acousticness. It will calculate a weighted similarity score for each song and rank songs from highest to lowest score, prioritizing songs that most closely match the user's preferences. Unlike large platforms, my version will focus on song characteristics rather than user history or the behavior of similar users.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
The recommender will use genre, mood, energy, tempo, valence, danceability, and acousticness to calculate similarity scores. The id, title, and artist fields will identify and display songs rather than directly determine similarity.

- What information does your `UserProfile` store
The UserProfile stores the user's music preferences, which the recommender uses to find similar songs. It includes:
- Preferred genre: The type of music the user enjoys.
- Preferred mood: The emotional tone the user prefers.
- Preferred energy: The desired energy level, from 0 to 1.
- Preferred tempo: The desired speed in beats per minute.
- Preferred valence: The preferred level of positivity or cheerfulness.
- Preferred danceability: How danceable the user wants the music to be.
- Preferred acousticness: The preferred acoustic sound level.
These preferences are compared with each song's features to calculate a similarity score and rank recommendations.

- How does your `Recommender` compute a score for each song
The Recommender computes a score for each song by comparing its features with the user's preferences. It awards 25 points for a matching genre and 20 points for a matching mood. For numerical features—energy, valence, tempo, danceability, and acousticness, it calculates similarity scores based on how close each song's values are to the user's preferred values, then multiplies them by their assigned weights. The points are added together to produce a total score out of 100. Songs with higher scores match the user's preferences more closely and are ranked higher in the recommendations.

| Feature | Maximum points |
|---|---|
| Genre match | 25 |
| Mood match | 20 |
| Energy similarity | 15 |
| Valence similarity | 15 |
| Tempo similarity | 10 |
| Danceability similarity | 10 |
| Acousticness similarity | 5 |
| **Total** | **100** |


- How do you choose which songs to recommend
I choose which songs to recommend by calculating a similarity score for each song based on the user's preferences. The process is:
- Compare each song's genre and mood with the user's preferred genre and mood.
- Calculate similarity scores for numerical features—energy, tempo, valence, danceability, and acousticness—giving higher scores to values closer to the user's preferences.
- Add the weighted points to get a total score out of 100.
- Sort the songs from highest to lowest score.
- Return the top three highest-scoring songs, excluding the song the user is already listening to.

This approach prioritizes songs that most closely match the user's musical preferences.

You can include a simple diagram or bullet list if helpful.
1. INPUT — User Preferences
Preferred genre, mood, energy, tempo, valence, danceability, acousticness
2. PROCESS — Read songs.csv
Load all songs and initialize an empty recommendation list.
3. THE LOOP — Evaluate Each Song
For each song in the CSV:
Compare its features with user preferences
Calculate a weighted similarity score (0–100)
Store the song and its score
4. RANK — Sort Recommendations
Sort all scored songs from highest to lowest. Exclude the currently selected song if needed.

### Algorithm Recipe (Final)

**Input:** a user profile (genre, mood, energy, tempo, valence, danceability, acousticness), the song catalog from `data/songs.csv`, and optionally the song currently playing.

**Step 1 — Score each song (0–100 points):**

| Feature | Rule | Max points |
|---|---|---|
| Genre | 25 if the song's genre equals the user's genre (case-insensitive), otherwise 0 | 25 |
| Mood | 20 if the song's mood equals the user's mood (case-insensitive), otherwise 0 | 20 |
| Energy | `(1 - abs(song - target)) × 15` | 15 |
| Valence | `(1 - abs(song - target)) × 15` | 15 |
| Tempo | `max(0, 1 - abs(song_bpm - target_bpm) / 122) × 10` | 10 |
| Danceability | `(1 - abs(song - target)) × 10` | 10 |
| Acousticness | `(1 - abs(song - target)) × 5` | 5 |
| **Total** | | **100** |

- Energy, valence, danceability, and acousticness are already on a 0–1 scale, so closeness is `1 - abs(difference)`.
- Tempo is in BPM, so the difference is divided by 122 (the catalog's BPM range, 54–176) to put it on the same 0–1 scale.
- Each rule that earns points adds a short reason (for example, "genre match (+25)" or "energy close to target (+14.4)") so every recommendation can be explained.

**Step 2 — Filter:** remove the song the user is currently listening to.

**Step 3 — Rank:** sort the remaining songs by total score, highest first. Ties keep their original CSV order.

**Step 4 — Return:** the top 3 songs, each with its score and reasons.

**Example:** for a user who likes pop / happy music with energy 0.8, tempo 120, valence 0.8, danceability 0.8, and acousticness 0.2, *Sunrise City* scores about 99, *Gym Hero* about 75, and *Rooftop Lights* about 73.

### Potential Biases I Expect

- **Labels over sound:** genre and mood are worth 45 points but only count on an exact match. In the example above, *Gym Hero* (pop, intense) beats *Rooftop Lights* (indie pop, happy) even though *Rooftop Lights* fits the user's happy mood better. Similar moods like "chill" and "relaxed" also get no credit.
- **Uneven catalog:** most genres have only one song, while lofi has three. Lofi and pop fans get strong matches, but fans of metal, classical, or salsa get at most one genre match. The rest of their list is filled by songs that only roughly match on energy and tempo.
- **Intensity counted more than once:** energy, tempo, and danceability usually rise together, so about 35 points mostly measure one thing. Acousticness is worth only 5 points, so acoustic preferences barely change the results.
- **Filter bubble:** each preference is a single target value, so users with varied taste can't be represented. Nothing rewards variety, so the top 3 tend to be very similar songs.
- **Subjective data:** each song has one genre and one mood picked by the dataset author, and the genre list leans toward Western music.
---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



