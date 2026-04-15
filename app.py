import streamlit as st

# Configuration de la page pour mobile
st.set_page_config(page_title="Calculateur Labo Eric", page_icon="🧪")

st.title("🧪 Assistant de Labo")
st.markdown("---")

# Menu principal
menu = ["Solide", "Liquide", "Dilution (Mère/Fille)"]
choix = st.sidebar.selectbox("Espèce à prélever :", menu)

# --- 1. MODULE SOLIDES ---
if choix == "Solide":
    st.header("⚖️ Préparation par pesée")
    mode = st.radio("Concentration demandée :", ["Concentration MASSIQUE (g/L)", "Concentration MOLAIRE (mol/L)"])
    
    v = st.number_input("Volume final souhaité (L)", min_value=0.0, value=0.100, step=0.01, format="%.3f")
    
    if mode == "Concentration MASSIQUE (g/L)":
        cm = st.number_input("Concentration massique demandée (g/L)", min_value=0.0, value=10.0)
        masse = cm * v
    else:
        c = st.number_input("Concentration molaire demandée (mol/L)", min_value=0.0, value=0.1, format="%.4f")
        m_mol = st.number_input("Masse molaire du solide (g/mol)", min_value=0.0, value=58.44)
        masse = c * v * m_mol
    
    st.metric("Masse à peser :", f"{masse:.4f} g")

# --- 2. MODULE LIQUIDES ---
elif choix == "Liquide":
    st.header("💧 Prélèvement de liquide pur")
    st.info("Utilisé pour les acides concentrés ou solvants.")
    
    v_sol = st.number_input("Volume de solution à préparer (L)", min_value=0.0, value=0.100, step=0.01, format="%.3f")
    purete = st.number_input("Pureté (ex: 37% -> taper 37)", min_value=0.0, max_value=100.0, value=98.0) / 100
    d = st.number_input("Densité ou Masse volumique (g/mL)", min_value=0.0, value=1.84)
    
    mode_l = st.radio("Concentration demandée :", ["Concentration MASSIQUE (g/L)", "Concentration MOLAIRE (mol/L)"])
    
    if mode_l == "Concentration MASSIQUE (g/L)":
        target_cm = st.number_input("Concentration massique demandée (g/L)", min_value=0.0, value=5.0)
        v_prelev = (target_cm * v_sol) / (purete * d)
        m_prelev = (target_cm *v_sol) / (purete)
    else:
        target_c = st.number_input("Concentration molaire demandée (mol/L)", min_value=0.0, value=0.1)
        m_mol_l = st.number_input("Masse molaire (g/mol)", min_value=0.0, value=98.08)
        v_prelev = (target_c * v_sol * m_mol_l) / (purete * d)
        m_prelev = (target_c * v_sol * m_mol_l) / (purete)

    col1, col2, col3 = st.columns([2, 2, 2])

    with col1:
        st.metric("Volume à prélever :" , f"{v_prelev:.2f} mL")

    with col2:
        st.markdown("<div style='text-align:center; margin-top:15px;'><h2 style='font-size:30px; font-weight:bold;'>OU</h2></div>", unsafe_allow_html=True)

    with col3:
        st.metric("Masse à prélever :", f"{m_prelev:.2f} g")
    

# --- 3. MODULE DILUTION ---
elif choix == "Dilution (Mère/Fille)":
    st.header("🧪 Dilution de solution")
    unit = st.radio("Concentration demandée :", ["Concentration MASSIQUE (g/L)", "Concentration MOLAIRE (mol/L)"])
    
    c_mere = st.number_input(f"{unit} de la solution MÈRE", min_value=0.0001, value=1.0)
    c_fille = st.number_input(f"{unit} de la solution FILLE", min_value=0.0001, value=0.1)
    v_fille = st.number_input("Volume FILLE souhaité (mL)", min_value=0.0, value=100.0)
    
    if c_fille >= c_mere:
        st.error("La fille doit être moins concentrée que la mère !")
    else:
        v_mere = (c_fille * v_fille) / c_mere
        st.metric("Volume MÈRE à prélever :", f"{v_mere:.2f} mL")
        st.write(f"👉 Verser {v_mere:.2f} mL de mère et compléter jusqu'à {v_fille} mL.")
