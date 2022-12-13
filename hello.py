import streamlit as st
if st.button("Click me"):
  st.write("Hello world")

my_pick = st.text_input("Pick a number:")
if my_pick:
  st.write(f"You picked: {my_pick}")
