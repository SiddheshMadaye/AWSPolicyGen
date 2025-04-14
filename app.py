from flask import Flask, render_template, request, jsonify
import boto3
import json

app = Flask(__name__)

# Initialize AWS SDK
s3_client = boto3.client('s3')

# Sample list of AWS services and actions
aws_actions = {
    "S3": ["s3:PutObject", "s3:GetObject", "s3:ListBucket"],
    "EC2": ["ec2:StartInstances", "ec2:StopInstances", "ec2:DescribeInstances"]
}

@app.route('/')
def index():
    return render_template('index.html', aws_actions=aws_actions)

@app.route('/generate_policy', methods=['POST'])
def generate_policy():
    service = request.form['service']
    actions = request.form.getlist('actions')
    resource = request.form['resource']
    condition = request.form['condition']

    # Generate IAM Policy JSON
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",  # Hardcoded to "Allow" for simplicity
                "Action": actions,
                "Resource": resource,
                "Condition": {"StringEquals": {"aws:SourceIp": condition}} if condition else {}
            }
        ]
    }

    return jsonify(policy)

if __name__ == '__main__':
    app.run(debug=True)
