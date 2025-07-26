import json
import requests
import google.generativeai as genai
import os

# Configure Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "your-gemini-api-key")
genai.configure(api_key=GOOGLE_API_KEY)

def extract_civic_signal(text):
    prompt = f"""
Given the following news article or social media post, extract ONLY IF it is related to any of these civic event types or topics:

INFRASTRUCTURE & CIVIC: flood, waterlogging, drainage, sewerage, water supply, water crisis, traffic, traffic jam, congestion, road closure, road work, potholes, power cut, electricity outage, load shedding, transformer blast, garbage, waste management, garbage collection, landfill, street lights, street lighting, dark streets, footpath, sidewalk, pedestrian walkway, public toilets, sanitation, hygiene

TRANSPORT & MOBILITY: bus, BMTC, public transport, bus strike, bus breakdown, metro, BMRCL, Namma Metro, metro station, metro construction, auto rickshaw, taxi, cab, ride sharing, parking, parking space, parking violation, towing, accident, road accident, traffic accident, collision, ambulance, emergency vehicle, emergency response

WEATHER & NATURAL: rain, heavy rain, monsoon, rainfall, storm, thunderstorm, lightning, wind, heat wave, temperature, weather alert, air quality, pollution, smog, dust, tree fall, uprooted tree, broken branches

GOVERNMENT & ADMIN: BBMP, Bruhat Bengaluru Mahanagara Palike, ward, corporator, mayor, commissioner, complaint, grievance, helpline, citizen complaint, budget, funds, allocation, development work, election, voting, polling booth

PUBLIC SERVICES: hospital, medical emergency, health, school, college, education, exam, police, law enforcement, crime, theft, fire, fire station, fire emergency, postal service, courier, delivery

EVENTS & GATHERINGS: protest, demonstration, rally, march, festival, celebration, cultural event, flash mob, street performance, sports event, marathon, tournament, concert, music, entertainment

TECHNOLOGY & DIGITAL: internet, broadband, connectivity issues, mobile network, signal, telecom, digital payment, UPI, cashless, app, mobile app, government app, smart city, digital transformation

BUSINESS & ECONOMY: market, shopping, retail, business, restaurant, food, delivery, food safety, real estate, property, construction, startup, technology, innovation, employment, job, unemployment

COMMUNITY & SOCIAL: neighborhood, community, residents, senior citizens, children, women, migrant workers, labor, workers, NGO, volunteer, social work, charity, donation, relief

ENVIRONMENTAL: lake, water body, pollution, park, garden, green space, wildlife, animals, stray dogs, noise pollution, sound, plastic ban, environment

EMERGENCY & CRISIS: emergency, crisis, disaster, evacuation, rescue, relief, lockdown, curfew, restrictions, pandemic, COVID, health crisis, security, threat, alert

LOCATIONS: Koramangala, Indiranagar, HSR Layout, Whitefield, Electronic City, Marathahalli, Malleswaram, Basavanagudi, Jayanagar, Hebbal, Yeshwanthpur, Peenya, Airport Road, Old Airport Road, Hosur Road

If the post is not related to any of these, return null for all fields.

Extract:
1. Type of event (e.g., traffic, flood, power cut, etc.)
2. Location (specific area or landmark)
3. Severity level (low, moderate, high)
4. Actionable advice (if any)

Text:
{text}

Return your answer as a JSON object with keys: type, location, severity, advice.
If any field is missing or not found, use null.
"""
    
    try:
        # Use Gemini Pro model
        model = genai.GenerativeModel('gemini-1.0-pro')
        response = model.generate_content(prompt)
        
        result_text = response.text
        # Extract JSON from response
        try:
            # Find JSON object in the response
            start_idx = result_text.find('{')
            end_idx = result_text.rfind('}') + 1
            if start_idx != -1 and end_idx != 0:
                json_str = result_text[start_idx:end_idx]
                structured = json.loads(json_str)
            else:
                structured = {"type": None, "location": None, "severity": None, "advice": None}
        except json.JSONDecodeError:
            structured = {"type": None, "location": None, "severity": None, "advice": None}
            
    except Exception as e:
        print(f"Gemini API error: {str(e)}")
        structured = {"type": None, "location": None, "severity": None, "advice": None}
    
    return structured

def process_event(event_data):
    """
    Process an event through the LLM and return structured data
    """
    text = event_data.get('text', '')
    if not text:
        return None
    
    # Extract civic signals using LLM
    structured_data = extract_civic_signal(text)
    
    # Combine original event data with structured extraction
    result = {
        "original_event": event_data,
        "extracted_data": structured_data,
        "timestamp": event_data.get('timestamp', None)
    }
    
    return result 