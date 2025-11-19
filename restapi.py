from flask import flask, request, jsonify
# Initialize the Flask app
app = flask(__name__)

# In-memory data store for users
# Key: user_id (integer), Value: user_data (dictionary)
# We'll start with a few sample users.
users = {
    1: {'username': 'alice', 'email': 'alice@example.com'},
    2: {'username': 'bob', 'email': 'bob@example.com'}
}

# Simple counter to assign new IDs
next_user_id = 3

# --- 1. GET (Read All and Read One) ---
@app.route('/users', methods=['GET'])
def get_users():
    """Retrieves a list of all users."""
    # Convert the dictionary values to a list for JSON output
    user_list = [{'id': id, **data} for id, data in users.items()]
    return jsonify(user_list)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieves a single user by ID."""
    user = users.get(user_id)
    if user:
        # Include the ID in the response
        response_data = {'id': user_id, **user}
        return jsonify(response_data)
    # If the user is not found, return a 404 Not Found error
    return jsonify({'error': 'User not found'}), 404

# --- 2. POST (Create) ---
@app.route('/users', methods=['POST'])
def create_user():
    """Creates a new user."""
    global next_user_id
    
    # Get the JSON data from the request body
    new_user_data = request.json
    
    # Simple validation
    if not new_user_data or 'username' not in new_user_data or 'email' not in new_user_data:
        return jsonify({'error': 'Missing username or email in request'}), 400 # Bad Request

   # Assign a new ID and store the user
    user_id = next_user_id
    users[user_id] = {'username': new_user_data['username'], 'email': new_user_data['email']}
    next_user_id += 1
    
    # Return the newly created user data with the ID and a 201 Created status
    response_data = {'id': user_id, **users[user_id]}
    return jsonify(response_data), 201

# --- 3. PUT (Update/Replace) ---
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates an existing user (replaces all fields)."""
    if user_id not in users:
        return jsonify({'error': 'User not found'}), 404
        
    update_data = request.json
    
    # Simple validation
    if not update_data or 'username' not in update_data or 'email' not in update_data:
        return jsonify({'error': 'Missing username or email in request'}), 400

    # Update the user data
    users[user_id] = {'username': update_data['username'], 'email': update_data['email']}
    
   # Return the updated user data
    response_data = {'id': user_id, **users[user_id]}
    return jsonify(response_data)

# --- 4. DELETE (Delete) ---
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a user by ID."""
    if user_id in users:
        del users[user_id]
        # Return a 204 No Content status for successful deletion
        return '', 204 
    
    return jsonify({'error': 'User not found'}), 404

# Run the application
if __name__ == '_main_':
    # Setting debug=True restarts the server automatically on code changes
    app.run(debug=True)