"""
PlagScan Flask Web Application.

Routes:
- GET /: Main Dashboard & Document Comparison Input Form
- POST /compare: Runs document comparison, benchmarking, and renders results
- POST /api/compare: JSON API for comparison results
- GET /samples/<sample_id>: Returns pre-loaded sample documents for quick demo
- GET /health: Healthcheck endpoint
"""

import os
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_file
from config import Config
from utils.file_handler import process_uploaded_document
from services.comparison_service import compare_documents
from services.benchmark_service import run_algorithm_benchmark

app = Flask(__name__)
app.config.from_object(Config)

# Sample documents for easy viva demo and testing
SAMPLE_DOCUMENTS = {
    "identical": {
        "title": "Identical Documents (100% Similarity)",
        "doc1": "The Knuth-Morris-Pratt algorithm searches for occurrences of a word within a main text by employing the observation that when a mismatch occurs, the word itself embodies sufficient information to determine where the next match could begin.",
        "doc2": "The Knuth-Morris-Pratt algorithm searches for occurrences of a word within a main text by employing the observation that when a mismatch occurs, the word itself embodies sufficient information to determine where the next match could begin."
    },
    "partial": {
        "title": "Partially Modified Text (Approx 50% Similarity)",
        "doc1": "Design and Analysis of Algorithms is a fundamental core subject in computer science. It teaches efficiency, time complexity, and asymptotic notations like Big O, Theta, and Omega. Dynamic programming and greedy paradigms solve complex optimization problems.",
        "doc2": "In modern engineering, Design and Analysis of Algorithms is a fundamental core subject in computer science. Students study software development practices and machine learning architectures alongside data structures."
    },
    "different": {
        "title": "Completely Different Documents (0% Similarity)",
        "doc1": "Photosynthesis is the biological process by which green plants and certain organisms transform light energy into chemical energy stored in glucose.",
        "doc2": "Relational databases use structured query language to manage records through relational tables, foreign key constraints, and normalized schemas."
    }
}


@app.route("/", methods=["GET"])
def index():
    """Renders the main homepage dashboard."""
    return render_template("index.html", samples=SAMPLE_DOCUMENTS)


@app.route("/compare", methods=["POST"])
def compare():
    """
    Handles comparison submission from web UI form.
    Validates uploaded files / text inputs and runs comparison service.
    """
    doc1_file = request.files.get("doc1_file")
    doc2_file = request.files.get("doc2_file")
    doc1_text_raw = request.form.get("doc1_text", "")
    doc2_text_raw = request.form.get("doc2_text", "")
    algorithm = request.form.get("algorithm", "kmp")

    try:
        shingle_size = int(request.form.get("shingle_size", 5))
        if shingle_size < 1 or shingle_size > 20:
            shingle_size = 5
    except ValueError:
        shingle_size = 5

    # Process Document 1
    doc1_text, doc1_name, err1 = process_uploaded_document(doc1_file, doc1_text_raw)
    if err1:
        flash(f"Document 1 Error: {err1}", "danger")
        return redirect(url_for("index"))

    # Process Document 2
    doc2_text, doc2_name, err2 = process_uploaded_document(doc2_file, doc2_text_raw)
    if err2:
        flash(f"Document 2 Error: {err2}", "danger")
        return redirect(url_for("index"))

    # Run primary comparison
    result = compare_documents(
        doc1_text=doc1_text,
        doc2_text=doc2_text,
        algorithm_key=algorithm,
        shingle_size=shingle_size
    )

    # Run fair algorithm benchmark on identical inputs
    benchmark_data = run_algorithm_benchmark(
        doc1_text=doc1_text,
        doc2_text=doc2_text,
        shingle_size=shingle_size
    )

    result["doc1_name"] = doc1_name
    result["doc2_name"] = doc2_name
    result["benchmark"] = benchmark_data

    return render_template("result.html", result=result)


@app.route("/api/compare", methods=["POST"])
def api_compare():
    """JSON API endpoint for programmatic document comparison."""
    data = request.get_json(silent=True) or {}
    doc1_text = data.get("doc1_text", "")
    doc2_text = data.get("doc2_text", "")
    algorithm = data.get("algorithm", "kmp")
    shingle_size = int(data.get("shingle_size", 5))

    if not doc1_text.strip() or not doc2_text.strip():
        return jsonify({"error": "Both doc1_text and doc2_text must be provided and non-empty."}), 400

    result = compare_documents(doc1_text, doc2_text, algorithm_key=algorithm, shingle_size=shingle_size)
    benchmark = run_algorithm_benchmark(doc1_text, doc2_text, shingle_size=shingle_size)
    result["benchmark"] = benchmark

    return jsonify({"success": True, "data": result})


@app.route("/samples/<sample_id>", methods=["GET"])
def get_sample(sample_id):
    """Returns sample text for quick 1-click viva demonstrations."""
    if sample_id in SAMPLE_DOCUMENTS:
        return jsonify(SAMPLE_DOCUMENTS[sample_id])
    return jsonify({"error": "Sample not found"}), 404


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "PlagScan"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
