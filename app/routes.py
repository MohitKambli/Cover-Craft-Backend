from flask import Blueprint, request, jsonify
from app.utils import generate_cover_letter
from app.s3_utils import upload_file_to_s3

api = Blueprint('api', __name__)

@api.route('/hello', methods=['GET'])
def hello():
    return 'Hello World'

@api.route('/generate-cover-letter', methods=['POST'])
def generate_cover_letter_api():
    try:
        # Get the uploaded resume file and job description
        resume = request.files.get("resume")
        job_description = request.form.get("job_description")

        if not resume or not job_description:
            return jsonify({'error': 'Resume file and job description are required.'}), 400

        # Upload the resume to S3
        _, resume_url = upload_file_to_s3(resume)

        # Generate the cover letter using the S3 pre-signed URL
        cover_letter = generate_cover_letter(resume_url, job_description)
        print('Cover Letter: ', cover_letter)
        return jsonify({'cover_letter': cover_letter})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
