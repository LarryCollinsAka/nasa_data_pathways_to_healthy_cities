# NASA Hackathon 2025 –  Data Pathways to Healthy Cities and Human Settlements

### Challenge Statement
Climate change brings about new complexities to consider for maintaining the wellbeing of society and the environment in cities. Natural resources, ecosystems, and existing infrastructure all must be monitored to ensure human quality of life remains high. Your challenge is to demonstrate how an urban planner can use NASA Earth observation data to develop smart strategies for city growth that maintain both the wellbeing of people and the environment.

###  Challenge
Use NASA Earth observation data to help urban planners design smart, sustainable strategies for city growth while maintaining human and environmental wellbeing.

---
### Methodology
Based on the Challenge Statement, and making our solution inclusive, 6 major cities, Yaoundé, Lagos, Mumbai, Douala, Pune and Abuja are case studies here. 
To address the challenge problem carefully, we need to step back and identify the cross‑cutting, climate‑driven challenges that are pressing across all six cities (Douala, Yaoundé, Lagos, Abuja, Mumbai, Pune). This way, we know we’re solving the root problems rather than just symptoms.

To indentify the challenges and complexities of climate change and map across all six cities, internet researches were carried out and a liitle yes or no survey was used to get answers from citizens particularly in Yaounde and Douala. The questions were on four categories

- Waste Management and Sanitation
- Water and Flooding
- Green Spaces and Urban Heat
- Quality of Air and Health
 
### Narrowing Down to Three Core Challenges

From the four categories identified across all six cities, we applied prioritization to select the three most pressing issues that are both **climate-driven** and **actionable with NASA Earth observation data**:

1. **Water and Flooding** → Douala (case study)  
2. **Green Spaces and Urban Heat** → Mumbai (case study)  
3. **Waste Management and Land Use** → Lagos (case study)  

These three were chosen because:
- They are **cross-cutting**: each affects health, infrastructure, and equity.  
- They are **data-rich**: NASA provides high-quality, open datasets for each.  
- They are **locally urgent**: confirmed by survey responses and city-level research.  

---


### Problem Exploration – The 5 Whys

To ensure our solution addresses root causes rather than symptoms, we applied the **5 Whys methodology** to three pressing urban challenges. This structured brainstorming shows how we arrived at our focus areas and data choices.

### Case Studies
We did some research across 6 cities Douala, Yaounde, Lagos, Mumbai, Abuja and Pune. We 

#### 1. Flooding in Douala
- **Symptom:** Neighborhoods regularly submerge during heavy rains.  
- **Why 1:** Drainage systems are overwhelmed.  
- **Why 2:** Urban expansion encroaches on floodplains.  
- **Why 3:** Zoning and infrastructure are not informed by risk maps.  
- **Why 4:** High-resolution precipitation/elevation data isn’t integrated in planning.  
- **Why 5:** Satellite-based monitoring and predictive analytics are underused.  
- **Problem Statement:** Douala faces recurrent flooding due to unplanned growth and inadequate drainage; integrating NASA precipitation and elevation data is essential to anticipate and mitigate risk.

#### 2. Heat Stress in Mumbai
- **Symptom:** Intensifying heatwaves cause health risks and discomfort.  
- **Why 1:** Dense built-up areas trap heat (urban heat islands).  
- **Why 2:** Insufficient green cover and reflective surfaces.  
- **Why 3:** Planning lacks real-time thermal insights.  
- **Why 4:** Satellite-derived LST and vegetation indices are not operationalized.  
- **Why 5:** Data-to-action pipelines for cooling interventions are missing.  
- **Problem Statement:** Mumbai’s heat stress threatens health and livability; using NASA thermal and vegetation data can guide targeted cooling and greening.

#### 3. Waste & Land Use in Lagos
- **Symptom:** Unmanaged waste and rapid land-use change degrade environments.  
- **Why 1:** Population growth outpaces waste systems.  
- **Why 2:** Informal settlements expand without infrastructure.  
- **Why 3:** Authorities lack up-to-date land cover and activity visibility.  
- **Why 4:** Satellite imagery and nighttime lights are not systematically applied.  
- **Why 5:** Integrated geospatial monitoring is missing in day-to-day decisions.  
- **Problem Statement:** Lagos struggles with waste and unplanned land use; NASA land cover and nighttime lights data provide the visibility needed for smarter interventions.

---


###  Focus Area
- Case study: **Douala & Yaoundé (Cameroon)**
- Urban challenges: waste management, flooding, air quality, lack of green spaces

###  Project Idea
Build a **data-driven platform** that:
- Maps waste hotspots using satellite & community data
- Monitors air quality and flooding risks
- Supports planning for green spaces and infrastructure
- Engages communities through reporting + AI insights

###  NASA Data Sources
- **Landsat** – urban growth & land use
- **MODIS** – air quality & climate indicators
- **GRACE** – water & flooding risks
- **VIIRS** – population density (nighttime lights)

###  Tech Stack
- **Backend**: Python (FastAPI/Django, Pandas, GeoPandas, NASA APIs)
- **Frontend**: React (interactive dashboards, maps)
- **Visualization**: Mapbox / Leaflet / Power BI
- **Hosting**: AWS (S3 + CloudFront)

###  Repository Structure

