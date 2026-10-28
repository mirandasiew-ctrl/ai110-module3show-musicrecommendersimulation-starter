import pytest

from src.recommender import Song, UserProfile, Recommender, score_song, recommend_songs

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


# Edge cases for the functional API (score_song / recommend_songs).
# These document current behavior, including known weaknesses.

def make_song_dicts() -> list:
    return [
        {"id": 1, "title": "Pop Track", "artist": "A", "genre": "pop", "mood": "happy",
         "energy": 0.8, "tempo_bpm": 120, "valence": 0.9, "danceability": 0.8, "acousticness": 0.2},
        {"id": 2, "title": "Lofi Loop", "artist": "B", "genre": "lofi", "mood": "chill",
         "energy": 0.4, "tempo_bpm": 80, "valence": 0.6, "danceability": 0.5, "acousticness": 0.9},
        {"id": 3, "title": "Lofi Focus", "artist": "C", "genre": "lofi", "mood": "focused",
         "energy": 0.4, "tempo_bpm": 80, "valence": 0.6, "danceability": 0.5, "acousticness": 0.8},
    ]


def test_string_numeric_preference_raises_type_error():
    with pytest.raises(TypeError):
        recommend_songs({"energy": "0.9"}, make_song_dicts())


def test_none_genre_raises_attribute_error():
    with pytest.raises(AttributeError):
        recommend_songs({"genre": None}, make_song_dicts())


def test_empty_profile_scores_zero_and_keeps_csv_order():
    results = recommend_songs({}, make_song_dicts(), k=3)

    assert [score for _, score, _ in results] == [0, 0, 0]
    assert [song["id"] for song, _, _ in results] == [1, 2, 3]
    assert all(explanation == "" for _, _, explanation in results)


def test_whitespace_in_labels_prevents_match():
    score, reasons = score_song({"genre": " Lofi", "mood": "chill "}, make_song_dicts()[1])

    assert score == 0
    assert reasons == []


def test_out_of_range_values_clamp_to_zero():
    score, _ = score_song({"energy": 2.0, "valence": -1.0}, make_song_dicts()[0])

    assert score == 0


def test_genre_only_ties_keep_csv_order():
    results = recommend_songs({"genre": "lofi"}, make_song_dicts(), k=2)

    assert [score for _, score, _ in results] == [15, 15]
    assert [song["id"] for song, _, _ in results] == [2, 3]


def test_negative_k_returns_all_but_last():
    # Known bug: ranked[:-1] slices off the last song instead of returning nothing
    results = recommend_songs({}, make_song_dicts(), k=-1)

    assert len(results) == 2
