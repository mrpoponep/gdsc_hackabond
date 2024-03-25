import streamlit as st
import docx
from quiz import create_quiz
import json
import google.generativeai as genai
genai.configure(api_key='AIzaSyATnwbAxhJhdp1Kt075vK11QYwIGzjHB0E')
model = genai.GenerativeModel('gemini-pro')

def main():
    st.title("Document to Questions Generator")
    uploaded_file = st.file_uploader("Upload a document", type=["txt", "docx"])
    Generate_Questions = True
    questions=None
    text=None
    
    if uploaded_file is not None:
        if uploaded_file.type == "text/plain":  
            text = uploaded_file.getvalue().decode("utf-8")  
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":  
            try:
                docx_text = docx.Document(uploaded_file)
                text = "\n".join([para.text for para in docx_text.paragraphs])
            except Exception as e:
                st.error("Error: Unable to read the docx file.")
                st.stop()
        else:
            st.error("Unsupported file format. Please upload a txt or docx file.")
            st.stop()
    if 'generated_questions' not in st.session_state:
        st.session_state.generated_questions = None
    if text is not None:
        nums_question = st.number_input(label="Num of Questions", value=1, key="Num Questions", max_value=20)
        instructions = st.text_area(label="Instructions", value="", key="Instructions")
        if st.button("Generate Questions"):
            Generate_Questions = True
            st.session_state.generated_questions = create_quiz(model,nums_question,text,instructions)
            
    if st.session_state.generated_questions:
        st.write("## Generated Questions:")
        
        st.write(st.session_state.generated_questions)
        question_data = json.loads(st.session_state.generated_questions)
    
        for idx, question in enumerate(question_data["Questions"]):
            st.subheader(f"Question {idx+1}:")
            question_text = st.text_input("Question:", question['Question'],key=f"Question {idx} Title",)
            
            if question["Option"]!=None:
                options=[None]*len(question["Option"])
                for indx,option in enumerate(question["Option"]):
                    option_text = st.text_input(f"Answer Option {indx+1}",option,key=f"Question {idx} option {indx}",label_visibility='hidden')
                    options[indx]=option_text
            correct_answer = st.text_input("Correct Answer:", question['correct_answer'],key=f"Question {idx} Answer",)
            if st.button(f"Save Question {idx+1}", key=f'Save Question{idx}'):
                # Update the question data with the new values
                question_data["Questions"][idx]['Question'] = question_text
                question_data["Questions"][idx]["Option"] = options
                question_data["Questions"][idx]['correct_answer'] = correct_answer
                # Print the updated question_data for debugging
                print(question_data)
if __name__ == "__main__":
    main()