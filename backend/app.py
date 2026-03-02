from flask import Flask, jsonify, request
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)

# Instructions:
# - Use the functions in backend/db.py in your implementation.
# - You are free to use additional data structures in your solution
# - You must define and tell your tutor one edge case you have devised and how you have addressed this

@app.route("/students")
def get_students():
    """
    Route to fetch all students from the database
    return: Array of student objects
    """
    # TODO: replace with your implementation. This is a mock response
    students = db.get_all_students()
    return jsonify(students), 200


@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """

    # Getting the request body - replace with your implementation
    student_data = request.json
    
    # Checking input data
    if not student_data:
        return jsonify({"error": "Missing request body"}), 404
    
    name = student_data.get("name")
    course = student_data.get("course")
    mark = student_data.get("mark", 0)

    # Checking student info valid
    if not isinstance(name, str) or not name.strip():
        return jsonify({"error": "Invalid name"}), 404
    if not isinstance(course, str) or not course.strip():
        return jsonify({"error": "Invalid course"}), 404
    if not isinstance(mark, int) or not (0 <= mark <= 100):
        return jsonify({"error": "Invalid mark"}), 404

    created = db.insert_student(name.strip(), course.strip(), mark)
    return jsonify(created), 200


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    existing = db.get_student_by_id(student_id)
    if not existing:
        return jsonify({"error": "Student not found"}), 404

    student_data = request.get_json()
    if not student_data:
        return jsonify({"error": "Missing request body"}), 404

    name = student_data.get("name")
    course = student_data.get("course")
    mark = student_data.get("mark")

    if name is not None and (not isinstance(name, str) or not name.strip()):
        return jsonify({"error": "Invalid name"}), 404
    if course is not None and (not isinstance(course, str) or not course.strip()):
        return jsonify({"error": "Invalid course"}), 404
    if mark is not None and (not isinstance(mark, int) or not (0 <= mark <= 100)):
        return jsonify({"error": "Invalid mark"}), 404

    updated = db.update_student(
        student_id,
        name=name.strip() if isinstance(name, str) else None,
        course=course.strip() if isinstance(course, str) else None,
        mark=mark,
    )
    return jsonify(updated), 200


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    deleted = db.delete_student(student_id)
    if not deleted:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(deleted), 200

@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks 
    return: An object with the stats (count, average, min, max)
    """
    students = db.get_all_students()
    marks = [student["mark"] for student in students if student.get("mark") is not None]

    if not marks:
        return jsonify({
            "count": 0,
            "average": 0,
            "min": None,
            "max": None
        }), 200

    return jsonify({
        "count": len(marks),
        "average": sum(marks) / len(marks),
        "min": min(marks),
        "max": max(marks)
    }), 200

@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)