import streamlit as st
import requests
import json
import base64
import io
from PIL import Image

# Configure Streamlit page layout
st.set_page_config(
    page_title="TTB Label Compliance Verifier Prototype",
    layout="wide"
)

# =========================================================================
# HEADER & PROTOTYPE OVERVIEW
# =========================================================================
st.title("Alcoholic Beverage Label Compliance Verifier")

st.info(
    "**Prototype Notice:** This is a prototype for the Alcohol and Tobacco Tax and Trade Bureau (TTB). "
    "The core idea is to configure an automated inspection payload with the front and back images of an alcoholic beverage label alongside its declared metadata.\n\n"
    "**How to use:**\n"
    "1. **Select Category:** Choose whether the beverage is a *Distilled Spirit*, *Wine*, or *Malt Beverage (Beer)*.\n"
    "2. **Select Subclass & Net Contents:** The application dynamically restricts available subclasses and standard container sizes according to TTB statutory standards.\n"
    "3. **Fill Metadata & Attach Images:** Provide application manifest details (with separate fields for Manufacturer and Location) and upload front/back label images.\n"
    "4. **Execute Verification:** The payload is sent to local `llama-server` (`gemma4:12b`) via port 8080 to evaluate label compliance."
)

# Endpoint URL for llama-server OpenAI-compatible chat API
LLAMA_SERVER_URL = "http://host.docker.internal:8080/v1/chat/completions"

# =========================================================================
# REGULATORY TAXONOMY MAP (27 CFR Parts 4, 5, 7)
# =========================================================================
GUIDELINE_MAP = {
    "4.1": {
        "section_name": "Distilled Spirits",
        "cfr_part": "27 CFR Part 5",
        "class_types": [
            "Vodka", "Grain Neutral Spirits", "Grain Spirits", "Neutral Spirits",
            "Bourbon Whisky", "Straight Bourbon Whisky", "Rye Whisky", "Straight Rye Whisky",
            "Wheat Whisky", "Straight Wheat Whisky", "Malt Whisky", "Peanut Butter Whiskey", "Straight Malt Whisky",
            "Rye Malt Whisky", "Straight Rye Malt Whisky", "Corn Whisky", "Straight Corn Whisky",
            "Tennessee Whisky", "Blended Whisky", "Canadian Whisky", "Scotch Whisky",
            "Irish Whisky", "American Single Malt Whisky", "Light Whisky", "Spirit Whisky",
            "Gin", "Distilled Gin", "London Dry Gin", "Plymouth Gin", "Flavored Gin",
            "Rum", "Puerto Rican Rum", "Jamaican Rum", "Agricultural Rum", "Flavored Rum",
            "Tequila", "Tequila Blanco", "Tequila Silver", "Tequila Joven", "Tequila Reposado",
            "Tequila Añejo", "Tequila Extra Añejo", "Mezcal", "Mezcal Joven", "Mezcal Reposado",
            "Mezcal Añejo", "Brandy", "Grape Brandy", "Pisco", "Cognac", "Armagnac",
            "Applejack", "Apple Brandy", "Fruit Brandy", "Grappa", "Pomace Brandy",
            "Flavored Brandy", "Calvados", "Kirsch", "Slivovitz", "Liqueur", "Cordial",
            "Triple Sec", "Amaretto", "Schnapps", "Coffee Liqueur", "Cream Liqueur",
            "Sambuca", "Anisette", "Ouzo", "Crème de Menthe", "Crème de Cacao",
            "Crème de Cassis", "Rock and Rye", "Flavored Vodka", "Flavored Tequila",
            "Flavored Whisky", "Prepared Cocktails", "Margarita", "Martini", "Manhattan",
            "Old Fashioned", "Daiquiri", "Distilled Spirits Specialty", "Agave Spirits",
            "Alcohol", "Whisky", "Flavored Spirits", "Specialty Spirits", "Cocktails",
            "Imitation Spirits"
        ],
        "mandatory_checks": [
            "brand_name", "class_type", "alcohol_content", 
            "net_contents", "company_name", "location_address", "government_warning"
        ],
        "net_content_allowed_values": ["50 mL", "100 mL", "200 mL", "375 mL", "750 mL", "1 L", "1.75 L"]
    },
    "4.2": {
        "section_name": "Wine",
        "cfr_part": "27 CFR Part 4",
        "class_types": [
            "Cabernet Sauvignon", "Wine", "agricultural wine", "amber wine",
            "american champagne", "amontillado sherry", "angelico", "aperitif wine",
            "apple wine", "berry wine", "blackberry wine", "blueberry wine", "brut",
            "california champagne", "carbonated grape wine", "carbonated wine", "cava",
            "champagne", "cherry wine", "cider", "citrus wine", "cyser", "demi-sec",
            "dessert wine", "dry vermouth", "extra dry", "fino sherry", "flavored wine",
            "fortified wine", "fruit wine", "grape wine", "grapefruit wine", "honey wine",
            "imitation wine", "light wine", "madeira", "malmsey madeira", "manzanilla sherry",
            "marsala", "mead", "melomel", "muscatel", "oloroso sherry", "orange wine",
            "pedro ximénez sherry", "perry", "pink wine", "plum wine", "port", "prosecco",
            "pyment", "red wine", "retsina", "retsina wine", "rice wine", "rosé wine",
            "ruby port", "sake", "sec", "sherry", "sparkling grape wine", "sparkling wine",
            "spumante", "substandard wine", "sweet vermouth", "table wine", "tawny port",
            "tokay", "vermouth", "vintage port", "white wine", "wine specialty"
        ],
        "mandatory_checks": [
            "brand_name", "class_type", "alcohol_content", "net_contents", 
            "company_name", "location_address", "government_warning"
        ],
        "net_content_allowed_values": ["187 mL", "375 mL", "500 mL", "750 mL", "1.5 L", "3 L"]
    },
    "4.3": {
        "section_name": "Malt Beverages (Beer)",
        "cfr_part": "27 CFR Part 7",
        "class_types": [
            "Beer", "Draft Beer", "Draught Beer", "Lager", "Pale Lager", "Pilsner",
            "Pilsen", "Light Lager", "Dark Lager", "Bock", "Doppelbock", "Eisbock",
            "Vienna Lager", "Märzen", "Oktoberfest", "Rauchbier", "Ale", "Pale Ale",
            "India Pale Ale", "IPA", "New England IPA", "Session IPA", "Imperial IPA",
            "Double IPA", "American Pale Ale", "Amber Ale", "Red Ale", "Brown Ale",
            "Blonde Ale", "Golden Ale", "Cream Ale", "Lo-Cal Ale", "Wheat Ale", "Hefeweizen",
            "Weissbier", "Dunkelweizen", "Weizenbock", "Witbier", "Saison",
            "Farmhouse Ale", "Biere de Garde", "Sour Ale", "Gose", "Berliner Weisse",
            "Lambic", "Gueuze", "Fruit Lambic", "Porter", "Robust Porter", "Baltic Porter",
            "Stout", "Dry Stout", "Irish Stout", "Milk Stout", "Oatmeal Stout",
            "Imperial Stout", "Russian Imperial Stout", "Barleywine", "Wheatwine",
            "Rye Ale", "Scotch Ale", "Wee Heavy", "Malt Liquor", "Flavored Malt Beverage",
            "FMB", "Hard Seltzer", "Hard Cider", "Hard Lemonade", "Non-Alcoholic Malt Beverage",
            "Cereal Beverage", "Malt Beverage", "Near Beer"
        ],
        "mandatory_checks": [
            "brand_name", "class_type", "alcohol_content", "net_contents", 
            "company_name", "location_address", "government_warning"
        ],
        "net_content_allowed_values": ["12 fl. oz.", "16 fl. oz.", "1 Pint", "22 fl. oz."]
    }
}

# =========================================================================
# UI LAYOUT: INPUT CONTROLS & AUDIT OUTPUT
# =========================================================================
col_input, col_output = st.columns([1, 1], gap="large")

with col_input:
    st.subheader("1. Classification & Subclass Selection")
    
    category_options = {key: data["section_name"] for key, data in GUIDELINE_MAP.items()}
    selected_sec_key = st.selectbox(
        "Select Beverage Category", 
        options=list(category_options.keys()), 
        format_func=lambda x: category_options[x]
    )
    
    active_guideline = GUIDELINE_MAP[selected_sec_key]
    
    selected_subclass = st.selectbox(
        "Select Subclass Designation", 
        options=active_guideline["class_types"]
    )
    
    selected_net_contents = st.selectbox(
        "Select Net Contents Size", 
        options=active_guideline["net_content_allowed_values"]
    )
    
    contains_sulfites = False
    if selected_sec_key == "4.2":
        contains_sulfites = st.checkbox(
            "Product contains 10+ ppm sulfites (Requires 'Contains Sulfites' on label)",
            value=True,
            help="Uncheck if this wine is naturally low in sulfites (<10 ppm) and exempt from TTB sulfite labeling rules."
        )

    st.write("---")
    st.subheader("2. Application Manifest Details")
    app_id = st.text_input("Application ID", value="COLA-2026-001")
    brand_name = st.text_input("Brand Name", value="DON Q")
    alcohol_content = st.text_input("Alcohol Content", value="40% Alc./Vol.")
    company_name = st.text_input("Company / Manufacturer Name", value="DESTILERIA SERRALLES, INC.")
    location_address = st.text_input("Bottler / Producer Location", value="PONCE, PUERTO RICO")
    
    st.write("---")
    st.subheader("3. Label Images")
    front_img = st.file_uploader("Upload Front Label Image", type=["jpg", "jpeg", "png", "webp"])
    back_img = st.file_uploader("Upload Back Label Image", type=["jpg", "jpeg", "png", "webp"])
    
    if front_img or back_img:
        preview_col1, preview_col2 = st.columns(2)
        with preview_col1:
            if front_img:
                st.image(front_img, caption="Front Label Preview", use_container_width=True)
        with preview_col2:
            if back_img:
                st.image(back_img, caption="Back Label Preview", use_container_width=True)

    submit_button = st.button("Verify Label Compliance", type="primary", use_container_width=True)

with col_output:
    st.subheader("Verification Results")
    placeholder = st.empty()
    placeholder.info("Fill out the metadata options, attach front and back label images, and click **Verify Label Compliance**.")

# =========================================================================
# EXECUTION & LLAMA-SERVER INVOCATION
# =========================================================================
if submit_button:
    if not (front_img or back_img):
        st.error("Please upload at least one label image to perform the compliance audit.")
    else:
        with col_output:
            st.info(f"Auditing label payload via llama-server for {active_guideline['section_name']} ({selected_subclass})...")
            
            # Format image elements according to OpenAI Multimodal schema
            user_content = []

            for file in [front_img, back_img]:
                if file is not None:
                    file.seek(0)
                    img = Image.open(file)
                    
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    
                    # 1280px maintains resolution for text reading while keeping token counts manageable
                    img.thumbnail((1280, 1280))
                    
                    buffered = io.BytesIO()
                    img.save(buffered, format="JPEG", quality=85)
                    encoded_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
                    
                    user_content.append({
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_str}"
                        }
                    })

            # Conditional Sulfite Instructions
            sulfite_instruction = ""
            if selected_sec_key == "4.2":
                if contains_sulfites:
                    sulfite_instruction = "- MANDATORY: Verify that 'Contains Sulfites' (or equivalent statutory wording) is clearly printed on the label."
                else:
                    sulfite_instruction = "- NOTE: Applicant declared low/no sulfites (<10 ppm). Do NOT flag missing 'Contains Sulfites' text as a violation."

            # Construct structured verification text
            prompt_text = f"""
            You are an expert TTB label compliance auditor testing compliance against {active_guideline['cfr_part']}.

            PAYLOAD MANIFEST METADATA:
            - Primary Category: {active_guideline['section_name']} ({active_guideline['cfr_part']})
            - Declared Subclass: {selected_subclass}
            - Declared Net Contents: {selected_net_contents}
            - Application ID: {app_id}
            - Brand Name: {brand_name}
            - Alcohol Content: {alcohol_content}
            - Company / Manufacturer Name: {company_name}
            - Producer / Bottler Location: {location_address}
            - Declared Sulfite Status: {'Contains 10+ ppm Sulfites' if contains_sulfites else 'Exempt / Low Sulfites (<10 ppm)' if selected_sec_key == '4.2' else 'N/A'}

            REGULATORY MANDATES:
            - Mandatory Checks Required for Category: {json.dumps(active_guideline['mandatory_checks'])}
            - Permitted Standard Container Sizes: {json.dumps(active_guideline['net_content_allowed_values'])}

            AUDIT INSTRUCTIONS:
            1. Verify whether the declared Subclass ({selected_subclass}) accurately matches the product description printed on the front or back label images.
            2. Verify that the Net Contents ({selected_net_contents}) matches the printed label text and complies with statutory volume standards..
            3. Verify that the Company/Manufacturer Name ({company_name}) and Producer/Bottler Location ({location_address}) match the mandatory name and address statement printed on the label.
            4. Check that mandatory elements under {active_guideline['cfr_part']} (e.g. Government Warning statement, alcohol percentage, manufacturer name, location) are explicitly visible on the label images.
            {sulfite_instruction}
            5. Detail any discrepancies, missing mandatory regulatory elements, or formatting non-conformities clearly.
            """

            # Append the prompt text to the user content array
            user_content.append({
                "type": "text",
                "text": prompt_text.strip()
            })

            # Construct OpenAI-formatted payload expected by llama-server
            payload = {
                "messages": [
                    {
                        "role": "user",
                        "content": user_content
                    }
                ],
                "stream": True,
                "temperature": 0.2,
                "max_tokens": -1
            }

            try:
                response = requests.post(LLAMA_SERVER_URL, json=payload, stream=True, timeout=300)
                response.raise_for_status()

                output_text = ""
                res_placeholder = st.empty()

                # Process Server-Sent Events (SSE) from OpenAI compatible stream
                for line in response.iter_lines():
                    if line:
                        line_str = line.decode("utf-8").strip()
                        if line_str.startswith("data: "):
                            data_content = line_str[6:]
                            if data_content == "[DONE]":
                                break
                            try:
                                data = json.loads(data_content)
                                delta = data["choices"][0]["delta"]
                                content_chunk = delta.get("content")
                                if content_chunk:
                                    output_text += content_chunk
                                    res_placeholder.markdown(output_text + "▌")
                            except json.JSONDecodeError:
                                continue
                
                # Final render without streaming cursor
                res_placeholder.markdown(output_text)

            except requests.exceptions.Timeout:
                st.error("The request timed out after 5 minutes. Check model complexity or local GPU/Metal load.")
            except requests.exceptions.ConnectionError:
                st.error(f"Could not connect to llama-server at {LLAMA_SERVER_URL}. Verify `./llama-server` is running on port 8080.")
            except requests.exceptions.RequestException as e:
                st.error(f"Error communicating with llama-server: {e}")