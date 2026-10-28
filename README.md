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
The Recommender computes a score for each song by comparing its features with the user's preferences. It awards 15 points for a matching genre and 15 points for a matching mood. For numerical features—energy, valence, tempo, danceability, and acousticness, it calculates similarity scores based on how close each song's values are to the user's preferred values, then multiplies them by their assigned weights. The points are added together to produce a total score out of 100. Songs with higher scores match the user's preferences more closely and are ranked higher in the recommendations.

| Feature | Maximum points |
|---|---|
| Genre match | 15 |
| Mood match | 15 |
| Energy similarity | 20 |
| Valence similarity | 20 |
| Tempo similarity | 10 |
| Danceability similarity | 10 |
| Acousticness similarity | 10 |
| **Total** | **100** |


- How do you choose which songs to recommend
I choose which songs to recommend by calculating a similarity score for each song based on the user's preferences. The process is:
- Compare each song's genre and mood with the user's preferred genre and mood.
- Calculate similarity scores for numerical features—energy, tempo, valence, danceability, and acousticness—giving higher scores to values closer to the user's preferences.
- Add the weighted points to get a total score out of 100.
- Sort the songs from highest to lowest score.
- Return the top five highest-scoring songs, excluding the song the user is already listening to.

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
| Genre | 15 if the song's genre equals the user's genre (case-insensitive), otherwise 0 | 15 |
| Mood | 15 if the song's mood equals the user's mood (case-insensitive), otherwise 0 | 15 |
| Energy | `(1 - abs(song - target)) × 20` | 20 |
| Valence | `(1 - abs(song - target)) × 20` | 20 |
| Tempo | `max(0, 1 - abs(song_bpm - target_bpm) / 122) × 10` | 10 |
| Danceability | `(1 - abs(song - target)) × 10` | 10 |
| Acousticness | `(1 - abs(song - target)) × 10` | 10 |
| **Total** | | **100** |

- Energy, valence, danceability, and acousticness are already on a 0–1 scale, so closeness is `1 - abs(difference)`.
- Tempo is in BPM, so the difference is divided by 122 (the catalog's BPM range, 54–176) to put it on the same 0–1 scale.
- Each rule that earns points adds a short reason (for example, "genre match (+15)" or "energy close to target (+19.2)") so every recommendation can be explained.

**Step 2 — Filter:** remove the song the user is currently listening to.

**Step 3 — Rank:** sort the remaining songs by total score, highest first. Ties keep their original CSV order.

**Step 4 — Return:** the top 5 songs, each with its score and reasons.

**Example:** for a user who likes pop / happy music with energy 0.8, tempo 120, valence 0.8, danceability 0.8, and acousticness 0.2, *Sunrise City* scores about 98, *Rooftop Lights* about 82, and *Gym Hero* about 79.

**Weight change:** the first version gave genre 25, mood 20, energy 15, valence 15, and acousticness 5. Edge-case testing showed the 45 label points could override the numbers: a user asking for pop / intense but quiet, acoustic music still got *Gym Hero* first. Lowering genre and mood to 15 each and moving those points to energy, valence, and acousticness fixed that without changing the top results for the normal profiles.

### Potential Biases I Expect

- **Labels over sound:** genre and mood are worth 30 points but only count on an exact match. With the original weights (45 label points), *Gym Hero* (pop, intense) beat *Rooftop Lights* (indie pop, happy) in the example above even though *Rooftop Lights* fits the user's happy mood better; "indie pop" still gets no credit for "pop". Similar moods like "chill" and "relaxed" also get no credit.
- **Uneven catalog:** most genres have only one song, while lofi has three. Lofi and pop fans get strong matches, but fans of metal, classical, or salsa get at most one genre match. The rest of their list is filled by songs that only roughly match on energy and tempo.
- **Intensity counted more than once:** energy, tempo, and danceability usually rise together, so about 40 points mostly measure one thing. Acousticness is worth only 10 points, so acoustic preferences change the results less than intensity does.
- **Filter bubble:** each preference is a single target value, so users with varied taste can't be represented. Nothing rewards variety, so the top 5 tend to be very similar songs.
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

Loading songs from data/songs.csv...
Loaded songs: 20

=== High-Energy Pop ===
User profile: genre=pop, mood=happy, energy=0.85, tempo_bpm=125, valence=0.8, danceability=0.85, acousticness=0.1
Recommendations:
  1. Sunrise City by Neon Echo - Score: 81.63
     Because: genre match (+15); energy close to target (+19.4); valence close to target (+19.2); tempo_bpm close to target (+9.4); danceability close to target (+9.4); acousticness close to target (+9.2)
  2. Gym Hero by Max Pulse - Score: 81.43
     Because: genre match (+15); energy close to target (+18.4); valence close to target (+19.4); tempo_bpm close to target (+9.4); danceability close to target (+9.7); acousticness close to target (+9.5)
  3. Runway Lights by Avery Lane - Score: 68.55
     Because: energy close to target (+20.0); valence close to target (+19.6); tempo_bpm close to target (+9.8); danceability close to target (+9.4); acousticness close to target (+9.8)
  4. Rooftop Lights by Indigo Parade - Score: 65.12
     Because: energy close to target (+18.2); valence close to target (+19.8); tempo_bpm close to target (+9.9); danceability close to target (+9.7); acousticness close to target (+7.5)
  5. Neon Mirage by Pixel Mirage - Score: 61.85
     Because: energy close to target (+19.2); valence close to target (+13.2); tempo_bpm close to target (+9.8); danceability close to target (+9.9); acousticness close to target (+9.8)

=== Chill Lofi ===
User profile: genre=lofi, mood=chill, energy=0.38, tempo_bpm=76, valence=0.58, danceability=0.6, acousticness=0.8
Recommendations:
  1. Focus Flow by LoRoom - Score: 83.87
     Because: genre match (+15); energy close to target (+19.6); valence close to target (+19.8); tempo_bpm close to target (+9.7); danceability close to target (+10.0); acousticness close to target (+9.8)
  2. Library Rain by Paper Lanterns - Score: 82.87
     Because: genre match (+15); energy close to target (+19.4); valence close to target (+19.6); tempo_bpm close to target (+9.7); danceability close to target (+9.8); acousticness close to target (+9.4)
  3. Midnight Coding by LoRoom - Score: 82.54
     Because: genre match (+15); energy close to target (+19.2); valence close to target (+19.6); tempo_bpm close to target (+9.8); danceability close to target (+9.8); acousticness close to target (+9.1)
  4. Desert Postcard by Sage & Sand - Score: 65.24
     Because: energy close to target (+19.0); valence close to target (+19.8); tempo_bpm close to target (+9.3); danceability close to target (+8.5); acousticness close to target (+8.6)
  5. Coffee Shop Stories by Slow Stereo - Score: 64.55
     Because: energy close to target (+19.8); valence close to target (+17.4); tempo_bpm close to target (+8.9); danceability close to target (+9.4); acousticness close to target (+9.1)

=== Deep Intense Rock ===
User profile: genre=rock, mood=intense, energy=0.92, tempo_bpm=150, valence=0.4, danceability=0.6, acousticness=0.08
Recommendations:
  1. Storm Runner by Voltline - Score: 82.24
     Because: genre match (+15); energy close to target (+19.8); valence close to target (+18.4); tempo_bpm close to target (+9.8); danceability close to target (+9.4); acousticness close to target (+9.8)
  2. Iron Pulse by Black Anvil - Score: 64.82
     Because: energy close to target (+19.0); valence close to target (+19.0); tempo_bpm close to target (+8.5); danceability close to target (+8.8); acousticness close to target (+9.5)
  3. Neon Mirage by Pixel Mirage - Score: 62.20
     Because: energy close to target (+17.8); valence close to target (+18.8); tempo_bpm close to target (+8.2); danceability close to target (+7.4); acousticness close to target (+10.0)
  4. Night Drive Loop by Neon Echo - Score: 58.82
     Because: energy close to target (+16.6); valence close to target (+18.2); tempo_bpm close to target (+6.7); danceability close to target (+8.7); acousticness close to target (+8.6)
  5. Gym Hero by Max Pulse - Score: 57.82
     Because: energy close to target (+19.8); valence close to target (+12.6); tempo_bpm close to target (+8.5); danceability close to target (+7.2); acousticness close to target (+9.7)

=== Sad but Hype (mood not in catalog) ===
User profile: mood=sad, energy=0.9, tempo_bpm=150, valence=0.2
Recommendations:
  1. Iron Pulse by Black Anvil - Score: 44.12
     Because: energy close to target (+18.6); valence close to target (+17.0); tempo_bpm close to target (+8.5)
  2. Storm Runner by Voltline - Score: 44.04
     Because: energy close to target (+19.8); valence close to target (+14.4); tempo_bpm close to target (+9.8)
  3. Neon Mirage by Pixel Mirage - Score: 41.20
     Because: energy close to target (+18.2); valence close to target (+14.8); tempo_bpm close to target (+8.2)
  4. Night Drive Loop by Neon Echo - Score: 37.92
     Because: energy close to target (+17.0); valence close to target (+14.2); tempo_bpm close to target (+6.7)
  5. Gym Hero by Max Pulse - Score: 36.52
     Because: energy close to target (+19.4); valence close to target (+8.6); tempo_bpm close to target (+8.5)

=== Labels vs Numbers (pop/intense but quiet) ===
User profile: genre=pop, mood=intense, energy=0.1, tempo_bpm=60, valence=0.2, danceability=0.2, acousticness=0.95
Recommendations:
  1. Quiet Snowfall by Eira North - Score: 59.01
     Because: energy close to target (+18.8); valence close to target (+11.4); tempo_bpm close to target (+9.5); danceability close to target (+9.8); acousticness close to target (+9.5)
  2. Velvet Waltz by Mira Sol - Score: 58.84
     Because: energy close to target (+17.2); valence close to target (+13.6); tempo_bpm close to target (+9.3); danceability close to target (+9.0); acousticness close to target (+9.7)
  3. Spacewalk Thoughts by Orbit Bloom - Score: 55.00
     Because: energy close to target (+16.4); valence close to target (+11.0); tempo_bpm close to target (+10.0); danceability close to target (+7.9); acousticness close to target (+9.7)
  4. Blue Hour by June Harbor - Score: 54.19
     Because: energy close to target (+13.4); valence close to target (+17.8); tempo_bpm close to target (+8.7); danceability close to target (+7.1); acousticness close to target (+7.2)
  5. Desert Postcard by Sage & Sand - Score: 53.43
     Because: energy close to target (+15.4); valence close to target (+12.6); tempo_bpm close to target (+8.0); danceability close to target (+7.5); acousticness close to target (+9.9)

=== Near-Miss Genre (indie pop described as pop) ===
User profile: genre=pop, mood=happy, energy=0.76, tempo_bpm=124, valence=0.81, danceability=0.82, acousticness=0.35
Recommendations:
  1. Sunrise City by Neon Echo - Score: 80.71
     Because: genre match (+15); energy close to target (+18.8); valence close to target (+19.4); tempo_bpm close to target (+9.5); danceability close to target (+9.7); acousticness close to target (+8.3)
  2. Gym Hero by Max Pulse - Score: 76.54
     Because: genre match (+15); energy close to target (+16.6); valence close to target (+19.2); tempo_bpm close to target (+9.3); danceability close to target (+9.4); acousticness close to target (+7.0)
  3. Rooftop Lights by Indigo Parade - Score: 70.00
     Because: energy close to target (+20.0); valence close to target (+20.0); tempo_bpm close to target (+10.0); danceability close to target (+10.0); acousticness close to target (+10.0)
  4. Runway Lights by Avery Lane - Score: 64.64
     Because: energy close to target (+18.2); valence close to target (+19.8); tempo_bpm close to target (+9.8); danceability close to target (+9.1); acousticness close to target (+7.7)
  5. Island Motion by Coral Beat - Score: 64.60
     Because: energy close to target (+18.8); valence close to target (+18.6); tempo_bpm close to target (+7.7); danceability close to target (+9.8); acousticness close to target (+9.7)

=== Ghost Genre (k-pop not in catalog) ===
User profile: genre=k-pop, mood=happy, energy=0.8
Recommendations:
  1. Neon Mirage by Pixel Mirage - Score: 19.80
     Because: energy close to target (+19.8)
  2. Sunrise City by Neon Echo - Score: 19.60
     Because: energy close to target (+19.6)
  3. Rooftop Lights by Indigo Parade - Score: 19.20
     Because: energy close to target (+19.2)
  4. Night Drive Loop by Neon Echo - Score: 19.00
     Because: energy close to target (+19.0)
  5. Runway Lights by Avery Lane - Score: 19.00
     Because: energy close to target (+19.0)

=== Whitespace in Labels ===
User profile: genre= Lofi, mood=chill 
Recommendations:
  1. Sunrise City by Neon Echo - Score: 0.00
     Because: 
  2. Midnight Coding by LoRoom - Score: 0.00
     Because: 
  3. Storm Runner by Voltline - Score: 0.00
     Because: 
  4. Library Rain by Paper Lanterns - Score: 0.00
     Because: 
  5. Gym Hero by Max Pulse - Score: 0.00
     Because: 

=== Out-of-Range Values ===
User profile: energy=2.0, valence=-1.0
Recommendations:
  1. Sunrise City by Neon Echo - Score: 0.00
     Because: 
  2. Midnight Coding by LoRoom - Score: 0.00
     Because: 
  3. Storm Runner by Voltline - Score: 0.00
     Because: 
  4. Library Rain by Paper Lanterns - Score: 0.00
     Because: 
  5. Gym Hero by Max Pulse - Score: 0.00
     Because: 

=== Genre Only (ties) ===
User profile: genre=lofi
Recommendations:
  1. Midnight Coding by LoRoom - Score: 15.00
     Because: genre match (+15)
  2. Library Rain by Paper Lanterns - Score: 15.00
     Because: genre match (+15)
  3. Focus Flow by LoRoom - Score: 15.00
     Because: genre match (+15)
  4. Sunrise City by Neon Echo - Score: 0.00
     Because: 
  5. Storm Runner by Voltline - Score: 0.00
     Because: 
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.
========================= test session starts =========================
platform win32 -- Python 3.13.0, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Development\AI110\Projects\ai110-module3show-musicrecommendersimulation-starter
plugins: anyio-4.15.1, platformdirs-4.13.0, cov-7.1.0
collected 9 items                                                      

tests\test_recommender.py .........                              [100%]

========================== 9 passed in 0.16s ==========================

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

Loading songs from data/songs.csv...
Loaded songs: 20

User profile: genre=pop, mood=happy, energy=0.8, tempo_bpm=120, valence=0.8, danceability=0.8, acousticness=0.2
Recommendations:
  1. Sunrise City by Neon Echo - Score: 98.74
     Because: genre match (+25); mood match (+20); energy close to target (+14.7); valence close to target (+14.4); tempo_bpm close to target (+9.8); danceability close to target (+9.9); acousticness close to target (+4.9)
  2. Gym Hero by Max Pulse - Score: 75.07
     Because: genre match (+25); energy close to target (+13.1); valence close to target (+14.5); tempo_bpm close to target (+9.0); danceability close to target (+9.2); acousticness close to target (+4.2)
  3. Rooftop Lights by Indigo Parade - Score: 72.97
     Because: mood match (+20); energy close to target (+14.4); valence close to target (+14.8); tempo_bpm close to target (+9.7); danceability close to target(+9.8); acousticness close to target (+4.2)
  4. Runway Lights by Avery Lane - Score: 52.29
     Because: energy close to target (+14.3); valence close to target (+14.7); tempo_bpm close to target (+9.8); danceability close to target (+8.9); acousticness close to target (+4.6)
  5. Island Motion by Coral Beat - Score: 49.33
     Because: energy close to target (+13.5); valence close to target (+13.8); tempo_bpm close to target (+8.0); danceability close to target (+9.6); acousticness close to target (+4.4)
```
 #### Added profiles and with Adversarial profiles
```
Loading songs from data/songs.csv...
Loaded songs: 20

=== High-Energy Pop ===
User profile: genre=pop, mood=happy, energy=0.85, tempo_bpm=125, valence=0.8, danceability=0.85, acousticness=0.1
Recommendations:
  1. Sunrise City by Neon Echo - Score: 97.38
     Because: genre match (+25); mood match (+20); energy close to target (+14.5); valence close to target (+14.4); tempo_bpm close to target (+9.4); danceability close to target (+9.4); acousticness close to target (+4.6)
  2. Gym Hero by Max Pulse - Score: 77.23
     Because: genre match (+25); energy close to target (+13.8); valence close to target (+14.5); tempo_bpm close to target (+9.4); danceability close to target (+9.7); acousticness close to target (+4.8)
  3. Rooftop Lights by Indigo Parade - Score: 71.87
     Because: mood match (+20); energy close to target (+13.7); valence close to target (+14.8); tempo_bpm close to target (+9.9); danceability close to target(+9.7); acousticness close to target (+3.8)
  4. Runway Lights by Avery Lane - Score: 53.75
     Because: energy close to target (+15.0); valence close to target (+14.7); tempo_bpm close to target (+9.8); danceability close to target (+9.4); acousticness close to target (+4.9)
  5. Neon Mirage by Pixel Mirage - Score: 48.85
     Because: energy close to target (+14.4); valence close to target (+9.9); tempo_bpm close to target (+9.8); danceability close to target (+9.9); acousticness close to target (+4.9)

=== Chill Lofi ===
User profile: genre=lofi, mood=chill, energy=0.38, tempo_bpm=76, valence=0.58, danceability=0.6, acousticness=0.8
Recommendations:
  1. Library Rain by Paper Lanterns - Score: 98.42
     Because: genre match (+25); mood match (+20); energy close to target (+14.5); valence close to target (+14.7); tempo_bpm close to target (+9.7); danceability close to target (+9.8); acousticness close to target (+4.7)
  2. Midnight Coding by LoRoom - Score: 98.29
     Because: genre match (+25); mood match (+20); energy close to target (+14.4); valence close to target (+14.7); tempo_bpm close to target (+9.8); danceability close to target (+9.8); acousticness close to target (+4.5)
  3. Focus Flow by LoRoom - Score: 79.12
     Because: genre match (+25); energy close to target (+14.7); valence close to target (+14.8); tempo_bpm close to target (+9.7); danceability close to target (+10.0); acousticness close to target (+4.9)
  4. Spacewalk Thoughts by Orbit Bloom - Score: 68.64
     Because: mood match (+20); energy close to target (+13.5); valence close to target (+13.9); tempo_bpm close to target (+8.7); danceability close to target(+8.1); acousticness close to target (+4.4)
  5. Desert Postcard by Sage & Sand - Score: 51.24
     Because: energy close to target (+14.2); valence close to target (+14.8); tempo_bpm close to target (+9.3); danceability close to target (+8.5); acousticness close to target (+4.3)

=== Deep Intense Rock ===
User profile: genre=rock, mood=intense, energy=0.92, tempo_bpm=150, valence=0.4, danceability=0.6, acousticness=0.08
Recommendations:
  1. Storm Runner by Voltline - Score: 97.79
     Because: genre match (+25); mood match (+20); energy close to target (+14.8); valence close to target (+13.8); tempo_bpm close to target (+9.8); danceability close to target (+9.4); acousticness close to target (+4.9)
  2. Gym Hero by Max Pulse - Score: 64.87
     Because: mood match (+20); energy close to target (+14.8); valence close to target (+9.4); tempo_bpm close to target (+8.5); danceability close to target (+7.2); acousticness close to target (+4.8)
  3. Iron Pulse by Black Anvil - Score: 50.57
     Because: energy close to target (+14.3); valence close to target (+14.2); tempo_bpm close to target (+8.5); danceability close to target (+8.8); acousticness close to target (+4.8)
  4. Neon Mirage by Pixel Mirage - Score: 48.05
     Because: energy close to target (+13.3); valence close to target (+14.1); tempo_bpm close to target (+8.2); danceability close to target (+7.4); acousticness close to target (+5.0)
  5. Night Drive Loop by Neon Echo - Score: 45.82
     Because: energy close to target (+12.4); valence close to target (+13.7); tempo_bpm close to target (+6.7); danceability close to target (+8.7); acousticness close to target (+4.3)

=== Sad but Hype (mood not in catalog) ===
User profile: mood=sad, energy=0.9, tempo_bpm=150, valence=0.2
Recommendations:
  1. Storm Runner by Voltline - Score: 35.49
     Because: energy close to target (+14.8); valence close to target (+10.8); tempo_bpm close to target (+9.8)
  2. Iron Pulse by Black Anvil - Score: 35.22
     Because: energy close to target (+14.0); valence close to target (+12.8); tempo_bpm close to target (+8.5)
  3. Neon Mirage by Pixel Mirage - Score: 32.95
     Because: energy close to target (+13.7); valence close to target (+11.1); tempo_bpm close to target (+8.2)
  4. Night Drive Loop by Neon Echo - Score: 30.12
     Because: energy close to target (+12.8); valence close to target (+10.6); tempo_bpm close to target (+6.7)
  5. Gym Hero by Max Pulse - Score: 29.52
     Because: energy close to target (+14.5); valence close to target (+6.4); tempo_bpm close to target (+8.5)

=== Labels vs Numbers (pop/intense but quiet) ===
User profile: genre=pop, mood=intense, energy=0.1, tempo_bpm=60, valence=0.2, danceability=0.2, acousticness=0.95
Recommendations:
  1. Gym Hero by Max Pulse - Score: 61.80
     Because: genre match (+25); mood match (+20); energy close to target (+2.5); valence close to target (+6.4); tempo_bpm close to target (+4.1); danceability close to target (+3.2); acousticness close to target (+0.5)
  2. Quiet Snowfall by Eira North - Score: 46.71
     Because: energy close to target (+14.1); valence close to target (+8.6); tempo_bpm close to target (+9.5); danceability close to target (+9.8); acousticness close to target (+4.8)
  3. Velvet Waltz by Mira Sol - Score: 46.29
     Because: energy close to target (+12.9); valence close to target (+10.2); tempo_bpm close to target (+9.3); danceability close to target (+9.0); acousticness close to target (+4.8)
  4. Sunrise City by Neon Echo - Score: 45.10
     Because: genre match (+25); energy close to target (+4.2); valence close to target (+5.4); tempo_bpm close to target (+5.2); danceability close to target (+4.1); acousticness close to target (+1.1)
  5. Spacewalk Thoughts by Orbit Bloom - Score: 43.30
     Because: energy close to target (+12.3); valence close to target (+8.2); tempo_bpm close to target (+10.0); danceability close to target (+7.9); acousticness close to target (+4.9)

=== Near-Miss Genre (indie pop described as pop) ===
User profile: genre=pop, mood=happy, energy=0.76, tempo_bpm=124, valence=0.81, danceability=0.82, acousticness=0.35
Recommendations:
  1. Sunrise City by Neon Echo - Score: 97.01
     Because: genre match (+25); mood match (+20); energy close to target (+14.1); valence close to target (+14.6); tempo_bpm close to target (+9.5); danceability close to target (+9.7); acousticness close to target (+4.2)
  2. Rooftop Lights by Indigo Parade - Score: 75.00
     Because: mood match (+20); energy close to target (+15.0); valence close to target (+15.0); tempo_bpm close to target (+10.0); danceability close to target (+10.0); acousticness close to target (+5.0)
  3. Gym Hero by Max Pulse - Score: 74.09
     Because: genre match (+25); energy close to target (+12.4); valence close to target (+14.4); tempo_bpm close to target (+9.3); danceability close to target (+9.4); acousticness close to target (+3.5)
  4. Runway Lights by Avery Lane - Score: 51.29
     Because: energy close to target (+13.7); valence close to target (+14.9); tempo_bpm close to target (+9.8); danceability close to target (+9.1); acousticness close to target (+3.9)
  5. Island Motion by Coral Beat - Score: 50.40
     Because: energy close to target (+14.1); valence close to target (+14.0); tempo_bpm close to target (+7.7); danceability close to target (+9.8); acousticness close to target (+4.8)

=== Ghost Genre (k-pop not in catalog) ===
User profile: genre=k-pop, mood=happy, energy=0.8
Recommendations:
  1. Sunrise City by Neon Echo - Score: 34.70
     Because: mood match (+20); energy close to target (+14.7)
  2. Rooftop Lights by Indigo Parade - Score: 34.40
     Because: mood match (+20); energy close to target (+14.4)
  3. Neon Mirage by Pixel Mirage - Score: 14.85
     Because: energy close to target (+14.8)
  4. Runway Lights by Avery Lane - Score: 14.25
     Because: energy close to target (+14.3)
  5. Night Drive Loop by Neon Echo - Score: 14.25
     Because: energy close to target (+14.2)

=== Whitespace in Labels ===
User profile: genre= Lofi, mood=chill 
Recommendations:
  1. Sunrise City by Neon Echo - Score: 0.00
     Because: 
  2. Midnight Coding by LoRoom - Score: 0.00
     Because: 
  3. Storm Runner by Voltline - Score: 0.00
     Because: 
  4. Library Rain by Paper Lanterns - Score: 0.00
     Because: 
  5. Gym Hero by Max Pulse - Score: 0.00
     Because: 

=== Out-of-Range Values ===
User profile: energy=2.0, valence=-1.0
Recommendations:
  1. Sunrise City by Neon Echo - Score: 0.00
     Because: 
  2. Midnight Coding by LoRoom - Score: 0.00
     Because: 
  3. Storm Runner by Voltline - Score: 0.00
     Because: 
  4. Library Rain by Paper Lanterns - Score: 0.00
     Because: 
  5. Gym Hero by Max Pulse - Score: 0.00
     Because: 

=== Genre Only (ties) ===
User profile: genre=lofi
Recommendations:
  1. Midnight Coding by LoRoom - Score: 25.00
     Because: genre match (+25)
  2. Library Rain by Paper Lanterns - Score: 25.00
     Because: genre match (+25)
  3. Focus Flow by LoRoom - Score: 25.00
     Because: genre match (+25)
  4. Sunrise City by Neon Echo - Score: 0.00
     Because: 
  5. Storm Runner by Voltline - Score: 0.00
     Because: 

```
#### Rebalanced weight
```
Loading songs from data/songs.csv...
Loaded songs: 20

=== High-Energy Pop ===
User profile: genre=pop, mood=happy, energy=0.85, tempo_bpm=125, valence=0.8, danceability=0.85, acousticness=0.1
Recommendations:
  1. Sunrise City by Neon Echo - Score: 96.63
     Because: genre match (+15); mood match (+15); energy close to target (+19.4); valence close to target (+19.2); tempo_bpm close to target (+9.4); danceability close to target (+9.4); acousticness close to target (+9.2)
  2. Gym Hero by Max Pulse - Score: 81.43
     Because: genre match (+15); energy close to target (+18.4); valence close to target (+19.4); tempo_bpm close to target (+9.4); danceability close to target (+9.7); acousticness close to target (+9.5)
  3. Rooftop Lights by Indigo Parade - Score: 80.12
     Because: mood match (+15); energy close to target (+18.2); valence close to target (+19.8); tempo_bpm close to target (+9.9); danceability close to target(+9.7); acousticness close to target (+7.5)
  4. Runway Lights by Avery Lane - Score: 68.55
     Because: energy close to target (+20.0); valence close to target (+19.6); tempo_bpm close to target (+9.8); danceability close to target (+9.4); acousticness close to target (+9.8)
  5. Neon Mirage by Pixel Mirage - Score: 61.85
     Because: energy close to target (+19.2); valence close to target (+13.2); tempo_bpm close to target (+9.8); danceability close to target (+9.9); acousticness close to target (+9.8)

=== Chill Lofi ===
User profile: genre=lofi, mood=chill, energy=0.38, tempo_bpm=76, valence=0.58, danceability=0.6, acousticness=0.8
Recommendations:
  1. Library Rain by Paper Lanterns - Score: 97.87
     Because: genre match (+15); mood match (+15); energy close to target (+19.4); valence close to target (+19.6); tempo_bpm close to target (+9.7); danceability close to target (+9.8); acousticness close to target (+9.4)
  2. Midnight Coding by LoRoom - Score: 97.54
     Because: genre match (+15); mood match (+15); energy close to target (+19.2); valence close to target (+19.6); tempo_bpm close to target (+9.8); danceability close to target (+9.8); acousticness close to target (+9.1)
  3. Focus Flow by LoRoom - Score: 83.87
     Because: genre match (+15); energy close to target (+19.6); valence close to target (+19.8); tempo_bpm close to target (+9.7); danceability close to target (+10.0); acousticness close to target (+9.8)
  4. Spacewalk Thoughts by Orbit Bloom - Score: 77.19
     Because: mood match (+15); energy close to target (+18.0); valence close to target (+18.6); tempo_bpm close to target (+8.7); danceability close to target(+8.1); acousticness close to target (+8.8)
  5. Desert Postcard by Sage & Sand - Score: 65.24
     Because: energy close to target (+19.0); valence close to target (+19.8); tempo_bpm close to target (+9.3); danceability close to target (+8.5); acousticness close to target (+8.6)

=== Deep Intense Rock ===
User profile: genre=rock, mood=intense, energy=0.92, tempo_bpm=150, valence=0.4, danceability=0.6, acousticness=0.08
Recommendations:
  1. Storm Runner by Voltline - Score: 97.24
     Because: genre match (+15); mood match (+15); energy close to target (+19.8); valence close to target (+18.4); tempo_bpm close to target (+9.8); danceability close to target (+9.4); acousticness close to target (+9.8)
  2. Gym Hero by Max Pulse - Score: 72.82
     Because: mood match (+15); energy close to target (+19.8); valence close to target (+12.6); tempo_bpm close to target (+8.5); danceability close to target(+7.2); acousticness close to target (+9.7)
  3. Iron Pulse by Black Anvil - Score: 64.82
     Because: energy close to target (+19.0); valence close to target (+19.0); tempo_bpm close to target (+8.5); danceability close to target (+8.8); acousticness close to target (+9.5)
  4. Neon Mirage by Pixel Mirage - Score: 62.20
     Because: energy close to target (+17.8); valence close to target (+18.8); tempo_bpm close to target (+8.2); danceability close to target (+7.4); acousticness close to target (+10.0)
  5. Night Drive Loop by Neon Echo - Score: 58.82
     Because: energy close to target (+16.6); valence close to target (+18.2); tempo_bpm close to target (+6.7); danceability close to target (+8.7); acousticness close to target (+8.6)

=== Sad but Hype (mood not in catalog) ===
User profile: mood=sad, energy=0.9, tempo_bpm=150, valence=0.2
Recommendations:
  1. Iron Pulse by Black Anvil - Score: 44.12
     Because: energy close to target (+18.6); valence close to target (+17.0); tempo_bpm close to target (+8.5)
  2. Storm Runner by Voltline - Score: 44.04
     Because: energy close to target (+19.8); valence close to target (+14.4); tempo_bpm close to target (+9.8)
  3. Neon Mirage by Pixel Mirage - Score: 41.20
     Because: energy close to target (+18.2); valence close to target (+14.8); tempo_bpm close to target (+8.2)
  4. Night Drive Loop by Neon Echo - Score: 37.92
     Because: energy close to target (+17.0); valence close to target (+14.2); tempo_bpm close to target (+6.7)
  5. Gym Hero by Max Pulse - Score: 36.52
     Because: energy close to target (+19.4); valence close to target (+8.6); tempo_bpm close to target (+8.5)

=== Labels vs Numbers (pop/intense but quiet) ===
User profile: genre=pop, mood=intense, energy=0.1, tempo_bpm=60, valence=0.2, danceability=0.2, acousticness=0.95
Recommendations:
  1. Quiet Snowfall by Eira North - Score: 59.01
     Because: energy close to target (+18.8); valence close to target (+11.4); tempo_bpm close to target (+9.5); danceability close to target (+9.8); acousticness close to target (+9.5)
  2. Velvet Waltz by Mira Sol - Score: 58.84
     Because: energy close to target (+17.2); valence close to target (+13.6); tempo_bpm close to target (+9.3); danceability close to target (+9.0); acousticness close to target (+9.7)
  3. Spacewalk Thoughts by Orbit Bloom - Score: 55.00
     Because: energy close to target (+16.4); valence close to target (+11.0); tempo_bpm close to target (+10.0); danceability close to target (+7.9); acousticness close to target (+9.7)
  4. Blue Hour by June Harbor - Score: 54.19
     Because: energy close to target (+13.4); valence close to target (+17.8); tempo_bpm close to target (+8.7); danceability close to target (+7.1); acousticness close to target (+7.2)
  5. Desert Postcard by Sage & Sand - Score: 53.43
     Because: energy close to target (+15.4); valence close to target (+12.6); tempo_bpm close to target (+8.0); danceability close to target (+7.5); acousticness close to target (+9.9)

=== Near-Miss Genre (indie pop described as pop) ===
User profile: genre=pop, mood=happy, energy=0.76, tempo_bpm=124, valence=0.81, danceability=0.82, acousticness=0.35
Recommendations:
  1. Sunrise City by Neon Echo - Score: 95.71
     Because: genre match (+15); mood match (+15); energy close to target (+18.8); valence close to target (+19.4); tempo_bpm close to target (+9.5); danceability close to target (+9.7); acousticness close to target (+8.3)
  2. Rooftop Lights by Indigo Parade - Score: 85.00
     Because: mood match (+15); energy close to target (+20.0); valence close to target (+20.0); tempo_bpm close to target (+10.0); danceability close to target (+10.0); acousticness close to target (+10.0)
  3. Gym Hero by Max Pulse - Score: 76.54
     Because: genre match (+15); energy close to target (+16.6); valence close to target (+19.2); tempo_bpm close to target (+9.3); danceability close to target (+9.4); acousticness close to target (+7.0)
  4. Runway Lights by Avery Lane - Score: 64.64
     Because: energy close to target (+18.2); valence close to target (+19.8); tempo_bpm close to target (+9.8); danceability close to target (+9.1); acousticness close to target (+7.7)
  5. Island Motion by Coral Beat - Score: 64.60
     Because: energy close to target (+18.8); valence close to target (+18.6); tempo_bpm close to target (+7.7); danceability close to target (+9.8); acousticness close to target (+9.7)

=== Ghost Genre (k-pop not in catalog) ===
User profile: genre=k-pop, mood=happy, energy=0.8
Recommendations:
  1. Sunrise City by Neon Echo - Score: 34.60
     Because: mood match (+15); energy close to target (+19.6)
  2. Rooftop Lights by Indigo Parade - Score: 34.20
     Because: mood match (+15); energy close to target (+19.2)
  3. Neon Mirage by Pixel Mirage - Score: 19.80
     Because: energy close to target (+19.8)
  4. Night Drive Loop by Neon Echo - Score: 19.00
     Because: energy close to target (+19.0)
  5. Runway Lights by Avery Lane - Score: 19.00
     Because: energy close to target (+19.0)

=== Whitespace in Labels ===
User profile: genre= Lofi, mood=chill 
Recommendations:
  1. Sunrise City by Neon Echo - Score: 0.00
     Because: 
  2. Midnight Coding by LoRoom - Score: 0.00
     Because: 
  3. Storm Runner by Voltline - Score: 0.00
     Because: 
  4. Library Rain by Paper Lanterns - Score: 0.00
     Because: 
  5. Gym Hero by Max Pulse - Score: 0.00
     Because: 

=== Out-of-Range Values ===
User profile: energy=2.0, valence=-1.0
Recommendations:
  1. Sunrise City by Neon Echo - Score: 0.00
     Because: 
  2. Midnight Coding by LoRoom - Score: 0.00
     Because: 
  3. Storm Runner by Voltline - Score: 0.00
     Because: 
  4. Library Rain by Paper Lanterns - Score: 0.00
     Because: 
  5. Gym Hero by Max Pulse - Score: 0.00
     Because: 

=== Genre Only (ties) ===
User profile: genre=lofi
Recommendations:
  1. Midnight Coding by LoRoom - Score: 15.00
     Because: genre match (+15)
  2. Library Rain by Paper Lanterns - Score: 15.00
     Because: genre match (+15)
  3. Focus Flow by LoRoom - Score: 15.00
     Because: genre match (+15)
  4. Sunrise City by Neon Echo - Score: 0.00
     Because: 
  5. Storm Runner by Voltline - Score: 0.00
     Because: 
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5

**Experiment 1: Lowering the genre weight.** My scoring uses points instead of multipliers, so my version of this experiment was lowering genre from 25 points to 15. I then also lowered mood from 20 to 15 and moved the freed-up points to energy (15 → 20), valence (15 → 20), and acousticness (5 → 10).

| Profile | Original (genre 25, mood 20) | Genre 15 only | Final (genre 15, mood 15) |
|---|---|---|---|
| High-Energy Pop | Sunrise City 97.4 · Gym Hero 77.2 · Rooftop Lights 71.9 | Sunrise City 87.4 · Rooftop Lights 71.9 · Gym Hero 67.2 | Sunrise City 96.6 · Gym Hero 81.4 · Rooftop Lights 80.1 |
| Labels vs Numbers (asks for pop/intense, describes quiet acoustic music) | **Gym Hero 61.8** · Quiet Snowfall 46.7 | **Gym Hero 51.8** · Quiet Snowfall 46.7 | **Quiet Snowfall 59.0** · Velvet Waltz 58.8 |
| Near-Miss Genre (describes Rooftop Lights, but says "pop") | Sunrise City 97.0 · Rooftop Lights 75.0 · Gym Hero 74.1 | Sunrise City 87.0 · Rooftop Lights 75.0 · Gym Hero 64.1 | Sunrise City 95.7 · Rooftop Lights 85.0 · Gym Hero 76.5 |
| Chill Lofi / Deep Intense Rock | Same top 3 in every version | | |

**What happened:**
- With the original weights, genre and mood together were worth 45 points. That was enough for *Gym Hero*, a loud pop gym song, to be the #1 pick for a listener who described quiet, acoustic music.
- Lowering only genre to 15 was **not enough** to fix this, because genre and mood together were still worth 35 points. *Gym Hero* stayed at #1.
- The fix came from lowering mood as well and moving the points to the sound features. After that, the quiet, acoustic songs won.
- Lowering genre also widened the Near-Miss gap. *Rooftop Lights* had been only 0.9 points ahead of *Gym Hero*; after the change it was 10.9 points ahead in the "genre 15 only" version and 8.5 in the final version.
- The normal profiles (Chill Lofi, Deep Intense Rock, and Sunrise City at #1 for pop) did not change. This shows the rebalance fixed the edge cases without breaking the cases that already worked.

**Conclusion:** the genre weight was too strong, but the real problem was how much the labels counted in total compared with the sound features. I kept the final weights.

- What happened when you added tempo or valence to the score

**Experiment 2: Adding tempo and valence.** I scored each profile four ways: without tempo or valence, with only tempo added, with only valence added, and with both (my final version). Genre, mood, energy, danceability, and acousticness were always included.

| Profile | Neither | + Tempo only | + Valence only | Both (final) |
|---|---|---|---|---|
| High-Energy Pop (#4–5) | Runway Lights · Neon Mirage | Runway Lights · Neon Mirage | Runway Lights · **Salsa de Sol** | Runway Lights · Neon Mirage |
| Chill Lofi (#5) | Coffee Shop Stories | Coffee Shop Stories | **Desert Postcard** | Desert Postcard |
| Deep Intense Rock (#5) | **Sunrise City** | Runway Lights | **Night Drive Loop** | Night Drive Loop |
| Sad but Hype (top 3) | Storm Runner · **Salsa de Sol** · Gym Hero | Storm Runner · Gym Hero · Salsa de Sol | **Iron Pulse** · Storm Runner · Neon Mirage | Iron Pulse · Storm Runner · Neon Mirage |

**What happened:**
- **The top 3 for the normal profiles never changed.** High-Energy Pop, Chill Lofi, and Deep Intense Rock kept the same top three in all four versions. Genre, mood, and energy already pick the obvious winners, so tempo and valence mainly change the lower spots.
- **Tempo added very little.** Adding tempo raised almost every score by about 10 points but barely changed the order. This is because tempo mostly repeats what energy already measures: fast songs in this catalog are also high-energy songs.
- **Valence made the biggest difference, especially for "sad" listeners.** Without valence, the Sad but Hype listener got *Salsa de Sol* at #2 and *Gym Hero* at #3, two of the most cheerful songs in the catalog. Since no song is labeled "sad," energy was the only thing being scored. Adding valence pushed the cheerful songs out and brought in darker ones like *Iron Pulse*, *Neon Mirage*, and *Night Drive Loop*. Valence is the only way this listener's sadness gets counted at all.
- **Valence also cleaned up the rock list.** Without it, the happy pop song *Sunrise City* showed up at #5 for the rock fan. Valence replaced it with the moodier *Night Drive Loop*.
- **Tempo and valence sometimes pull in different directions.** For the pop fan, valence alone brought in *Salsa de Sol* (very cheerful), but adding tempo pushed it back out because its tempo (176 BPM) is far from the listener's 125. With both features, *Neon Mirage* returned at #5.

**Conclusion:** valence is worth keeping. It is the feature that tells "happy loud" apart from "dark loud," and it makes up for the missing "sad" mood. Tempo is less useful on its own because it overlaps with energy, but it helps filter out songs that are way too fast or too slow.

- How did your system behave for different types of users

**Experiment 3: Testing different types of users.** I ran 10 profiles through the final version: 3 typical listeners and 7 tricky ones designed to confuse the scoring. I also scored 2,000 randomly generated listeners to see who gets good results and who doesn't.

| Type of user | Profile | #1 pick (score) | Verdict |
|---|---|---|---|
| Typical | High-Energy Pop | Sunrise City (96.6) | Good match |
| Typical | Chill Lofi | Library Rain (97.9) | Good match |
| Typical | Deep Intense Rock | Storm Runner (97.2) | Good match |
| Conflicting preferences | Labels vs Numbers (says pop/intense, describes quiet acoustic music) | Quiet Snowfall (59.0) | Reasonable: the sound wins over the labels |
| Conflicting preferences | Sad but Hype (sad mood, high energy) | Iron Pulse (44.1) | Reasonable pick, but a low score |
| Label not in catalog | Ghost Genre (k-pop) | Sunrise City (34.6) | Genre silently ignored |
| Label worded differently | Near-Miss Genre (says "pop," describes indie pop) | Sunrise City (95.7) | Perfect sound match *Rooftop Lights* only #2 |
| Very little info | Genre Only (lofi) | Midnight Coding (15.0) | Three-way tie, order decided by file position |
| Broken input | Whitespace in Labels / Out-of-Range Values | Sunrise City (0.0) | Invalid: every song scores 0, no warning |

**What happened:**
- **Typical listeners were served very well.** When genre, mood, and sound all point the same way, the #1 pick scores about 97 and is the song a person would choose by hand. Very different listeners also get very different lists: the pop and lofi fans share no songs at all.
- **Listeners with conflicting preferences got sensible but weaker results.** After rebalancing the weights, the described sound wins over the labels, which I think is the right call. But Sad but Hype's best song only scores 44, because no song is labeled "sad."
- **Listeners whose words don't match the catalog lose out without being told.** "K-pop" earns nothing, and "pop" doesn't count for "indie pop." The system still returns five songs, so the listener has no idea part of their request was ignored.
- **Broken input gives meaningless results.** Extra spaces or impossible numbers make every song score zero, and the system just shows the first five songs in the file. Text where a number is expected crashes the program.
- **Across 2,000 random listeners, "sad" listeners got the worst results.** Their #1 pick averaged 64.4 points, compared with about 69 for everyone else, because only 2 songs in the catalog sound truly gloomy. Average-sounding songs were also recommended much more often: *Blue Hour* appeared in 42% of top-five lists, but *Salsa de Sol* in only 10%.

**Conclusion:** the system works well for listeners who want what the catalog has plenty of and use its exact labels. It works worst for listeners with uncommon tastes, sad moods, or slightly different wording, and it never tells them when it can't help. See the "Evaluation" and "Limitations and Bias" sections of [model_card.md](model_card.md) for profile-by-profile comparisons.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

- **Tiny, uneven catalog.** There are only 20 songs. Lofi has 3 and pop has 2, but every other genre has just one, so fans of metal, jazz, or salsa get at most one real genre match.
- **Missing music and moods.** There is no hip-hop, R&B, K-pop, or Latin pop, and no "sad" mood. Only 2 songs sound truly gloomy, so listeners who like sad music get the weakest results.
- **Exact-word matching.** "Indie pop" gets no credit for "pop," and "melancholic" gets none for "sad." Extra spaces in a label also break the match.
- **No lyrics, language, or context.** The system only knows how a song sounds and how it's labeled. It can't handle requests like "instrumental only," "songs in Spanish," or "music for studying."
- **Average songs get recommended too often.** Songs in the middle of the range score decently for almost everyone. In a test with 2,000 random listeners, *Blue Hour* appeared in 42% of top-five lists, while the very fast, very cheerful *Salsa de Sol* appeared in only 10%.
- **One taste per listener, no variety.** Each preference is a single number, so someone who likes both calm and loud music can't be described. The top five are just the closest matches, so they often sound alike or include the same artist twice.
- **Fails silently.** If a preference can't be matched, or the input has a typo or an impossible value, the system still shows five songs without any warning. Ties always go to the song listed first in the file, and text where a number is expected crashes the program.

**Risk:** in a real app, these problems would quietly give worse recommendations to people with less common tastes, while making it look like the system worked fine.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this

Building this project showed me that a recommender doesn't really "understand" music. It turns each song into a handful of numbers and labels, compares them to the numbers and labels a user gave, and adds up points for how close they are. The "prediction" is just the songs with the highest totals. That means the results depend entirely on two things a person decides: which features get measured, and how much each one is worth. When I gave genre and mood 45 of the 100 points, a loud gym song won for someone who described quiet, acoustic music, just because its labels matched. After I moved those points to energy, valence, and acousticness, the same listener got calm, acoustic songs. The data stayed the same, but changing a few weights completely changed what the system "thought" the user wanted.

I also learned that bias can come in quietly, without anyone meaning to be unfair. Some of it comes from the data: the catalog has three lofi songs but only one metal song, and no song labeled "sad," so those listeners get weaker results no matter how good the scoring is. Some of it comes from the design: exact-word matching ignores "indie pop" when someone asks for "pop," and the way points are taken away makes average-sounding songs show up far more often than distinctive ones. The most worrying part is that the system never says when it is struggling. It still returns five songs with confident-looking scores, so a listener with uncommon taste would just get worse recommendations without ever knowing why. In a real app with millions of users, the same kinds of choices could decide which artists get heard and which listeners get left out.



