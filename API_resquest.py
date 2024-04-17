import requests
import json

# Define the API endpoint URL
api_url = "http://127.0.0.1:8000/generate_quiz/"

def call_generate_api():
    payload = {
        "nums": 5,
        "document": '''
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
    The parameters of an equation that give the lowest value for the sum of the squares of all of the residuals. ''',
        "instructions": "These are additional instructions for generating the quiz."
    }

    try:
        # Make the POST request to the API
        response = requests.post(api_url, json=payload)
        # Check if the request was successful
        if response.status_code == 200:
            # Print the generated quiz questions
            questions = (response.json())
            print(questions)
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")


def call_grade_api(json_data):
    try:
        # Define the API endpoint URL
        api_url = "http://127.0.0.1:8000/grade/"

        # Define the request payload
        payload = {"json_data": json_data}

        # Make the POST request to the API
        response = requests.post(api_url, json=payload)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            graded_data = response.json()
            print(graded_data)
            return graded_data
        else:
            print(f"Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage
json_data = {
    "Questions": [
        {
            "Question": "1+1",
            "Option": ["1", "2", "3", "4", "5"],
            "correct_answer": "2",
            "answer": "2"
        },
        {
            "Question": "2+2",
            "Option": None,
            "correct_answer": "4",
            "answer": "5"
        }
    ]
}

if __name__ == "__main__":
    call_generate_api()
    #call_grade_api(json_data)