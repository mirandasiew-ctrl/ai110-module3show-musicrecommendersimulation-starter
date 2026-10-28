"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs

# Test profiles covering different corners of the catalog
USER_PROFILES = {
    "High-Energy Pop": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.85,
        "tempo_bpm": 125,
        "valence": 0.8,
        "danceability": 0.85,
        "acousticness": 0.1,
    },
    "Chill Lofi": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.38,
        "tempo_bpm": 76,
        "valence": 0.58,
        "danceability": 0.6,
        "acousticness": 0.8,
    },
    "Deep Intense Rock": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.92,
        "tempo_bpm": 150,
        "valence": 0.4,
        "danceability": 0.6,
        "acousticness": 0.08,
    },
    # Adversarial profiles designed to trick or expose weaknesses in the scoring
    "Sad but Hype (mood not in catalog)": {
        "mood": "sad",
        "energy": 0.9,
        "tempo_bpm": 150,
        "valence": 0.2,
    },
    "Labels vs Numbers (pop/intense but quiet)": {
        "genre": "pop",
        "mood": "intense",
        "energy": 0.1,
        "tempo_bpm": 60,
        "valence": 0.2,
        "danceability": 0.2,
        "acousticness": 0.95,
    },
    "Near-Miss Genre (indie pop described as pop)": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.76,
        "tempo_bpm": 124,
        "valence": 0.81,
        "danceability": 0.82,
        "acousticness": 0.35,
    },
    "Ghost Genre (k-pop not in catalog)": {
        "genre": "k-pop",
        "mood": "happy",
        "energy": 0.8,
    },
    "Whitespace in Labels": {
        "genre": " Lofi",
        "mood": "chill ",
    },
    "Out-of-Range Values": {
        "energy": 2.0,
        "valence": -1.0,
    },
    "Genre Only (ties)": {
        "genre": "lofi",
    },
}


def main() -> None:
    songs = load_songs("data/songs.csv")

    for name, user_prefs in USER_PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)

        profile = ", ".join(f"{key}={value}" for key, value in user_prefs.items())
        print(f"\n=== {name} ===")
        print(f"User profile: {profile}")
        print("Recommendations:")
        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"  {rank}. {song['title']} by {song['artist']} - Score: {score:.2f}")
            print(f"     Because: {explanation}")


if __name__ == "__main__":
    main()
