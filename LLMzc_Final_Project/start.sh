#!/bin/bash
# Start both apps in the background
streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0 &
streamlit run dashboard.py --server.port=8502 --server.address=0.0.0.0 &

# Wait for both processes
wait