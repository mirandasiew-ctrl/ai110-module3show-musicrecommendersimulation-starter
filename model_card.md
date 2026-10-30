# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

VibeScore 1.0

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
VibeScore suggests the **top five songs** from a small 20-song catalog that best match what a listener says they like. Each suggestion comes with a score out of 100 and a short list of reasons, such as "genre match" or "energy close to target," so the listener can see why it was picked. If the listener is already playing a song, that song is left out so it isn't recommended back to them. The recommendations are based only on how the songs sound and how they are labeled (genre, mood, energy, tempo, cheerfulness, danceability, and acousticness). It does not use what other people listen to, play counts, or the listener's history.

- What assumptions does it make about the user 
VibeScore assumes a few things about every listener:
 **They know what they like and can describe it.** They can say what they want as numbers, such as an energy level of 0.8.
 **Their taste fits in one spot.** Each preference is a single target value, so a listener who enjoys both very calm and very loud music can't be described well.
 **Their taste doesn't change.** The system doesn't know about time of day, activity, or how the listener feels right now, unless they update their profile.
 **They use the catalog's exact words.** A listener who asks for "sad" or "k-pop" gets no credit for those words, because the catalog only knows its own labels. A small difference like "indie pop" vs. "pop" also counts as no match.
 **They want songs that sound alike.** The top five are simply the five closest matches, so the system assumes the listener wants more of the same rather than some variety or something new.

- Is this for real users or classroom exploration  
VibeScore is for **classroom exploration**, not real listeners. It is a simulation built to learn how recommender systems turn preferences into scores, and where those scores can go wrong. The catalog has only 20 made-up songs, the profiles are typed in by hand, and the program can crash or quietly return meaningless results when given unexpected input. It should not be used to make recommendations for real people. It is useful for testing ideas, such as changing weights or trying tricky user profiles, and seeing how the results change.

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

- **Genre (15 points) and mood (15 points):** a song gets all of these points if it matches what the user asked for, and none if it doesn't. There is no partial credit.
- **The other five (70 points total):** these are worth more the closer the song is to what the user wants. A song that is almost exactly as energetic as the user asked for gets nearly all of the energy points. A song that is much calmer gets only a few. Energy and cheerfulness are worth 20 points each, and tempo, danceability, and acousticness 10 each.

After every song has a score, the recommender lines them up from highest to lowest. It skips the song the user is already listening to and suggests the top five. Each suggestion comes with a short list of reasons, like "genre match (+15)" or "energy close to target (+19.6)," so the user can see why it was picked.

**Changes from the starter logic:** the starter code did not score songs at all. It just returned the first few songs in the file. The starter's user profile only had genre, mood, energy, and a yes/no "likes acoustic" setting. I added tempo, cheerfulness, and danceability. I also changed acoustic sound from a yes/no question to a sliding scale. At first I made genre and mood the biggest factors because they seemed like the clearest signals of taste. Testing showed that those labels could outweigh everything else. For example, a user who asked for pop but described quiet, acoustic music still got a loud pop song first. So I lowered genre and mood to 15 points each and gave more weight to energy and cheerfulness. I also added the reasons so every recommendation can be explained.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog 
20 songs 

- What genres or moods are represented  
17 genres and 16 moods. Lofi has the most songs (3), followed by pop (2). Every other genre has just one song: rock, metal, indie pop, electronic, synthwave, disco, salsa, reggae, country, folk, blues, jazz, classical, ambient, and new age. For moods, chill has 3 songs, happy and intense have 2 each, and the other 13 have one song each: relaxed, focused, moody, hopeful, romantic, playful, powerful, melancholic, mysterious, nostalgic, passionate, peaceful, and confident. There is no "sad" or "angry" mood, and only 2 songs sound truly gloomy.

- Did you add or remove data 
I added data.

- Are there parts of musical taste missing in the dataset  
Yes, quite a few:
  - **Missing genres:** there is no hip-hop, rap, R&B, K-pop, Afrobeats, Latin pop, punk, gospel, or soundtrack music. The genres that are included lean toward Western music.
  - **Missing sounds:** there are no songs with medium energy. Every song is either calm (0.43 or lower) or loud (0.64 or higher). There are also very few sad-sounding songs, so listeners who like gloomy or emotional music have little to choose from.
  - **Missing information about each song:** the catalog has no lyrics, language, vocals vs. instrumental, release year, song length, or popularity. Someone who only wants instrumental music, songs in Spanish, or music from the '90s can't express that.
  - **Too simple labels:** each song gets exactly one genre and one mood, but real songs often mix styles and feelings. Those labels were also picked by one person, so they reflect one person's opinion.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results 
VibeScore works best for listeners whose taste matches what the catalog has a lot of:
  - **Calm, acoustic listeners** like the Chill Lofi profile get *Library Rain*, *Midnight Coding*, and *Focus Flow*. All three are quiet, slow lofi songs that score in the 80s and 90s.
  - **Upbeat, happy pop listeners** like the High-Energy Pop profile get *Sunrise City* at #1 with a score of about 97, followed by other bright, danceable songs.
  - **Loud, intense listeners** like the Deep Intense Rock profile get *Storm Runner* at #1 with a score of about 97, followed by other high-energy songs such as *Iron Pulse* and *Neon Mirage*.
  - **Listeners whose labels and sound clearly agree,** for example someone who asks for "chill" and also describes slow, quiet music. When everything points the same way, the top pick is almost always a song a person would agree with.

In general, it gives reasonable results to listeners who use the catalog's exact genre and mood words, want either clearly calm or clearly energetic music, and like cheerful or neutral songs more than sad ones.

- Any patterns you think your scoring captures correctly 
  - **Energy separates calm music from loud music.** The High-Energy Pop and Chill Lofi listeners share no songs in their top five. A calm listener never gets a loud song pushed on them, and the reverse is also true.
  - **Cheerfulness separates different kinds of loud music.** The pop and rock listeners both want high energy, but the pop list fills with happy songs while the rock list moves toward darker ones like *Iron Pulse*. The scoring tells "party loud" apart from "angry loud."
  - **Closer is better, not bigger.** The score rewards songs that are near what the listener asked for, not songs with the most of something. A listener who wants low energy gets the calmest songs, not the loudest.
  - **The sound wins when the labels disagree with it.** After rebalancing the weights, a listener who asks for "pop" and "intense" but describes quiet, acoustic music gets quiet, acoustic songs. How a song actually sounds now counts for more than the words attached to it.
  - **Genre picks the group, and the numbers sort it.** For the lofi fan, all three lofi songs make the top three. The energy and acousticness scores then decide which one is the best fit.
  - **Every pick can be explained.** The reasons listed with each song match the features that actually earned the points, so it is easy to see why a song was recommended.
 
- Cases where the recommendations matched your intuition  
  - **Rock fan gets *Storm Runner*.** Before running the program, I guessed that a loud, fast, darker rock listener would get *Storm Runner*, and it came out #1 with a score of about 97. *Iron Pulse*, a metal song, showed up at #3, which also felt right, since metal is close to rock.
  - **Lofi fan gets *Library Rain*.** For someone who wants calm, slow, acoustic background music, *Library Rain* and *Midnight Coding* are exactly the songs I would have picked by hand, and they finished #1 and #2 with almost the same score.
  - **The "pop but quiet" listener gets peaceful songs.** Once I rebalanced the weights, the listener who asked for pop but described quiet, acoustic music got *Quiet Snowfall* and *Velvet Waltz*. Their words said "pop," but what they described was a calm, gentle song, and those picks fit that.
  - **The "sad but hype" listener gets *Iron Pulse*.** No song is labeled "sad," but a heavy, dark metal song that is also very loud is a good guess for someone who wants angry or sad energy. The system got there using only the energy and cheerfulness numbers.
  - **The pop fan's #4 pick is disco.** *Runway Lights* isn't pop, but it is upbeat, confident, and very danceable, so it is a natural next song for a happy pop listener.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

**Weakness: average-sounding songs get recommended far more than distinctive ones.** The recommender takes away points slowly as a song gets further from what the user wants, so a song that is only medium in energy, tempo, and cheerfulness still earns a decent score from almost everyone. When I tested 2,000 random user profiles, *Blue Hour* showed up in 42% of the top-five lists, while *Salsa de Sol*, the fastest and one of the most cheerful songs in the catalog, showed up in only 10%. This creates a filter bubble where listeners keep seeing the same middle-of-the-road songs, and songs with a strong, unusual sound only reach the few users whose tastes match them almost exactly. A fairer version would penalize big differences more sharply, or make sure the top five include some variety.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested 
I started with three "normal" listeners: a **High-Energy Pop** fan (happy, upbeat, danceable), a **Chill Lofi** fan (calm, slow, acoustic), and a **Deep Intense Rock** fan (loud, fast, darker). Then I added seven tricky profiles meant to confuse the scoring:

- **Sad but Hype:** wants a sad mood but very high energy. No song in the catalog is labeled "sad."
- **Labels vs Numbers:** asks for pop / intense, but describes quiet, slow, acoustic music.
- **Near-Miss Genre:** describes *Rooftop Lights* almost exactly, but calls the genre "pop" instead of "indie pop."
- **Ghost Genre:** asks for k-pop, which isn't in the catalog.
- **Whitespace in Labels:** types " Lofi" and "chill " with extra spaces.
- **Out-of-Range Values:** asks for energy and cheerfulness levels that are impossible (above the maximum or below zero).
- **Genre Only:** gives a genre and nothing else.

- What you looked for in the recommendations
For each one, I checked whether the top song made sense for that listener and read the reasons to see which features were driving the score.

- What surprised you  
- **Labels could beat the actual sound.** With my first weights, the Labels vs Numbers listener got *Gym Hero*, a loud gym anthem, as their #1 song. It matched the words "pop" and "intense" even though it was the opposite of every other preference. This is what made me rebalance the weights.
- **One word cost a perfect match.** *Rooftop Lights* matched the Near-Miss listener's sound perfectly, but it lost a lot of points because "indie pop" didn't count as "pop." With my first weights, *Gym Hero* came within one point of passing it.
- **Typos made the system give up without saying so.** Extra spaces or impossible numbers gave every song a score of zero. The recommender still showed five songs, which were just the first five in the file, with no warning that anything was wrong. *Sunrise City* "won" those lists only because it is the first song in the file.
- **Turning off mood changed more than I expected.** When I briefly removed the mood check, *Focus Flow* jumped to #1 for the lofi fan, and *Gym Hero* fell from #2 to #5 for the rock fan. Its only link to that listener had been the shared word "intense." Mood was acting mostly as a tiebreaker between songs of the same genre, and sometimes it rewarded songs just for sharing a label.

- Any simple tests or comparisons you ran  
**Comparing profiles side by side.** These comparisons use the final weights with all features turned on:

- **High-Energy Pop vs. Chill Lofi:** these two lists share no songs at all. The pop fan gets loud, bright, electronic-sounding songs (*Sunrise City*, *Gym Hero*, *Rooftop Lights*), while the lofi fan gets quiet, slow, acoustic ones (*Library Rain*, *Midnight Coding*, *Focus Flow*). This makes sense because the two profiles sit at opposite ends of energy, tempo, and acousticness, so a song that scores well for one scores poorly for the other.
- **High-Energy Pop vs. Deep Intense Rock:** both listeners want high energy, so they share two songs (*Gym Hero* and *Neon Mirage*). The difference is cheerfulness: the pop list fills up with happy songs like *Rooftop Lights* and *Runway Lights*, while the rock list shifts toward darker ones like *Iron Pulse* and *Night Drive Loop*. This shows that cheerfulness is what separates "party loud" from "angry loud."
- **Chill Lofi vs. Deep Intense Rock:** another pair with no overlap. The lofi fan's top songs have energy around 0.3–0.4, and the rock fan's are all above 0.75. This is the clearest sign that energy is doing its job of separating calm listeners from intense ones.
- **Deep Intense Rock vs. Sad but Hype:** both lists contain almost the same loud songs (*Storm Runner*, *Iron Pulse*, *Neon Mirage*, *Night Drive Loop*, *Gym Hero*), but in a different order. Without a genre to match, *Iron Pulse* moves to #1 for Sad but Hype because it is the darkest-sounding loud song. The scores also drop from about 97 to about 44, because no song can earn the "sad" mood points. The result is reasonable given the catalog, but the low scores show that this listener is not being served well.
- **Labels vs. Numbers vs. Chill Lofi:** even though Labels vs. Numbers asks for "pop" and "intense," its list looks much more like the lofi fan's than the pop fan's. Both get calm, acoustic songs such as *Spacewalk Thoughts* and *Desert Postcard*. This is the behavior I wanted after rebalancing: when the labels and the described sound disagree, the sound wins.
- **High-Energy Pop vs. Near-Miss Genre:** these profiles are almost identical, but Near-Miss describes *Rooftop Lights* exactly. That moves *Rooftop Lights* from #3 to #2, ahead of *Gym Hero*. *Sunrise City* still stays at #1 because it is the only song that matches both "pop" and "happy." This makes sense, but it also shows that one genre word is still worth more than a perfect match on sound.
- **Near-Miss Genre vs. Ghost Genre:** changing the genre to "k-pop," which is not in the catalog, removes *Gym Hero* from the top three. Without genre points, the only songs that stand out are the two "happy" ones, *Sunrise City* and *Rooftop Lights*. After them, the scores fall to about 19, and the rest of the list is decided by energy alone. This is the correct behavior, but the user never learns that their genre was ignored.
- **Whitespace in Labels vs. Out-of-Range Values:** these two very different mistakes produce the exact same list. Every song scores zero, so the system just shows the first five songs in the file. This output is not valid for either user, and the recommender cannot tell the difference between a typo and a real preference.
- **Genre Only vs. Chill Lofi:** both lists start with the same three lofi songs, but Genre Only gives all three exactly 15 points. It cannot rank them, so they appear in file order. Chill Lofi puts them in a meaningful order using energy and acousticness. This shows that genre decides which songs make the list, and the number features decide the order within it.

**Other checks.** I wrote automated tests for the edge cases above, including what happens when a preference is typed as text instead of a number (the program crashes). I also scored 2,000 random listeners to see which songs got recommended most often, which is described in the Limitations section.

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
  - **Partial credit for similar labels.** "Indie pop" should count as close to "pop," and "melancholic" as close to "sad." This would fix the biggest problem I found, where one word difference cost a song most of its label points.
  - **More information about each song.** Adding language, vocals vs. instrumental, release year, and popularity would let listeners ask for things like "instrumental only," "songs in Spanish," or "'90s music," which the model can't handle today.
  - **More than one genre and mood per song.** Real songs often mix styles, like a pop song that is also electronic. Letting each song carry a few tags would make the labels more accurate.
  - **"Avoid" preferences.** A listener should be able to say what they *don't* want, like "no metal" or "nothing too acoustic," so those songs get pushed down or left out.
  - **Let listeners choose what matters most.** Right now everyone gets the same weights. Someone who cares mostly about mood, or mostly about tempo for running, should be able to make that feature count for more.

- Better ways to explain recommendations  
  - **Use plain words instead of feature names.** Right now a reason looks like "valence close to target (+14.4)." A listener would understand "sounds cheerful, like you asked" much better than "valence" or "tempo_bpm."
  - **Only say "close" when it really is close.** Every feature that earns any points gets the label "close to target," even when a song only earned 2.5 out of 20 energy points. Explanations should say "a bit calmer than you wanted" or "much louder than you asked for" when the match is weak.
  - **Show what didn't match, too.** The reasons only list what earned points. *Gym Hero*'s explanation never mentions that it is "intense" when the listener asked for "happy." Showing the misses would make it clear why a song ranked lower than expected.
  - **Warn when a preference can't be matched.** If a listener asks for "sad" or "k-pop," the system should say "no songs in the catalog match this mood/genre" instead of quietly ignoring it. The same goes for typos and impossible values, which currently give every song a score of zero with an empty explanation.
  - **Lead with the main reason.** Instead of a long list of numbers, start with the one or two things that mattered most, like "Recommended mainly because it's lofi and very calm," and keep the full breakdown for anyone who wants details.
  - **Explain why #1 beat #2.** When two songs are close, a short note like "*Library Rain* won because it's more acoustic" would help the listener understand the order, not just the list.

- Improving diversity among the top results 
  - **Limit one song per artist.** For the lofi fan, two of the top three songs are by LoRoom (*Midnight Coding* and *Focus Flow*). Letting each artist appear only once would leave room for other voices.
  - **Skip songs that are near-copies of ones already picked.** After choosing the #1 song, the next pick should get a small penalty if it sounds almost the same. That way the top five covers a few different sides of the listener's taste instead of five versions of one song.
  - **Save one "wildcard" spot.** The fifth slot could go to a good match from a genre the listener didn't ask for. This would help them discover something new while the first four still play it safe.
  - **Penalize big differences more sharply.** In my 2,000-listener test, average-sounding songs like *Blue Hour* showed up in 42% of top-five lists, while distinctive songs like *Salsa de Sol* showed up in only 10%. Taking away more points for big gaps would stop the same middle-of-the-road songs from appearing for everyone.
  - **Break ties fairly.** When songs have the same score, the one listed first in the file always wins. Shuffling ties, or breaking them with another feature, would stop the songs at the top of the file from getting an unfair boost.
 
- Handling more complex user tastes  
  - **Allow ranges instead of one number.** A listener should be able to say "energy between 0.6 and 0.9" instead of picking a single target. Any song inside the range would get full points.
  - **Support more than one taste.** Someone who likes both calm lofi and loud rock currently has to pick a value in the middle, and gets songs that fit neither. Letting a listener have two or more "taste profiles" and mixing results from each would serve them much better.
  - **Accept more than one favorite genre or mood.** A listener should be able to say "pop or electronic" and "happy or confident," with a match on any of them earning points.
  - **Change with the situation.** Taste depends on what someone is doing. The same person might want calm music for studying at night and fast music at the gym. Letting the listener pick a situation, or using the time of day, would make the results fit the moment.
  - **Learn from what the listener does.** If someone skips a song or plays it again, the system could slowly adjust their profile, so their preferences don't have to be typed in perfectly the first time.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
I learned that a recommender is really just a set of choices about what matters and how much. Every weight I picked was a decision about what kind of listener to favor. When genre and mood were worth 45 points, the labels on a song mattered more than how it sounded. Changing a few numbers completely changed who got good recommendations. I also learned that a recommender almost always returns *something*, even when it has no good answer. Testing with strange and broken profiles was the only way to see where the results stopped making sense.

- Something unexpected or interesting you discovered 
What surprised me most was how much a single word could matter. *Gym Hero* is a pop workout song, but it kept showing up as the #2 pick for the rock fan. Its only real connection to that listener was that both were labeled "intense." When I briefly turned off the mood check, *Gym Hero* dropped to #5, and *Focus Flow* jumped to #1 for the lofi fan, even though it isn't labeled "chill." I expected mood to be one of the most important features. Instead, it was often just breaking ties, and sometimes it rewarded songs only for sharing a label. 

- How this changed the way you think about music recommendation apps  
I used to think apps like Spotify just "knew" my taste. Now I realize every recommendation comes from choices someone made about which features to count and how much each one is worth. Those choices decide whose taste gets served well. In my small version, listeners who liked sad music, or genres the catalog barely had, got worse results, and nothing told them that. It makes me wonder how often real apps keep showing me the same safe, average songs because those score well for everyone, and what music I'm missing because of it. I'll pay more attention now to when a playlist feels repetitive. I'll also look for "why this was recommended" explanations, because now I know how much they can reveal.

### Reflection on My Engineering Process

**Biggest learning moment.** My biggest learning moment was the "Labels vs Numbers" test. I had made genre and mood the biggest part of the score because they seemed like the clearest signals of taste. Then I tested a listener who asked for "pop" and "intense" but described quiet, acoustic music, and the #1 pick was *Gym Hero*, a loud gym song. My first idea was to just lower the genre weight, but when I tried it, *Gym Hero* was still #1. The real problem was how much the labels counted *together* compared with how the songs actually sounded. That taught me to test a fix before trusting it. It also taught me that the obvious explanation for a problem isn't always the right one.

**How AI tools helped, and when I double-checked them.** I used an AI assistant to suggest tricky test profiles, run experiments quickly, and help draft documentation. It was most useful for speed. It could score 2,000 random listeners or compare four versions of the weights in seconds, and it suggested edge cases I hadn't thought of, like extra spaces in a label or a negative number of results. I still had to double-check its work:
- It left the mood check turned off after one experiment, so the code no longer matched what my documentation described. I turned it back on and added a test that checks mood matches earn their 15 points, so it can't be turned off again without anyone noticing.
- After I changed the weights, the old sample outputs in my README still showed the previous scores.
- Some drafts it wrote for me were in first person and described things I may not have actually thought. I had to reword those so they were true to my own experience.
- I checked its numbers against real program output instead of trusting its summaries.

The lesson was that AI is a fast helper, but I'm still responsible for making sure the code, the results, and the writing all agree.

**How a simple algorithm can still "feel" like a recommendation.** I was surprised by how convincing the results felt even though the algorithm is just adding up points. When the lofi fan got *Library Rain* and *Midnight Coding*, it felt like the system "got" them. But it had no idea what lofi sounds like; it was only comparing a few numbers. The list of reasons made it feel even smarter, because "energy close to target" sounds like an explanation. Then I saw the other side: with a typo in the profile, the system still confidently showed five songs, all with a score of zero. A simple algorithm can feel smart when the input is clean, and that same confidence is what makes its mistakes easy to miss.

**What I would try next.** If I kept going, I would:
- Turn the "Future Work" ideas into real experiments, starting with partial credit for similar genres and moods (like "indie pop" and "pop"), since that was the most common problem.
- Add input checks and clear warnings when a preference can't be matched, instead of failing silently.
- Add a variety rule, like one song per artist, and test whether it reduces how often average-sounding songs show up.
- Grow the catalog with more genres and more sad or medium-energy songs, then re-run the 2,000-listener test to see if the results become fairer.
