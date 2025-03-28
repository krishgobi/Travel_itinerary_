from flask import Flask, render_template, request
import google.generativeai as genai
import config

app = Flask(__name__)

# Configure Gemini API Key
genai.configure(api_key=config.GEMINI_API_KEY)

def generate_itinerary(from_location, destination, days, interests, transport, activities):
    prompt = f"""
    Create a {days}-day travel itinerary from {from_location} to {destination}. 
    Preferences:
    - Interests: {interests}
    - Activities: {activities} (e.g., Food, Culture, Games, Temples, Party)
    - Preferred Transport: {transport}

    The itinerary should include:
    - Best travel options from {from_location} to {destination} based on {transport}
    - Day-wise places to visit and things to do
    - Local food recommendations
    - Cultural insights and tips
    - Any events, festivals, or experiences happening during travel dates
    """

    model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
    response = model.generate_content([prompt])

    return response.text if response and response.text else "Error: Could not generate itinerary."

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        from_location = request.form["from_location"]
        destination = request.form["destination"]
        days = request.form["days"]
        interests = request.form["interests"]
        transport = request.form["transport"]
        activities = request.form.getlist("activities")  # Get multiple selected values
        
        # Convert list to comma-separated string
        activities_str = ", ".join(activities)

        itinerary = generate_itinerary(from_location, destination, days, interests, transport, activities_str)
        
        return render_template("itinerary.html", itinerary=itinerary, destination=destination)
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
