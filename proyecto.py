import streamlit as st # importar la libreria
from groq import Groq 



#configuracion de la ventana de la web
st.set_page_config(page_title = "mi chat de IA", page_icon="💫")

#titulo de la pagina
st.title("mi primera aplicacion con streamlit")

#ingreso de dato del usuario
nombre = st.text_input("¿cual es tu nombre?")

#creamos boton con funcionalidad
if st.button("saludar"):
    st.write(f"hola {nombre}, gracias por participar")


modelo = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

#nos conectamos a API
def crear_usuario_groq():
    clave_secreta=st.secrets["CLAVE_API"]#obtiene la clave de la API
    return Groq(api_key=clave_secreta) #conectamos con la API
#configuramos el modleo que se va a usar
def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model=modelo, #indica el modelo de la IA
        messages=[{"role": "user", "content": mensajeDeEntrada}], #clave:valor
        stream=True #para que el modelo responda a tiempo
    )

#historial de mensajes (bacio)
def inicializar_estado():
    #si no existe una lista llamada mensaje entonces la creamos 
    if "mensajes" not in st.session_state: 
        st.session_state.mensajes = []#lista vacia (historial vacio)

def actualizar_historial(rol, contenido, avatar): #llenar el historial bacio
    #el metodo apped() agrega un elemento a la lista
    st.session_state.mensajes.append(
        {"role": rol, "content": contenido, "avatar": avatar}
    )

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar= mensaje["avatar"]): 
            st.markdown(mensaje["content"])

#contenedor del chat
def area_chat():
    contenedorDelChat=st.container(height=400, border= True)
    #agrupamos los mensajes en el area del chat
    with contenedorDelChat: mostrar_historial() #agrupar operaciones

# creando funcion
def configurar_pagina():
    st.title("mi chat de IA") #titulo
    st.sidebar.title("configuracion") #menu lateral 
    elegirModelo = st.sidebar.selectbox(
        "elegi un modulo", #titulo
        modelo, #opciones del menu
        index= 0 #valorDefecto
    )
    return elegirModelo 

def generar_respuestas(chat_completo):
    respuesta_completa="" #texto vacio
    for frase in chat_completo: 
        if frase.choices[0].delta.content:
            respuesta_completa+=frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa #juntar todas las palabras de la ia en un solo lugar


def main():
    #invocacion de funciones
    modelo=configurar_pagina() #llamamos a la funcion
    clienteUsuario=crear_usuario_groq()#crea el usuario para usar al API
    inicializar_estado()#crea el historial de mensaje
    area_chat() #creamos el sector para ver los mensajes

    mensaje=st.chat_input("Escribi un mensaje...")

    #verificamos si el mensaje tiene contenido
    if mensaje:
        actualizar_historial("user", mensaje, "🐶") #visualizamos el mensaje del usuario
        chat_completo=configurar_modelo(clienteUsuario, modelo, mensaje)
        if chat_completo:
            with st.chat_message("assistant"):#generar el control visual
                respuesta_completa=st.write_stream(generar_respuestas(chat_completo))
                actualizar_historial("assistant", respuesta_completa, "🤖")
                st.rerun()
#indicamos que nuesttra funcion principal es main
if __name__ == "__main__":
    main()


#generar_respuestas(chat_completo)
#actualizar_historial("assistant", chat_completo, "🤖") #ver el mensaje del modelo/ia
#st.rerun() # da respuestas de forma inmediata
#print(mensaje)



#st.write(f"usuario: {mensaje}") 