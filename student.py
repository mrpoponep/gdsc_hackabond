import streamlit as st
from quiz import create_quiz
import json
import google.generativeai as genai
genai.configure(api_key='AIzaSyATnwbAxhJhdp1Kt075vK11QYwIGzjHB0E')
model = genai.GenerativeModel('gemini-pro')

def load_questions(uploaded_file):
    content = uploaded_file.getvalue()
    content_str = content.decode("utf-8")
    return json.loads(content_str)

def save_answers(answers):
    # Implement logic to save student answers (e.g., to a database)
    pass

def main():
    st.title("Test Platform")

    # Teacher Upload Section
    st.title("Teacher Section")
    uploaded_file = st.sidebar.file_uploader("Upload Questions (JSON)", type=["json"],key="file")

    if uploaded_file is not None:
        question_data = load_questions(uploaded_file)
        st.sidebar.write("Questions Loaded Successfully!")
        st.sidebar.write(question_data)

    # Student Section
    st.title("Student Section")

    if 'question_data' in locals():
        st.write("Here are the questions:")

        for idx, question in enumerate(question_data["Questions"]):
            st.subheader(f"Question {idx+1}:")
            question_text = st.text_input("Question:", question['Question'],key=f"Question {idx} Title",)
            
            if question["Option"]!=None:
                options=[None]*len(question["Option"])
                options[idx] = st.radio(f"Question {idx+1}:", options=range(len(question['Option'])))

            answer = st.text_input("Answer:", question['correct_answer'],key=f"Question {idx} Answer",)
            if st.button(f"Save Question {idx+1}", key=f'Save Question{idx}'):
                # Update the question data with the new values
                question_data["Questions"][idx]['Question'] = question_text
                question_data["Questions"][idx]["Option"] = options
                question_data["Questions"][idx]['answer'] = answer
                # Print the updated question_data for debugging
                print(question_data)

if __name__ == "__main__":
    main()
