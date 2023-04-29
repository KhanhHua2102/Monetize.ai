from application import app

from flask import jsonify, request




from flask_cors import CORS

import gpt
import stock
import sql


CORS(app)



context_data = 'You are a friendly financial chatbot. The user will ask you questions, and you will provide polite responses.\n\n'


@app.route('/generate', methods=['POST'])
def generate():
    global context_data
    print("user message received:")
    data = request.get_json()
    userMessage = data['prompt']
    print(userMessage + '\n')

    promptResult = stock.promptProfit(userMessage)
    # perform a specific action for when stock information is present
    if promptResult[1]:
        print("Stock information detected in context_data. Performing specific action...\n")
        context_data += 'Q: ' + promptResult[0] + '\nA: '
    # normal bot reply
    else:
        print("No stock information detected in context_data.\n")
        context_data += 'Q: ' + userMessage + '\nA: '

    result = gpt.openAi(context_data)
    context_data += result + '\n\n'
    print(context_data)
    return jsonify({'response': result})

@app.route('/signUp', methods=['POST'])
def signUp():
    
    account_name = request.form['Account-Name']
    email_address = request.form['Email-Address']
    phone_number = request.form['Phone-Number']
    password = request.form['Password']
    re_password = request.form['Re-Password']

    # Add your validation logic here to ensure password and re_password are the same

    # Perform any other necessary actions with the received data
    print(f'Account Name: {account_name}')
    print(f'Email Address: {email_address}')
    print(f'Phone Number: {phone_number}')
    print(f'Password: {password}')
    print(f'Re-entered Password: {re_password}')

    sql.addUser(account_name,email_address,phone_number,password)

    return 'Success!'

