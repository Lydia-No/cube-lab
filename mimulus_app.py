import sys
import os

# Add src folder to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

import streamlit as st
from cube_explorer.grammars.mimulus import walk_sequence

BITS = 8

st.title("Mimulus Hypercube Explorer")

sequence_text = st.text_input(
    "Symbol sequence",
    value="cave horse ladder flowers storm"
)

if sequence_text:

    sequence = sequence_text.strip().split()

    try:
        path = walk_sequence(0, sequence)

        st.subheader("Trajectory")

        for i, state in enumerate(path):
            st.write(f"step {i:02d}  state={state:3d}  bits={state:0{BITS}b}")

    except Exception as e:
        st.error(str(e))O
