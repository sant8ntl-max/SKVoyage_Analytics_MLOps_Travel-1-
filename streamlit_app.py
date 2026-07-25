"""Streamlit app: explore the data and get hotel recommendations."""
import pickle
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Voyage Analytics", layout="wide")
st.title("🌍 Voyage Analytics — Travel Insights & Recommendations")

with open("artifacts/hotel_recommender.pkl", "rb") as f:
    rec_artifact = pickle.load(f)

hotel_profile = rec_artifact["hotel_profile"]
similarity_matrix = rec_artifact["similarity_matrix"]


def recommend_hotels(hotel_name, top_n=5):
    matches = hotel_profile.index[hotel_profile["name"] == hotel_name].tolist()
    if not matches:
        return pd.DataFrame(columns=["name", "place", "avg_price"])
    idx = matches[0]
    sims = sorted(enumerate(similarity_matrix[idx]), key=lambda x: x[1], reverse=True)[1:top_n + 1]
    rec_idx = [i for i, _ in sims]
    return hotel_profile.iloc[rec_idx][["name", "place", "avg_price"]].reset_index(drop=True)


st.sidebar.header("Hotel Recommender")
chosen_hotel = st.sidebar.selectbox("Pick a hotel you like", hotel_profile["name"].unique())
top_n = st.sidebar.slider("Number of recommendations", 3, 10, 5)

st.subheader(f"Hotels similar to '{chosen_hotel}'")
st.dataframe(recommend_hotels(chosen_hotel, top_n))

st.subheader("Most-booked hotels")
st.bar_chart(hotel_profile.sort_values("bookings", ascending=False).head(10).set_index("name")["bookings"])

st.subheader("Average price by destination")
st.bar_chart(hotel_profile.groupby("place")["avg_price"].mean().sort_values(ascending=False).head(10))
