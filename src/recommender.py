import csv
from typing import List, Dict, Tuple, Optional

# Scoring weights from the Algorithm Recipe in README.md (max total = 100)
GENRE_POINTS = 25
MOOD_POINTS = 20
NUMERIC_WEIGHTS = {
    "energy": 15,
    "valence": 15,
    "tempo_bpm": 10,
    "danceability": 10,
    "acousticness": 5,
}
TEMPO_RANGE = 122  # catalog BPM range (54-176), used to scale tempo to 0-1
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into dicts with numeric fields converted to int/float."""
    print(f"Loading songs from {csv_path}...")
    float_fields = ["energy", "tempo_bpm", "valence", "danceability", "acousticness"]
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song against user preferences (0-100) and return (score, reasons)."""
    score = 0.0
    reasons = []

    # Categorical features: all-or-nothing match (case-insensitive)
    if "genre" in user_prefs and song["genre"].lower() == user_prefs["genre"].lower():
        score += GENRE_POINTS
        reasons.append(f"genre match (+{GENRE_POINTS})")
    if "mood" in user_prefs and song["mood"].lower() == user_prefs["mood"].lower():
        score += MOOD_POINTS
        reasons.append(f"mood match (+{MOOD_POINTS})")

    # Numeric features: closer to the target earns more points.
    # Preferences the user didn't provide are skipped.
    for feature, weight in NUMERIC_WEIGHTS.items():
        if feature not in user_prefs:
            continue
        diff = abs(song[feature] - user_prefs[feature])
        if feature == "tempo_bpm":
            diff /= TEMPO_RANGE
        points = max(0.0, 1 - diff) * weight
        score += points
        if points > 0:
            reasons.append(f"{feature} close to target (+{points:.1f})")

    return score, reasons

def recommend_songs(
    user_prefs: Dict, songs: List[Dict], k: int = 5, exclude_id: Optional[int] = None
) -> List[Tuple[Dict, float, str]]:
    """Return the top k songs as (song, score, explanation), highest score first."""
    # Score every song once, skipping the song currently playing
    scored = [
        (song, *score_song(user_prefs, song))
        for song in songs
        if song["id"] != exclude_id
    ]

    # sorted() is stable, so tied songs keep their CSV order
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)

    return [(song, score, "; ".join(reasons)) for song, score, reasons in ranked[:k]]
