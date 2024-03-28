from flask import Flask, render_template, request, jsonify
import json
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

# Load customer and plan data from JSON files
def load_data(filename):
    with open(filename) as f:
        return json.load(f)

customers = load_data('customer_data.json')
plans = load_data('plan_data.json')

class CustomerResource(Resource):
    def post(self):
        data = request.json
        required_fields = ['name', 'dob', 'email', 'adharNumber', 'assignedMobileNumber', 'plan']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing fields'}), 400
        # Find the selected plan and integrate plan details into customer data
        selected_plan = next((plan for plan in plans if plan['planName'] == data['plan']), None)
        if selected_plan is None:
            return jsonify({'error': 'Invalid plan selected'}), 400
        data['planCost'] = selected_plan['planCost']
        data['planValidity'] = selected_plan['validity']
        #data['planStatus'] = selected_plan['planStatus']
        data['registrationDate'] = '2024-03-28'  # Assuming registration date is current date
        data['id'] = len(customers) + 1
        customers.append(data)
        with open('customers.json', 'w') as f:
            json.dump(customers, f, indent=4)
        return jsonify({'message': 'Customer registered successfully'}), 201

    def get(self):
        return jsonify(customers)

class UpdatePlanResource(Resource):
    def get(self, customer_id):
        plan_html = [f'<option value="{p['planName']}">{p['planName']}</option>' for p in plans]
        return f"<select hx-post='/api/customer/{customer_id}/update'>" + ''.join(plan_html)+ '</select>'

    def put(self, customer_id):
        data = request.json
        required_fields = ['plan']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing fields'}), 400
        # Find customer by ID
        customer = next((c for c in customers if c['id'] == customer_id), None)
        if customer is None:
            return jsonify({'error': 'Customer not found'}), 404
        # Find the selected plan and update plan details
        selected_plan = next((plan for plan in plans if plan['planName'] == data['plan']), None)
        if selected_plan is None:
            return jsonify({'error': 'Invalid plan selected'}), 400
        customer['plan'] = selected_plan['planName']
        customer['planCost'] = selected_plan['planCost']
        customer['planValidity'] = selected_plan['validity']
        customer['planStatus'] = selected_plan['planStatus']
        with open('customers.json', 'w') as f:
            json.dump(customers, f, indent=4)
        return jsonify({'message': 'Plan updated successfully'}), 200

class RenewPlanResource(Resource):
    def post(self, customer_id):
        # Find customer by ID
        customer = next((c for c in customers if c['id'] == customer_id), None)
        if customer is None:
            return jsonify({'error': 'Customer not found'}), 404
        # Renew plan
        if customer['planStatus'] == 'Active':
            customer['planStatus'] = 'Renewed'
        else:
            return jsonify({'error': 'Cannot renew. Plan is not active'}), 400
        with open('customers.json', 'w') as f:
            json.dump(customers, f, indent=4)
        return jsonify({'message': 'Plan renewed successfully'}), 200

@app.route('/')
def index():
    return render_template('index.html', customers=customers)

@app.route('/customer', methods=['GET'])
def customers_list():
    return render_template('customers.html', customers=customers)

@app.route('/new/customer', methods=['GET'])
def new_customer():
    return render_template('new_customers.html', customers=customers)



api.add_resource(CustomerResource, '/api/customers')
api.add_resource(UpdatePlanResource, '/api/customers/<int:customer_id>/update_plan')
api.add_resource(RenewPlanResource, '/api/customers/<int:customer_id>/renew_plan')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

