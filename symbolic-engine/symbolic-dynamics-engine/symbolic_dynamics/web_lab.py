from flask import Flask, jsonify
from symbolic_dynamics.algorithms.pipeline import SFTPipeline

app = Flask(__name__)

@app.route("/entropy")
def entropy():
    pipe = SFTPipeline(["0","1"],["000"])
    return jsonify({"entropy": pipe.entropy()})

@app.route("/")
def index():
    return """
    <h1>Symbolic Dynamics Lab</h1>
    <p>Visit /entropy to compute entropy.</p>
    """

if __name__ == "__main__":
    app.run(port=5000)
