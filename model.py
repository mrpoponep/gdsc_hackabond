def create_quiz(model,nums,document,intructions=""):
    teacher_prompt=f"""
    Given the provided document, generate {nums} questions and return it as a json file with the following key: Question, Option(for multiple choice, None if is not multiple choice) and correct_answer that can be derived from its content. Please ensure the questions are relevant and coherent.

    Document Excerpt (if applicable):
    {document}

    Instructions:
    Read the document carefully.
    Consider key points, concepts, and details within the document.
    Generate questions that seek information or clarification about the document's content.
    Ensure that the questions are grammatically correct and understandable.
    Aim to produce a variety of question types, such as factual, inferential, and evaluative questions.
    Do not put excess comma at the end of the value.
    Do not break the lines.
    {intructions}
    Example_output
    {{"Questions": [{{"Question": "1+1","Option": ["1","2","3","4","5"],"correct_answer": "2"}},{{"Question": "2+2","Option": null,"correct_answer": "4"}}]}}
    """
    print(teacher_prompt)
    response = model.generate_content(teacher_prompt)
    print(response.text)
    return response.text.replace("json", "").replace("```","")

def auto_grading(model,json):
  prompt = f"""You are a teacher, your responsibilities is grading the following student response and 
  providing the answer as a JSON file by adding two key correctness(True/False) and 
  explanation to the original file :\n\n 
  {json}\n\n 
  Please grade this response.
  Instructions:
    If there is no 'answer' field, return "correctness": False and "Explanation": No answer .
  Example_Input
    {{
    "Questions": [
    {{
      "Question": "1+1",
      "Option": [
        "1",
        "2",
        "3",
        "4",
        "5"
      ],
      "correct_answer": "2", 
      'answer': "2"
    }},
    {{
      "Question": "2+2",
      "Option": null,
      "correct_answer": "4",
      'answer': "5"
    }}
  ]
}}
Example_Ouput
{{
    "Questions": [
    {{
      "Question": "1+1",
      "Option": [
        "1",
        "2",
        "3",
        "4",
        "5"
      ],
      "correct_answer": "2", 
      "answer": "2",
      "correctness": "True",
      "explanation": "1+1 = 2 so the answer is true"
    }},
    {{
      "Question": "2+2",
      "Option": null,
      "correct_answer": "4",
      'answer': "5",
      "correctness": "False",
      "explanation": "2+2 = 4 so the answer is false"
    }}
  ]
}}
"""
  print(prompt)
  response = model.generate_content(prompt)
  return response.text.replace("JSON", "").replace("```","")

if __name__=="__main__":
    import google.generativeai as genai
    from google.generativeai.types import HarmCategory, HarmBlockThreshold
    genai.configure(api_key='AIzaSyATnwbAxhJhdp1Kt075vK11QYwIGzjHB0E')
    model = genai.GenerativeModel('gemini-pro')
    docx='''
Definitions:
Polynomial: A polynomial is of the form
f(x) = anxn + an-1xn-1 + ... + a1x + a0 Eq(1)
Where n is the order of the polynomial.
Examples: f (x) = 2x2 - 4x + 10 (Order 2)
f (x) = 9 (Order 0)
In the following definitions, the “equation” can be a polynomial but also any other equation.
Parameters
The values of the constants in an equation. For example, [an, an-1, …a1, a0] are the parameters of an nth-order polynomial, [2, -4, 10] are the parameters of the 2nd order example above, and [C, t] are the parameters of the equation f(x) = C*exp(-x/t). When parameters are constants that multiply terms (such as “C” but not “t” in the last example), we also call them coefficients.
Curve fitting:
Fitting an equation to a set of data points. This is used to test how well a quantitative model fits the data. That is, if you have a data set (x,y), where x and y are vectors, then curve fitting is finding an equation f(x), so that f(x(i)) is close to y(i) for all indices i in the vectors.
Residual:
For each data point, its residual is the difference between the actual data point and the value of the equation used to model the data. That is, the residual is f(x(i)) –y(i).
Least squares fit:
The parameters of an equation that give the lowest value for the sum of the squares of all of the residuals. '''

    input_ = '''{'Questions': [{'Question': 'What is the general form of a polynomial?', 'Option': ['f(x) = x^n + x^(n-1) + ... + x^2 + x + 1', 'f(x) = anxn + an-1xn-1 + ... + a1x + a0', 'f(x) = (ax + b)/(bx + c)', 'f(x) = e^(-x/t)', 'f(x) = sin(x) + cos(x)', 'f(x) = log(x)'], 'correct_answer': 'f(x) = anxn + an-1xn-1 + ... + a1x + a0'}, {'Question': 'Which of the following is NOT a parameter in a polynomial?', 'Option': ['an', 'a0', 'b', 't', 'C'], 'correct_answer': 'b'}, {'Question': 'Define curve fitting.', 'Option': None, 'correct_answer': 'Fitting an equation to a set of data points to test how well a quantitative model fits the data.'}, {'Question': 'What is the objective of a least squares fit?', 'Option': None, 'correct_answer': 'To minimize the sum of the squares of the residuals.', 'answer': 'j'}]}'''

    #res= create_quiz(model,nums=1,document=docx,intructions=None)
    res = auto_grading(model,input_)
    print(res)