from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # Use SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Applicant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)

# Create operation
@app.route('/api/create', methods=['POST'])
def create():
    try:
        req_data = request.get_json()
        name = req_data['name']
        age = req_data['age']
        phone_number = req_data['phone_number']
        email = req_data['email']

        # Save data to database
        new_applicant = Applicant(name=name, age=age, phone_number=phone_number, email=email)
        db.session.add(new_applicant)
        db.session.commit()

        return jsonify({'message': 'Data created successfully!'})

    except Exception as e:
        print("Error:", e)  # Add this line for debugging
        return jsonify({'error': "Invalid Data Format Or Data Already Exist"})

# Read operation
@app.route('/api/read', methods=['GET'])
def read():
    applicants = Applicant.query.all()
    result = []
    for applicant in applicants:
        result.append({
            'name': applicant.name,
            'age': applicant.age,
            'phone_number': applicant.phone_number,
            'email': applicant.email,
        })
    return jsonify(result)

# Update operation
@app.route('/api/update/<email>', methods=['PUT'])
def update(email):
    req_data = request.get_json()

    applicant = Applicant.query.filter_by(email=email).first()
    if applicant:
        applicant.name = req_data.get('name', applicant.name)
        applicant.age = req_data.get('age', applicant.age)
        applicant.phone_number = req_data.get('phone_number', applicant.phone_number)
        db.session.commit()
        return jsonify({'message': f'Data for {email} updated successfully!'})
    else:
        return jsonify({'error': f'Data for {email} not found!'})

# Delete operation
@app.route('/api/delete/<email>', methods=['DELETE'])
def delete(email):
    applicant = Applicant.query.filter_by(email=email).first()
    if applicant:
        db.session.delete(applicant)
        db.session.commit()
        return jsonify({'message': f'Data for {email} deleted successfully!'})
    else:
        return jsonify({'error': f'Data for {email} not found!'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
