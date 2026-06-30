import streamlit as st
from openai import OpenAI

# Configuración principal de la página
st.set_page_config(page_title="SanaFlow AI", page_icon="🏥", layout="centered")

st.title("🏥 SanaFlow AI")
st.subheader("Asistente Inteligente de Triaje para Consultorios")
st.write("Esta aplicación utiliza Inteligencia Artificial para analizar los mensajes desorganizados de los pacientes y generar una ficha estructurada de triaje médico.")

with st.expander("ℹ️ ¿Cómo funciona este asistente?"):
    st.write("""
    1. **Credenciales:** Ingresa tu API Key de OpenAI en el panel lateral.
    2. **Contexto:** Indica la especialidad de tu consultorio.
    3. **Datos:** Pega el mensaje exacto que envió el paciente.
    4. **Acción:** Haz clic en el botón inferior para procesar.
    """)

st.sidebar.header("Configuración de IA")
st.sidebar.info("Para usar la app, ingresa tu clave de API de OpenAI (sk-...).")
api_key = st.sidebar.text_input("Ingresa tu API Key", type="password")

st.markdown("---")
st.markdown("### 📝 Ingreso de Datos del Paciente")

especialidad = st.text_input("Especialidad del Consultorio", placeholder="Ej. Psicología, Pediatría...")
mensaje_paciente = st.text_area("Mensaje recibido del paciente", height=150)

if st.button("Generar Ficha de Triaje con IA 🚀", type="primary"):
    if not api_key:
        st.error("⚠️ Falta la API Key. Ingrésala en el menú lateral.")
    elif not especialidad or not mensaje_paciente:
        st.warning("⚠️ Debes completar tanto la especialidad como el mensaje del paciente.")
    else:
        try:
            client = OpenAI(api_key=api_key)
            prompt_sistema = f"""
            Actúa como un asistente médico de triaje para un consultorio de la especialidad de {especialidad}.
            Analiza el siguiente mensaje enviado por un paciente que solicita un turno: '{mensaje_paciente}'.
            Genera una ficha con: 1. Motivo principal 2. Síntomas 3. Prioridad sugerida 4. Resumen para el profesional.
            """
            
            with st.spinner("Analizando..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "Eres un asistente clínico profesional."},
                        {"role": "user", "content": prompt_sistema}
                    ]
                )
                resultado = response.choices[0].message.content
                
                st.success("¡Ficha clínica generada exitosamente!")
                st.info(resultado)
        except Exception as e:
            st.error("❌ Ocurrió un error. Verifica tu API Key de OpenAI.")
