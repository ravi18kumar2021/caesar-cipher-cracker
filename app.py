import streamlit as st
import nltk
from nltk.corpus import words

# download word list if not already
nltk.download('words', quiet=True)
words_set = set(words.words())

# caesar cipher function
def caesar_cipher(message:str, shift:int, encrypt:bool):
    alphabets = 'abcdefghijklmnopqrstuvwxyz'
    result = ''
    for ch in message:
        if ch.lower() not in alphabets:
            result += ch
        else:
            if encrypt == True:
                index = (alphabets.find(ch.lower()) + shift) % 26
            else:
                index = (alphabets.find(ch.lower()) - shift) % 26
            result += alphabets[index]
    return result

# word scoring
def score_text(text, word_set):
    words_in_text = text.lower().split()
    score = sum(1 for word in words_in_text if word.strip('.,!?') in word_set)
    return score

# secret message cracker 
def crack_caesar(cipher_text):
    best_score = 0
    best_shift = None
    best_guess = ''
    all_results = []

    for shift in range(1, 26):
        guess = caesar_cipher(cipher_text, shift, encrypt=False)
        score = score_text(guess, words_set)
        all_results.append((score, shift, guess))
        if score > best_score:
            best_score = score
            best_shift = shift
            best_guess = guess
    return best_score, best_shift, best_guess, all_results

st.title("🧠 Caesar Cipher Cracker")
st.write("Try to decode Caesar-encrypted text using AI-style scoring.")
cipher_input = st.text_area("🔐 Enter Encrypted Text", height=150)
if st.button("🔓 Crack the Code") and cipher_input:
    score, shift, guess, all_results = crack_caesar(cipher_input)
    if guess:
        st.subheader("✅ Cracked Output :")
        st.code(guess, language='text')
        st.success(f"🎉 Most likely decrypted text found on Shift : {shift}")

        with st.expander("🔎 See all shift attempts"):
            for sc, sh, g in all_results:
                st.write(f"🔢 Shift: {sh:2}   📊 Score: {sc:2}   📝 {g}")
    else:
        st.subheader("😕 Couldn’t crack the code")
        st.error("🤷‍♂️ No likely English sentence found. Try again")