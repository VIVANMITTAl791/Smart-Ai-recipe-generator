import streamlit as st
from openai import OpenAI
import os
import time
import io
import re
import urllib.parse
from datetime import datetime
from dotenv import load_dotenv

# .env file se API keys load karne ke liye
load_dotenv()

# System Engine Constants
TEXT_MODEL = "llama-3.3-70b-versatile"

# Groq API Client setup
api_key = os.environ.get("GROQ_API_KEY") or os.environ.get("XAI_API_KEY")
client = OpenAI(
    api_key=api_key,      
    base_url="https://api.groq.com/openai/v1",  
)

# Custom CSS for Premium Premium Kawaii Design Theme Layout Structure
def apply_cute_styles():
    st.markdown("""
    <style>
        /* Light Contrast Soft Canvas Styling */
        .stApp {
            background-color: #FFF9F3 !important;
        }
        
        /* High Visibility Text Colors - Crystal Clear Typography */
        body, p, li, span, label, .stMarkdown, [data-testid="stMarkdownContainer"] p {
            color: #1E293B !important;
            font-size: 16px;
            font-weight: 500;
        }
        
        /* Premium Core Typography Header Branding Blocks */
        .main-title {
            font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif;
            color: #FF5E7E;
            font-weight: bold;
            text-align: center;
            font-size: 45px;
            margin-bottom: 0px;
            text-shadow: 2px 2px #FFE5EC;
        }
        .sub-title-text {
            font-family: 'Arial', sans-serif;
            color: #5D3FD3;
            text-align: center;
            font-size: 19px;
            font-weight: bold;
            margin-bottom: 30px;
        }

        /* Sidebar Custom Scope Navigation Cardboard Layout */
        [data-testid="stSidebar"] {
            background-color: #FFE5EC !important;
            border-right: 4px dashed #FFB6C1;
        }
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] h3 {
            color: #D81B60 !important;
            font-weight: bold;
        }
        
        /* Dynamic Accent Elements for Access Cards */
        .profile-text {
            color: #1E293B !important;
            font-size: 15px;
            font-weight: bold;
            margin-bottom: 6px;
            background-color: #FFF0F2;
            padding: 8px 12px;
            border-radius: 10px;
            border-left: 4px solid #FF5E7E;
        }
        
        /* Premium Recipe Matrix Container Card */
        .recipe-card {
            background-color: #FFFFFF;
            border-radius: 28px;
            padding: 30px;
            border: 3px solid #FFB6C1;
            box-shadow: 0 8px 16px rgba(255, 182, 193, 0.2);
            margin-bottom: 25px;
        }
        .recipe-header {
            color: #D81B60;
            font-family: 'Comic Sans MS', sans-serif;
            font-size: 32px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 15px;
        }

        /* Video System Custom Fluid View Layout Box */
        .video-monitor-box {
            background-color: #FFF0F5;
            border: 3px dashed #FFB6C1;
            border-radius: 24px;
            padding: 25px;
            margin-top: 25px;
            box-shadow: 0 6px 12px rgba(255, 182, 193, 0.1);
            text-align: center;
        }
        
        /* Interactive Component Tracking Modules */
        .interactive-card {
            background-color: #FDF2F8;
            border: 2px solid #FBCFE8;
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 25px;
        }
        
        .history-item {
            background-color: #FFFFFF;
            border: 2px solid #FFB6C1;
            border-radius: 14px;
            padding: 12px;
            margin-bottom: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        }
        
        .nutrition-card {
            background-color: #E8F0FE;
            border-radius: 24px;
            padding: 20px;
            border: 2px solid #A4C2E6;
            margin-bottom: 25px;
            text-align: center;
        }

        .login-card {
            background-color: #FFFFFF;
            border-radius: 24px;
            padding: 35px;
            border: 3px solid #FFB6C1;
            max-width: 480px;
            margin: auto;
            box-shadow: 0 10px 25px rgba(0,0,0,0.06);
        }
        
        .thankyou-banner {
            text-align: center;
            font-family: 'Comic Sans MS', sans-serif;
            background: linear-gradient(135deg, #FFE5EC, #FFF0F5);
            border: 2px dashed #FF7B93;
            border-radius: 18px;
            padding: 20px;
            margin-top: 50px;
            color: #FF5E7E;
            font-size: 19px;
            font-weight: bold;
            box-shadow: 0 6px 12px rgba(255, 123, 147, 0.15);
        }

        /* Playful Cute Custom Streamlit Buttons */
        div.stButton > button {
            background-color: #FF7B93 !important;
            color: white !important;
            border-radius: 24px !important;
            border: 2px solid #FF5E7E !important;
            font-weight: bold !important;
            padding: 10px 24px !important;
            font-size: 16px !important;
            box-shadow: 0 5px 10px rgba(0,0,0,0.08) !important;
            transition: all 0.25s ease !important;
        }
        div.stButton > button:hover {
            transform: scale(1.03) translateY(-2px);
            background-color: #FF5E7E !important;
            box-shadow: 0 8px 15px rgba(255, 94, 126, 0.3) !important;
        }

        /* Custom Visual Layout Link Anchor Elements */
        .premium-video-link {
            display: inline-block;
            background-color: #FF1493 !important;
            color: white !important;
            font-size: 16px;
            font-weight: bold !important;
            padding: 14px 30px;
            border-radius: 50px;
            text-decoration: none !important;
            box-shadow: 0 4px 12px rgba(255, 20, 147, 0.3);
            transition: all 0.3s ease;
            margin-top: 12px;
        }
        .premium-video-link:hover {
            background-color: #C71585 !important;
            transform: scale(1.05) translateY(-1px);
            box-shadow: 0 6px 16px rgba(255, 20, 147, 0.4);
        }
    </style>
    """, unsafe_allow_html=True)

apply_cute_styles()

# ----------------- SESSION STATE SYSTEM ARCHITECTURE -----------------
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "input"
if "generated_recipe" not in st.session_state:
    st.session_state.generated_recipe = ""
if "recipe_name" not in st.session_state:
    st.session_state.recipe_name = "Yummy Dish"
if "selected_lang" not in st.session_state:
    st.session_state.selected_lang = "Roman Urdu/Hinglish"
if "parsed_ingredients" not in st.session_state:
    st.session_state.parsed_ingredients = []
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {"name": "", "phone": "", "avatar": None, "history": []}

# ----------------- ADVANCED DYNAMIC PORTION SCALER LOGIC -----------------
def scale_recipe_numbers(text, factor):
    if factor == 1.0:
        return text
        
    def replace_match(match):
        val = float(match.group(0))
        scaled_val = val * factor
        if scaled_val.is_integer():
            return str(int(scaled_val))
        return f"{scaled_val:.1f}"

    return re.sub(r'\b\d+(?:\.\d+)?\b', replace_match, text)

# ----------------- PARSING UTILITY PROCEDURES -----------------
def clean_and_parse_ingredients(recipe_text):
    items = []
    lines = recipe_text.split('\n')
    capture = False
    for line in lines:
        if "#Ingredients:" in line:
            capture = True
            continue
        if line.startswith('#') and capture:
            break
        if capture and line.strip():
            cleaned = re.sub(r'^[-\*\d\.\s\)\(]+', '', line).strip()
            if cleaned:
                items.append(cleaned)
    return items if items else ["Magical Spice Mix", "Love & Care"]

# ----------------- STAGE 0: DIRECT ENTRY GATEWAY -----------------
if st.session_state.logged_in_user is None:
    st.markdown("<div style='text-align: center; font-size: 65px; margin-top: 20px;'>👩‍🍳✨🍓</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-title'>Welcome to VM AI Kitchen</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title-text'>Apni details enter karke portal unlock karein! 🎀</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background-color: #E8F0FE; border: 2px dashed #A4C2E6; border-radius: 15px; padding: 15px; max-width: 450px; margin: 0 auto 20px auto; text-align: center;'>
        <b style='color: #2B6CB0; font-size: 16px;'>👶 Tot's Special Menu Alert! 🧸🍼</b><br>
        <p style='color: #1E293B; font-size: 14px; margin: 5px 0 0 0;'>
            Bacchon ke liye healthy & fun fusion recipes! 
            Ghar mein bache aaloo se banayein cute <i>Smileys</i>, ya vegetable purees se banayein colorful <i>Rainbow Parathas</i>! 🌈🥦
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='login-card'>", unsafe_allow_html=True)
    
    entry_name = st.text_input("Full Name (आपका नाम):", placeholder="e.g., Rahul Kumar")
    entry_phone = st.text_input("Phone Number (फ़ोन नंबर):", placeholder="e.g., 9876543210")
    entry_pass = st.text_input("Set Password (पासवर्ड):", type="password", placeholder="••••••••")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Unlock Kitchen Portal 🔑🚀", use_container_width=True):
        if not entry_name or not entry_phone or not entry_pass:
            st.error("Saari fields fill karna zaroori hai cutie! 📝")
        elif len(entry_phone) != 10 or not entry_phone.isdigit():
            st.error("Valid 10-digit phone number enter karein! 📱")
        else:
            st.session_state.user_profile["name"] = entry_name
            st.session_state.user_profile["phone"] = entry_phone
            st.session_state.logged_in_user = entry_phone
            st.success(f"Welcome to the kitchen, {entry_name}! Let's cook... 🎉")
            time.sleep(1)
            st.rerun()
                
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------- STATE 1: RUNTIME OPERATION AND APP KITCHEN SYSTEM -----------------
else:
    current_user_data = st.session_state.user_profile
    
    # ----------------- SIDEBAR PROFILE ACCESS & CONTROL FLOW -----------------
    with st.sidebar:
        st.markdown(f"### 👤 Profile Settings")
        
        if current_user_data.get("avatar") is not None:
            st.image(io.BytesIO(current_user_data["avatar"]), width=100, caption="My Profile pic")
        else:
            st.markdown("<div style='font-size:50px; text-align:center;'>🐱</div>", unsafe_allow_html=True)
            
        avatar_file = st.file_uploader("Change Profile Picture", type=["png", "jpg", "jpeg"])
        if avatar_file is not None:
            current_user_data["avatar"] = avatar_file.read()
            st.success("Profile photo uploaded! Refreshing...")
            time.sleep(0.5)
            st.rerun()
            
        st.markdown("#### 📝 My Details")
        st.markdown(f"<div class='profile-text'>👤 Name: {current_user_data['name']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='profile-text'>📱 Phone: {current_user_data['phone']}</div>", unsafe_allow_html=True)
        
        if st.button("Logout 🚪", use_container_width=True):
            st.session_state.logged_in_user = None
            st.session_state.current_page = "input"
            st.rerun()
            
        st.markdown("<hr style='border: 1px dashed #FFB6C1;'>", unsafe_allow_html=True)
        
        st.markdown("### 🕒 My Saved History")
        user_history = current_user_data["history"]
        
        if not user_history:
            st.write("Abhi aapki koi purani history nahi hai. 🐇")
        else:
            if st.button("Clear My History 🗑️"):
                current_user_data["history"] = []
                st.rerun()
                
            for idx, item in enumerate(reversed(user_history)):
                actual_idx = len(user_history) - 1 - idx
                st.markdown(f"""
                <div class='history-item'>
                    <small style='color: #475569;'>📅 {item['timestamp']}</small><br>
                    <b style='color: #5D3FD3;'>🍔 {item['recipe_name']}</b><br>
                    <small style='color: #1E293B;'>Query/Items: {item['ingredients']}</small>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"View Again 📂", key=f"hist_btn_{actual_idx}"):
                    st.session_state.generated_recipe = item['recipe_text']
                    st.session_state.recipe_name = item['recipe_name']
                    st.session_state.parsed_ingredients = clean_and_parse_ingredients(item['recipe_text'])
                    st.session_state.current_page = "recipe"
                    st.rerun()

    # ----------------- SCREEN 1: KITCHEN INPUT BOARD -----------------
    if st.session_state.current_page == "input":
        st.markdown("<div style='text-align: center; font-size: 65px; margin-bottom: -15px;'>🧁👩‍🍳🥕</div>", unsafe_allow_html=True)
        st.markdown("<div class='main-title'>VM AI Kitchen ✨</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='sub-title-text'>Welcome back, {current_user_data['name']}! Let's cook! 🥟🍓</div>", unsafe_allow_html=True)

        # FIXED HINGLISH LABELS HERE (REMOVED HINDI CHARACTERS)
        search_mode = st.radio(
            "Method choose karein (मेथड चुनें):",
            ["🎒 Fridge Ingredients (Hinglish: Bache hue saamaan se banayein)", "🍲 Direct Dish Name (Hinglish: Seede dish ka naam search karein)"],
            horizontal=True
        )

        col1, col2 = st.columns(2)
        with col1:
            if "Fridge" in search_mode:
                user_input_query = st.text_input(
                    "🎒 Fridge mein kya bacha hai?", 
                    placeholder="e.g., Aloo, Pyaaz, Bread, Tamatar"
                )
                ai_mode_context = f"Find or create a clever matching recipe using strictly these leftover ingredients: {user_input_query}."
            else:
                user_input_query = st.text_input(
                    "🍲 Kis dish ki recipe search karni hai?", 
                    placeholder="e.g., Shahi Paneer, Hakka Noodles, Momos"
                )
                ai_mode_context = f"Create a comprehensive step-by-step masterclass recipe tutorial specifically for the dish: '{user_input_query}'."

            meal_type = st.selectbox(
                "⏰ Time category:",
                ["Breakfast (Nashta 🥞)", "Lunch (Yummy Khana 🍱)", "Dinner (Special Raat 🍲)", "Quick Snack (Munchies 🍿)"]
            )
            recipe_lang = st.selectbox(
                "🌐 Choose Recipe Language (भाषा चुनें):",
                ["Roman Urdu/Hinglish", "Hindi (हिंदी)", "English"]
            )
            st.session_state.selected_lang = recipe_lang

        with col2:
            diet_preference = st.radio(
                "🌱 Diet Type Choice:",
                ["Pure Veg 🥬", "Non-Veg 🍗", "Anything works 😋"]
            )
            cooking_level = st.select_slider(
                "🧸 Cooking Level Option:",
                options=["Baby Chef 👶", "Smart Cook 🤓", "Master Chef 👑"]
            )

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Magic Recipe Banayein! ✨💖", use_container_width=True):
            if not user_input_query:
                st.warning("Pehle kuch input daaliye cutie! 🐹")
            else:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for percent_complete in range(100):
                    time.sleep(0.004)
                    progress_bar.progress(percent_complete + 1)
                    if percent_complete < 30:
                        status_text.text("🌈 Mixing magical spices... 🧂")
                    elif percent_complete < 60:
                        status_text.text("🐼 Asking pandas for chef tips... 🐾")
                    elif percent_complete < 90:
                        status_text.text("🔥 Baking with love... 🧁")
                    else:
                        status_text.text("Done! Opening New Page... 🎉")

                try:
                    prompt = f"""
                    You are a super cute cartoon masterchef. 
                    - Operational Search Context: {ai_mode_context}
                    - Category: {meal_type}
                    - Choice: {diet_preference}
                    - Difficulty: {cooking_level}
                    
                    CRITICAL METRIC LAW: You MUST design the recipe ingredients quantity numbers based EXACTLY on 2 Servings standard. Use regular global digits for quantities (e.g. 2 cups, 4 potatoes, 100 grams).
                    
                    CRITICAL LANGUAGE SYSTEM INSTRUCTION:
                    The user has explicitly selected the language option: "{st.session_state.selected_lang}". You must obey these language laws perfectly:
                    1. If "English" is selected -> You MUST write the ENTIRE response strictly in pure grammatical English text only.
                    2. If "Hindi (हिंदी)" is selected -> Write 100% in pure Devanagari script text only.
                    3. If "Roman Urdu/Hinglish" is selected -> Use English alphabets but conversational Hindi/Urdu speech terms.
                    
                    STRICT NUMBER RULE: Do NOT use Devnagari numerical symbols like '१, २, ३'. Always use regular numeric characters like '120, 2, 5, 10'.

                    Format the output strictly and divide sections exactly using these tags:
                    
                    #RecipeName: [Cool short dish name here]
                    
                    #Preparation: [Time details]
                    
                    #Ingredients:
                    [List items line-by-line cleanly without complex markdown tables]
                    
                    #Instructions:
                    [Numbered steps in clean lines]
                    
                    #NutritionTable:
                    - Calories: 400
                    - Protein: 14
                    
                    #ProTip:
                    [A clever cooking trick]
                    """

                    response = client.chat.completions.create(
                        model=TEXT_MODEL,
                        messages=[
                            {"role": "system", "content": f"You are a helpful anime chef operating precisely inside the framework of language option: {st.session_state.selected_lang}."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.65
                    )
                    
                    recipe_out = response.choices[0].message.content
                    st.session_state.generated_recipe = recipe_out
                    
                    for line in recipe_out.split('\n'):
                        if "#RecipeName:" in line:
                            st.session_state.recipe_name = line.replace("#RecipeName:", "").strip()
                            break
                    
                    st.session_state.parsed_ingredients = clean_and_parse_ingredients(recipe_out)
                    
                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    history_entry = {
                        "timestamp": now,
                        "recipe_name": st.session_state.recipe_name,
                        "ingredients": user_input_query,
                        "recipe_text": recipe_out
                    }
                    current_user_data["history"].append(history_entry)
                    
                    st.session_state.current_page = "recipe"
                    st.snow()
                    st.rerun()

                except Exception as e:
                    st.error(f"Magic failed: {e}")

    # ----------------- SCREEN 2: RECIPE LAYOUT PAGE -----------------
    elif st.session_state.current_page == "recipe":
        col_left, col_right = st.columns([1.8, 1.2])

        with col_right:
            st.markdown("<div class='interactive-card'>", unsafe_allow_html=True)
            st.markdown("##### 🎛️ Interactive Portion Scaler")
            portions = st.slider("Adjust Servings Scale:", min_value=1, max_value=8, value=2, step=1)
            scaling_factor = portions / 2.0
            st.markdown(f"<small style='color:#65a30d;'>Quantities scaled optimally for **{portions} hungry foodies**!</small>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        original_text = st.session_state.generated_recipe
        dynamic_scaled_text = scale_recipe_numbers(original_text, scaling_factor)

        if "Hindi" in st.session_state.selected_lang:
            formatted_text = dynamic_scaled_text.replace("#RecipeName:", "").replace("#Preparation:", "⏱️ **बनाने का समय:**").replace("#Ingredients:", "🍓 **आवश्यक सामग्री:**").replace("#Instructions:", "👩‍🍳 **बनाने की विधि:**").replace("#NutritionTable:", "🐹 **पोषण तथ्य (Health Stats):**").replace("#ProTip:", "💡 **शेफ की सीक्रेट टिप:**")
        else:
            formatted_text = dynamic_scaled_text.replace("#RecipeName:", "").replace("#Preparation:", "⏱️ **Cooking Speed Details:**").replace("#Ingredients:", "🍓 **Ingredients needed:**").replace("#Instructions:", "👩‍🍳 **Chalo banate hain:**").replace("#NutritionTable:", "🐹 **Health Nutrition Metrics:**").replace("#ProTip:", "💡 **Chef Bunny's Pro Tip:**")

        with col_left:
            if st.button("🐾 Back to Main Counter", use_container_width=False):
                st.session_state.current_page = "input"
                st.session_state.generated_recipe = ""
                st.session_state.recipe_name = "Yummy Dish"
                st.rerun()

            st.markdown("<hr style='border: 2px dashed #FFB6C1; margin-top:5px;'>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class='recipe-card'>
                <div class='recipe-header'>✨ {st.session_state.recipe_name} ✨</div>
            </div>
            """, unsafe_allow_html=True)
            
            food_image_url = "https://images.unsplash.com/photo-1498837167922-ddd27525d352?w=600&auto=format&fit=crop"
            st.image(food_image_url, caption=f"🍽️ Custom Kitchen View: {st.session_state.recipe_name}", use_container_width=True)
            
            st.markdown(formatted_text)

            video_box_title = "🎬 ऐआई वीडियो गाइड आ गई!" if "Hindi" in st.session_state.selected_lang else "🎬 Your AI Video Guide is Ready!"
            video_box_desc = "Neeche button par click karte hi bina kisi error ke is recipe ki saari step-by-step cooking tutorial videos automatic load ho jayengi! ✨" if "Roman" in st.session_state.selected_lang or "Hindi" in st.session_state.selected_lang else "Click the action button below to seamlessly stream the visual cooking tutorial masterclass instantly! ✨"
            video_btn_label = "📺 Play Step-by-Step Cooking Video 🐰"

            safe_video_query = urllib.parse.quote(f"{st.session_state.recipe_name} recipe step by step cooking tutorial")
            safe_youtube_url = f"https://www.youtube.com/results?search_query={safe_video_query}"

            st.markdown(f"""
            <div class='video-monitor-box'>
                <h4 style='color: #FF5E7E; font-family: "Comic Sans MS", sans-serif; margin-bottom: 8px;'>{video_box_title}</h4>
                <p style='font-size: 14px; color: #475569; margin-bottom: 15px;'>{video_box_desc}</p>
                <a class='premium-video-link' href='{safe_youtube_url}' target='_blank'>{video_btn_label}</a>
            </div>
            """, unsafe_allow_html=True)

        with col_left:
            pass

        with col_right:
            st.markdown("<div class='interactive-card'>", unsafe_allow_html=True)
            st.markdown("##### 🛒 Smart Prep Checklist")
            st.markdown("<small style='color:#475569;'>Cross off items as you pull them from the fridge:</small>", unsafe_allow_html=True)
            
            for index, ingredient in enumerate(st.session_state.parsed_ingredients):
                scaled_ing = scale_recipe_numbers(ingredient, scaling_factor)
                st.checkbox(f"🎁 {scaled_ing}", key=f"ing_check_{index}")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("""
            <div class='nutrition-card'>
                <h5 style='color: #2B6CB0; margin:0;'>🌸 Yummy Health Stats 🌸</h5>
            </div>
            """, unsafe_allow_html=True)
            
            base_calories = 210
            scaled_calories = int(base_calories * portions)
            st.metric(label="Energy Value Estimation", value=f"❤ {scaled_calories} kcal")
            st.metric(label="Muscle Build Power", value=f"⭐ {int(7 * portions)}-{int(9 * portions)} grams")
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button(
                label="🎀 Save Recipe Diary (TXT)",
                data=dynamic_scaled_text,
                file_name=f"{st.session_state.recipe_name.lower().replace(' ', '_')}_for_{portions}_servings.txt",
                mime="text/plain",
                use_container_width=True
            )

        st.markdown("""
        <div class='thankyou-banner'>
            🌸 Thank you for using VM AI Kitchen! Made with love to make your cooking magical ✨ Happy Munching! 🧸🍉
        </div>
        """, unsafe_allow_html=True)