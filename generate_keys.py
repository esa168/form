import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names = ["jarick", "elton"]
usernames = ["jarick", "esa"]
passwords = ["pevear8?1", "341438"]

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"

#below saves to the archive folder
#file_path = Path(__file__).parent / ".archive/xxxx.pkl"

with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)