import streamlit as st
import pandas as pd

def isValid(word, center_letter, all_letters):
    '''
    Only valid words are:
    - At least 4 letters
    - Contains the center letter
    - Only uses letters in the outer letters
    '''
    return (len(word) >= 4 and
            center_letter in word and
            set(word).issubset(all_letters))

def score(word, is_pangram):
    '''
    How To Play Spelling Bee
    (Courtesy: New York Times)
    Words must include the center letter.

    Words must contain at least four letters.

    Letters can be used more than once.

    Our word list does not include words that are offensive, obscure, hyphenated or proper nouns.

    Four-letter words are worth one point each.

    Longer words earn one point per letter. A six-letter word is worth six points.

    Each puzzle includes at least one “pangram,” which uses every letter at least once. A pangram is worth an additional seven points.
    '''
    if len(word) == 4:
        return 1
    elif is_pangram:
        return len(word) + 7
    else:
        return len(word)

def solver(dictionary, center_letter, outer_letters):
    '''
    Returns a dictionary of all valid words, pangrams, and their scores
    Args:
        dictionary: list of all words
        center_letter: the center letter of the puzzle
        outer_letters: the outer letters of the puzzle
    Returns:
        dictionary: {
            'valid_words': list of all valid words,
            'pangrams': list of all pangrams,
            'scored_words': list of tuples of (word, score),
            'total_score': total score of all words
        }
    '''
    all_letters = set(center_letter + ''.join(outer_letters))
    
    valid_words = [word for word in dictionary if isValid(word, center_letter, all_letters)]
    pangrams = [word for word in valid_words if set(word) == all_letters]
    
    scored_words = [(word, score(word, word in pangrams)) for word in valid_words]
    scored_words.sort(key=lambda x: x[1], reverse=True)
    
    total_score = sum(score for _, score in scored_words)
    
    return {
        'valid_words': valid_words,
        'pangrams': pangrams,
        'scored_words': scored_words,
        'total_score': total_score
    }

# Load dictionary
@st.cache_data
def load_dictionary():
    '''
    Loads dictionary from pickle (WordNet 3.0)
    '''
    dictionary = pd.read_pickle('data/words.pkl')['word'].tolist()
    dictionary = [word.lower() for word in dictionary]
    return list(set(dictionary))

dictionary = load_dictionary()

st.title("NYT Spelling Bee Bot")
st.write("Based on WordNet 3.0 Dictionary")
st.write("Enter the center letter and outer letters for today's Spelling Bee puzzle:")

col1, col2 = st.columns(2)

with col1:
    center_letter = st.text_input("Center Letter", "i").lower()

with col2:
    outer_letters = st.text_input("Outer Letters (no spaces or chars)", "bcelnv").lower()

if st.button("Solve Puzzle"):
    if len(center_letter) != 1 or len(outer_letters) != 6:
        st.error("Please enter 1 center letter and 6 outer letters.")
    else:
        results = solver(dictionary, center_letter, outer_letters)

        st.write(f"Found {len(results['valid_words'])} valid words")
        st.write(f"Total score: {results['total_score']}")

        st.subheader("Pangrams")
        st.write(", ".join(results['pangrams']))

        st.subheader("All Valid Words")
        df = pd.DataFrame(results['scored_words'], columns=['Word', 'Score'])
        st.dataframe(df)

        st.subheader("Word Length Distribution")
        length_dist = df['Word'].str.len().value_counts().sort_index()
        st.bar_chart(length_dist)

        st.subheader("Top 10 Scoring Words")
        st.table(df.head(10))

        # Download button for all words
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download all words as CSV",
            data=csv,
            file_name="spelling_bee_words.csv",
            mime="text/csv",
        )