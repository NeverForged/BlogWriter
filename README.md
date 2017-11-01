# BlogWriter
In an amazing attempt at laziness, I am writing a program to write my Geeks Who Drink Blogs for me.  Because how Geek is that?

## First Go
So, wrote some code, stole some code from old homeworks, grabbed the text of a bunch of old blogs.  Here it is.

### Method
* Make n-grams
* Randomly grab an n-gram key
* Grab some number of words that come after the key, then use cosine similarity to pick the closest one to a given topic.
* Grab last n words, rinse, repeat.

### Results
Here it is:
>> 'With all of our limbs! Yay! A few clever team names, and none that i need to edit before posting, so we all win at life. I even got to do an archer-esque “danger zone!”, so i was stoked. In preparing for the evening, found out that magnolia is known as a coug bar… or cougar bar. Let’s just say that, being a recent transplant from boston made me… and my wife… think that meant something very different, but the older ladies were not out in force, so all is well. With record numbers of teams, got to give a shout out to mac, i hope his birthday was awesome… see, just like the plug says, we do birthdays… even if it’s incidental because you went to the bar on it. Quiz went great. Had ties for 2nd to last and 2nd. Handled the later with a tiebreaker; the former with a dance-off. Yes. Tie for first place. Wishing it was second, because then dance off! But no, had to use the tiebreaker round… which came down to d&d saving a team. Seriously. What i do know, is that certain things are, intrinsically, true. I also know that they are not “outside the cave”, but rather have their hands free to make shadow puppets. An example of a false belief) that the moon is made of green cheese. So that, in a nutshell, is why i’m unemployed (except for quiz) in seattle… i gave up my job in the ma department of elementary and secondary education and drove across the country for my wife’s sanity (anyone hiring a test developer, or is that too soon?). But people said “if it’s global warming, why is it colder out?”. In response, of course, geologists and scientists ridiculed them and continued to… kidding, no, they changed the term. This shows a level of seriousness; if the term that best fits academically loses the needed audience, change it. Find one that works. Hell, works better than belittling and keeping on. Then leaving, i noticed my front tire was completely flat. Couldn’t find my jack. Called aaa. He couldn’t find the hole in my tire. Good times. Quiz had some drama, namely a team had 7 players, didn’t tell me, then one split at the end of the night, we can only have 1 first place team… and with two teams tied for that honor, we had sudden death! (does this mean i lied about the lack of anything resembling a computer in 299 bc explains why he used a cave instead. The competition was fierce… almost as fierce as that music round (seriously, only one team got more than 8 on that). Ended with…sudden death between october owls and tba: shimmy shimmy hillary… they’d shimmied it in at the end, slipping in the 6 to get the sudden death points. Wow, that came out wrong, i meant henry vi on one of the two mistakes above (often against each other), hence the “clickbait” title.'

### Conclusion
* Shuffle File could use some way to mark breaks (or file in general could mark breaks rather than shuffle)
* More grammar editing needed, though trigrams are fairly good for that (need to fix punctuation and capitalization though)
* Need more writing samples.
