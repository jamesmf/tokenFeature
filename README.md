# tokenFeature
convert text to tokens and tokens to a feature vector

This feature vector encodes which combinations of letters and spaces are observed in a string.  Useful primarily for adding to a feature vector that lies more in the semantic space.  It stores information like "does the word start with 'un'", "does the string contain 'not'", or "does the word end with 'ase'" - all of which are useful for answering important NLP questions - particularly about unseen words and their potential relation to known items in the vocabulary.

Similarly, the vector strives to encode abbreviations and acronyms in a useful way.  

The two test uses here were:

1 - mapping Kaggle's college basketball team name list to SportsReference's list


2 - training a SVM on a number of protein names to see how separable they are from regular English text


The first was very successful and the second showed only mild promise.  I suspect that this feature space might be paired well with word2vec vectors using something of a KNN approach.
