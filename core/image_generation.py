from openai import OpenAI
import streamlit as st

def generate_book_image(prompt: str, client: OpenAI) -> str:
    """
    Generates an image URL using OpenAI's DALL-E API based on the book theme or title.
    Returns the image URL as a string.
    """
    try:
        dalle_prompt = f"An artistic book cover representing: {prompt}"
        response = client.images.generate(
            model="dall-e-3",
            prompt=dalle_prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        st.warning(f"⚠️ Image generation failed: {e}")
        return ""
