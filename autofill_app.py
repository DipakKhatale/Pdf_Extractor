from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    df = pd.read_excel("extracted_resumes.xlsx")
    data = df.to_dict(orient='records')
    return render_template("index.html", data=data)

@app.route("/submit", methods=["POST"])
def submit():
    print("Received Form Data:", request.form)
    return "✅ Form submitted successfully!"

if __name__ == "__main__":
    app.run(debug=True)
