import streamlit as st
import google.generativeai as genai
import time

# Configuración principal de la página
st.set_page_config(page_title="SanaFlow AI", page_icon="🏥", layout="centered")

st.title("🏥 SanaFlow AI")
st.subheader("Asistente Inteligente de Triaje para Consultorios")
st.write("Esta aplicación utiliza la Inteligencia Artificial de Google (Gemini) para analizar los mensajes desorganizados de los pacientes y generar una ficha estructurada de triaje médico.")

with st.expander("ℹ️ ¿Cómo funciona este asistente?"):
    st.write("""
    1. **Credenciales:** Ingresa tu API Key de Gemini en el panel lateral.
    2. **Contexto:** Indica la especialidad de tu consultorio.
    3. **Datos:** Pega el mensaje exacto que envió el paciente.
    4. **Acción:** Haz clic en el botón inferior para procesar.
    """)

st.sidebar.header("Configuración de IA")
st.sidebar.info("Para usar la app, obtén tu clave gratuita en Google AI Studio e ingrésala abajo (empieza con AIza...). \n\n*Nota: Puedes usar 'demo123' para simular.*")
api_key = st.sidebar.text_input("Ingresa tu API Key de Gemini", type="password")

st.markdown("---")
st.markdown("### 📝 Ingreso de Datos del Paciente")

especialidad = st.text_input("Especialidad del Consultorio", placeholder="Ej. Traumatología, Psicología...")
mensaje_paciente = st.text_area("Mensaje recibido del paciente", height=150, placeholder="Ej. Hola doctor, me duele mucho la rodilla desde que fui a correr ayer...")

if st.button("Generar Ficha de Triaje con IA 🚀", type="primary"):
    if not api_key:
        st.error("⚠️ Falta la API Key. Ingrésala en el menú lateral.")
    elif not especialidad or not mensaje_paciente:
        st.warning("⚠️ Debes completar tanto la especialidad como el mensaje del paciente.")
    else:
        # ---- MODO DEMO ----
        if api_key == "demo123":
            with st.spinner("La Inteligencia Artificial está analizando el caso..."):
                time.sleep(2)
                resultado_demo = f"""
                **1. Motivo principal:** Dolor agudo tras actividad física.
                
                **2. Síntomas detectados:**
                - Dolor intenso en la zona afectada.
                - Posible inflamación (relacionada al esfuerzo).
                
                **3. Prioridad sugerida:** Media (Requiere evaluación a corto plazo para descartar lesión).
                
                **4. Resumen para el profesional:** Paciente refiere dolor de inicio agudo posterior a esfuerzo físico (correr). Se sugiere evaluación en las próximas 48hs para descartar patología tendinosa o articular en el contexto de {especialidad}.
                """
                st.success("¡Ficha clínica generada exitosamente!")
                st.info(resultado_demo)
                
        # ---- MODO REAL CON GEMINI ----
        else:
            try:
                # Configurar la API de Google Gemini
                genai.configure(api_key=api_key)
                
                # Usar el modelo Pro (versión clásica muy estable para evitar el error 404)
                model = genai.GenerativeModel('gemini-pro')
                
                prompt_sistema = f"""
                Actúa como un asistente médico de triaje profesional para un consultorio de la especialidad de {especialidad}.
                Analiza el siguiente mensaje enviado por un paciente que solicita un turno: '{mensaje_paciente}'.
                
                A partir de este mensaje, genera una ficha estructurada que contenga estrictamente:
                1. Motivo principal (Resumen de máximo 5 palabras).
                2. Síntomas detectados (Una lista breve).
                3. Prioridad sugerida (Baja, Media o Alta).
                4. Resumen para el profesional (Un texto de 2 líneas redactado en lenguaje técnico-médico).
                
                No agregues saludos ni comentarios extra, solo devuelve la ficha estructurada.
                """
                
                with st.spinner("Gemini está analizando el caso..."):
                    response = model.generate_content(prompt_sistema)
                    
                    st.success("¡Ficha clínica generada exitosamente!")
                    st.info(response.text)
            except Exception as e:
                st.error(f"❌ Ocurrió un error con la API. Verifica que tu clave de Gemini sea correcta. Detalle: {e}")
