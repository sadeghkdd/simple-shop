import streamlit as st
import sqlite3

conn = sqlite3.connect('products.db')
c = conn.cursor()

c.execute('SELECT name, price, img, link FROM products')  
rows = c.fetchall()

st.title('Phone Shop 📱')

for i in range(0, len(rows), 3):
    cols = st.columns(3)
    for j, col in enumerate(cols):
        if i + j < len(rows):
            name, price, img_url, link = rows[i + j]  
            with col:
                st.image(img_url, caption=name)
                st.write(f'Price: {price}')
                st.markdown(f'[View on eBay]({link})')  

conn.close()
