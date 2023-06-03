import requests

API_KEY = 'YRM6sMuZOWNWJx56lAnX*g(('
keyword = '#artifactory'

# Set the parameters for the API request
params = {
    'order': 'desc',
    'sort': 'activity',
    'tagged': keyword,
    'site': 'stackoverflow',
    'key': API_KEY,
    'page': 1, 
    'pagesize': 100  
}

# Make API request to search for questions with the keyword
search_url = "https://api.stackexchange.com/2.3/questions"
response = requests.get(search_url, params=params)
data = response.json()

while data['items']:
    questions = data['items']

    for question in questions:
        question_id = question['question_id']
        question_title = question['title']
    
        # Make API request to get answers for the question
        answers_url = f"https://api.stackexchange.com/2.3/questions/{question_id}/answers"
        answers_params = {
            'site': 'stackoverflow',
            'key': API_KEY,
            'page': 1,  
            'pagesize': 100  
        }

        answers_response = requests.get(answers_url, params=answers_params)
        answers_data = answers_response.json()

        # Create a list to store the answers for the question
        question_answers = []

        while answers_data['items']:
            
            for answer_data in answers_data['items']:
                answer_id = answer_data['answer_id']
                answer_upvotes = answer_data.get('score', 0)
                is_accepted = answer_data.get('is_accepted', False)

                answer_url = f"https://stackoverflow.com/a/{answer_id}"

                # Add answer details to the list
                answer_details = {
                    'Answer ID': answer_id,
                    'Number of upvotes': answer_upvotes,
                    'Accepted': is_accepted,
                    'URL': answer_url
                }
                question_answers.append(answer_details)

            if answers_data['has_more']:
                answers_params['page'] += 1
                answers_response = requests.get(answers_url, params=answers_params)
                answers_data = answers_response.json()
            else:
                break

        # Save the question and answers to a text file
        filename = f"Question-{question_id}.txt"
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(f"Question: {question_title}\n\n")
            file.write("Answers:\n\n")
            if len(question_answers) == 0:
                file.write("No answers\n")
            else:
                for answer in question_answers:
                    file.write(f"Answer ID: {answer['Answer ID']}\n")
                    file.write(f"Number of upvotes: {answer['Number of upvotes']}\n")
                    file.write(f"Accepted: {'Yes' if answer['Accepted'] else 'No'}\n")
                    file.write(f"URL: {answer['URL']}\n")
                    file.write("\n---\n\n")

        print(f"Saved question with ID {question_id} to {filename}")

    # Check if there are more pages of questions
    if data['has_more']:
        params['page'] += 1
        response = requests.get(search_url, params=params)
        data = response.json()
    else:
        break
