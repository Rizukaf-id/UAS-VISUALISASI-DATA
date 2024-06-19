import os

import streamlit as st
from streamlit_navigation_bar import st_navbar

import pages as pg


st.set_page_config(initial_sidebar_state="collapsed", page_title="052-Rizka F")

pages = ["Adventure Works", "IMDB"]
parent_dir = os.path.dirname(os.path.abspath(__file__))
# styles = {
#     "nav": {
#         "background-color": "royalblue",
#         "justify-content": "left",
#     },
#     "span": {
#         "color": "white",
#         "padding": "14px",
#     },
#     "active": {
#         "background-color": "white",
#         "color": "var(--text-color)",
#         "font-weight": "normal",
#         "padding": "14px",
#     }
# }
options = {
    "show_menu": False,
    "show_sidebar": False,
}

page = st_navbar(
    pages,
    # styles=styles,
    # options=options,
)

functions = {
    "Adventure Works": pg.show_aw,
    "IMDB": pg.show_imdb,
}
go_to = functions.get(page)
if go_to:
    go_to()