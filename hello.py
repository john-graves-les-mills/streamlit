import streamlit as st
if st.button("Click me"):
  st.write("Hello world")

if st.text_input("Pick a number:"):
  st.write(f"You picked:")
