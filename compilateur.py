import json
import random
import time
import ply.lex as lex
import requests
import streamlit as st
import numpy as np
from PIL import Image
import speech_recognition as sr
from streamlit_lottie import st_lottie
import ply.yacc as yacc
import pandas as pd
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

proverbs_contexts = {
                    'دير النيه وبات مع الحيه': 'يبدو بعض الأشخاص صادقين، لكن عندما يصافحونك، من الأفضل أن تعد أصابعك مرة أخرى',
                    'زعم تاكل اللحم': 'يعبر المثل عن النصيحة بأنه يجب أن يتم قياس الأشخاص بأفعالهم الفعلية وإنجازاتهم بدلاً من الكلام الكثير والمبالغة في التظاهر بالقوة والقدرة. يُشجع الأشخاص على أن يقدموا أدلة واقعية على مهاراتهم وقدراتهم بدلاً من الاعتماد على الزعم والمبالغة في التفاخر',
                    'اش خاصك العريان الخاتم امولاي': 'نحن نستغلّ طاقة الشباب تحسباً لوهن الشيخوخة ',
                    'لبغا العسل يصبر على قريص النحل': 'هذا التعبير يستخدم غالبًا ليعبر عن فكرة أن الشخص الذي يرغب في شيء لطيف وممتع قد يضطر في بعض الأحيان إلى تحمل تحديات أو مواقف غير مريحة. يسلط الضوء على المبدأ الذي يشير إلى أن الجائزة قد تتطلب جهدًا أو تضحية أو مواجهة صعوبات. بشكل عام، يعبر التعبير عن فكرة أن الأشياء الجيدة في الحياة قد تحتاج إلى بعض الجهد أو التحمل لتحقيقها' ,
                    'الفقيه اللي نتسناو بركتوا دخل الجامع ببلغتوا': 'نحن نستغلّ طاقة الشباب تحسباً لوهن الشيخوخة ',
                    'فران وقاد بحومه': 'اذا كانت هناك ضجة كبيرة على موضوع تافه لا يستحق',
                    'هزك الماء ضربك الضوء':'تعبر عن وضع يجد فيه الشخص نفسه في صعوبة أو مشكلة، غالبًا بسبب قرار سيء أو خداع. هذا يعني عادة أن الشخص وقع في وضع حساس أو غير مريح بعد أن تم خداعه أو خداعه.'
                    # Ajoutez d'autres proverbes et contextes
                }


# Sample photo and video data (replace with your actual file paths or URLs)
photo_data = {'دير النيه وبات مع الحيه': 'image/dirNiya.jpg',
                 'زعم تاكل اللحم': 'image/l7am.jpg',
                 'اش خاصك العريان الخاتم امولاي': 'image/l3aryan.jpeg',
                 'لبغا العسل يصبر على قريص النحل':'image/l3ssal.jpeg',
                 'الفقيه اللي نتسناو بركتوا دخل الجامع ببلغتوا':'image/lf9ih.jpeg',
                 'فران وقاد بحومه':'image/faran.jpeg',
                 'اللي دركك بخيط دركو بحيط':'image/7iit.jpeg',
                 'هزك الماء ضربك الضوء':'image/hazaklma.jpg'
            }


french_data = {
    'دير النيه وبات مع الحيه': 'Fais attention à la mauvaise intention et dors avec le serpent',
    'زعم تاكل اللحم': 'Les prétentions ne nourrissent pas',
    'اش خاصك العريان الخاتم امولاي': 'Que te manque-t-il homme nu ? Une bague mon seigneur',
    'لبغا العسل يصبر على قريص النحل': 'Qui veut du miel doit supporter les piqûres d\'abeilles',
    'فران وقاد بحومه': 'Il a agi de manière franche et dirigée par sa sagesse',
    'هزك الماء ضربك الضوء':'Etre dans le pétrin, se faire avoir',
    'الفقيه اللي نتسناو بركتوا دخل الجامع ببلغتوا': 'Le savant que nous attendons avec impatience est entré dans la mosquée avec sa bénédiction'
}

french_context ={
    'دير النيه وبات مع الحيه': 'Il semble que certaines personnes soient sincères, mais quand elles te serrent la main, il vaut mieux compter tes doigts une fois de plus',
    'زعم تاكل اللحم': 'ce proverbe souligne l\'importance de juger les personnes par leurs actions réelles et leurs réalisations plutôt que par leurs paroles et leurs prétentions. Il encourage les individus à fournir des preuves concrètes de leurs compétences plutôt que de se contenter de prétendre et de se vanter.',
    'اش خاصك العريان الخاتم امولاي': 'Nous exploitons l`énergie des jeunes en prévision de la faiblesse de la vieillesse',
    'لبغا العسل يصبر على قريص النحل': 'Rien n\'est gratuit. Toutes les bonnes choses ont un prix.',  
    'هزك الماء ضربك الضوء':'"être dans le pétrin, se faire avoir" exprime une situation où quelqu\'un se trouve dans une difficulté ou une complication, souvent en raison d\'une mauvaise décision ou d\'une tromperie. Cela signifie généralement être pris dans une situation délicate ou désagréable après avoir été trompé ou dupé.',
    'فران وقاد بحومه': 'l`expression dans son ensemble pourrait signifier que quelqu `un agit de manière franche et directe, tout en étant guidé par la sagesse dans ses actions. Cela pourrait être une louange à quelqu`un qui prend des décisions judicieuses et agit de manière transparente.', 
    'الفقيه اللي نتسناو بركتوا دخل الجامع ببلغتوا': 'Le savant que nous attendons avec impatience est entré dans la mosquée avec sa bénédiction, montrant ainsi sa sincérité et sa sagesse dans son engagement religieux.'
}
english_data = {
    'دير النيه وبات مع الحيه': 'Pay attention to the bad intention and sleep with the snake',
    'زعم تاكل اللحم': 'Claiming doesn\'t feed you',
    'اش خاصك العريان الخاتم امولاي': 'What do you need, naked man? A ring, my lord',
    'لبغا العسل يصبر على قريص النحل': 'Whoever wants honey must endure the stings of bees',
    'فران وقاد بحومه': 'He acted in a frank manner and led with wisdom',
    'هزك الماء ضربك الضوء':'Shook you like water and struck you like light.',
    'الفقيه اللي نتسناو بركتوا دخل الجامع ببلغتوا': 'The scholar we eagerly await entered the mosque with his blessing'
}


english_context = {
    'دير النيه وبات مع الحيه': 'It seems that some people are sincere, but when they shake your hand, it\'s better to count your fingers once again.',
    'زعم تاكل لحم': 'this proverb emphasizes the importance of judging people based on their actual actions and accomplishments rather than their words and claims. It encourages individuals to provide tangible evidence of their skills rather than relying on empty boasts and pretenses.',
    'اش خاصك العريان الخاتم امولاي': 'We harness the energy of the youth in anticipation of the weakness of old age.',
    'لبغا العسل يصبر على قريص النحل': 'Nothing is free. All good things have a price.',
    'هزك الماء ضربك الضوء':'expresses a situation where someone finds themselves in difficulty or complication, often due to a poor decision or deception. It generally means being caught in a tricky or unpleasant situation after being deceived or tricked.',
    'فران وقاد بحومه': 'The expression as a whole could mean that someone acts in a frank and direct manner, while being guided by wisdom in their actions. It could be praise for someone who makes wise decisions and acts transparently.',
    'الفقيه اللي نتسناو بركتوا دخل الجامع ببلغتوا': 'The scholar we eagerly await entered the mosque with his blessing, showing thus his sincerity and wisdom in his religious commitment.',
}


# Lexer and Parser
tokens = (
    'FIRST',
    'SECOND',
    'THIRD',
    'FOURTH',
    'FIFTH',
    'SIXTH',
    'SEVENTH',
    'SPACE'
)
# Error list
lexer_errors = []

# Define the expressions for each token
def t_FIRST(t):
    r'هزك|دير|زعم|اش|لبغا|الفقيه|فران|اللي'
    return t

def t_SECOND(t):
    r'الماء|النيه|تاكل|خاصك|العسل|اللي|وقاد|دركك'
    return t

def t_THIRD(t):
    r'ضربك|وبات|اللحم|العريان|يصبر|بحومه|بخيط|نتسناو'
    return t

def t_FOURTH(t):
    r'الضوء|مع|بركتوا|الخاتم|على|دركو'
    return t

def t_FIFTH(t):
    r'الحيه|امولاي|قريص|بحيط|دخل'
    return t

def t_SIXTH(t):
    r'النحل|الجامع'
    return t

def t_SEVENTH(t):
    r'ببلغتوا'
    return t

def t_SPACE(t):
    r'\s+'
    pass  # Ignore spaces

# Error handling
# def t_error(t):
#     st.write(f"Illegal character '{t.value[0]}'")
#     t.lexer.errors += 1
#     t.lexer.skip(1)
def t_error(t):
    global lexer_errors
    lexer_errors.append((t.value[0], t.lexpos - text.rfind('\n', 0, t.lexpos)))
    t.lexer.skip(1)
    t.lexer.errors += 1

# Build the lexer
lexer = lex.lex()

# Define the start symbol
start = 'sentence'

# Define the grammar rules
def p_sentence(p):
    '''
    sentence : FIRST SECOND THIRD FOURTH FIFTH SIXTH SEVENTH
            | FIRST SECOND THIRD FOURTH FIFTH SIXTH
            | FIRST SECOND THIRD FOURTH FIFTH
            | FIRST SECOND THIRD FOURTH
            | FIRST SECOND THIRD
            | FIRST SECOND
            | FIRST 

    '''
    pass
    p[0] = ' '.join(p[1:])

msg_error = ""
msg__ = ""
# Error handling
def p_error(p):
    global msg_error,msg__
    if lexer.errors == 0:
        msg_error+= f"Ghlti f Syntaxe 3awed kteb dakchi mezyan : '{p.value}'\n"
        msg__ += f"Ghlti f Syntaxe 3awed kteb dakchi mezyan : '{p.value}'\n"
       

# Build the parser
parser = yacc.yacc()

# Function to test the parser with examples
# def test_parser(text):
#     lexer.input(text)
#     lexer.errors = 0
#     return parser.parse()
def test_parser(text):
    global msg__
    lexer.input(text)
    lexer.errors = 0
    parso = parser.parse()
    if lexer_errors:
        msg__ += "Ghlti: "
        for character, col in lexer_errors:
            msg__ += " '{}' f blassa {}".format(character, col)
        return None
    return parso

def chatbot_parser(text):
    global msg_error
    lexer.input(text)
    lexer.errors = 0
    parso = parser.parse()
    if lexer_errors:
        msg_error += "Ghlti "
        for character, col in lexer_errors:
            msg_error += " '{}' f blassa {}".format(character, col)
        return None
    return parso


# Streamlit Configuration
st.set_page_config(page_title="Compilateur", page_icon='', layout="wide")

# Helper Function to Resize Image
def resiezeImage(img, new_width, new_height):
    original_image = Image.open(img)
    resized_image = original_image.resize((new_width, new_height))
    return resized_image

# Load Lottie Files
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
    


    
def about_app():
    st.markdown('<p style="font-size: 25px;">This video shows how awesome Morocco is and how cool their culture is. You get to see beautiful places, like colorful markets and the amazing Sahara Desert. The people in the video seem really nice and welcoming, making you feel like youd love to visit. Its like a cool journey through Morocco is history and traditions, with a mix of different influences that make it special. Overall, its a fantastic look at the beauty and cool things about Morocco that make you want to go there someday.</p>', unsafe_allow_html=True)


    st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 400px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 400px;
        margin-left: -400px;
    }
    </style>
    """,
    unsafe_allow_html=True,
    )

    video_path = 'Morocco in Motion  Travel Video.mp4'
    st.video(video_path)

    #st.markdown('<p style="font-size: 35px;">Here are some proverbs in Darija and their meanings in English.</p>', unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;margin-bottom:20px;'>Here are some proverbs in Darija and their meanings in English:</h1>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
   
    image1 = '4.jpeg'
    t1, t2 = st.columns((0.6,0.3))
    with t1:
        st.markdown('<h1>تعطيهم عينيك يطمعوا في حواجبك</h1>', unsafe_allow_html=True)
        st.write("##")
        st.write(
            """
       The phrase "تعطيهم عينيك يطمعوا في حواجبك" in Arabic can be translated 
       into English as "Give them your eyes, they'll covet your eyebrows."
       This expression suggests that when you show or share something valuable,
       people may develop desires for even more precious or desirable things that you possess.
       In other words, it serves as a warning against the temptation 
       to share too much or reveal too many things, as it can trigger envy or desires in others.
            """
        )
      

    with t2:
        st.image([image1], width=350)

    # Ajouter une marge entre les deux paires d'images
    st.markdown("<br><br>", unsafe_allow_html=True)

    image2 = '2.jpeg'
    t5, t6 = st.columns((0.6,0.3))
    with t5:
        st.markdown('<h1>كاين للي عندو لعقل كيفكر بيه و كاين لي غير هازو متقل بيه</h1>', unsafe_allow_html=True)
        st.write("##")
        st.write(
            """
        There are those who use their minds wisely, 
        and there are others who only carry it on their shoulders."
        This expression suggests a distinction between individuals 
        who use their intelligence and those who merely bear the weight 
        of a mind without employing it effectively. It implies that possessing intelligence
        is valuable when it is actively employed for thoughtful and wise considerations, 
        rather than merely being a burden or unused potential.
            """
        )

    with t6:
        st.image([image2], width=350)

    # Ajouter une marge entre les deux paires d'images
    st.markdown("<br><br>", unsafe_allow_html=True)

    image3 = '6.jpeg'
    t7, t8 = st.columns((0.6,0.3))
    with t7:
        st.title(" لكلشي في وقتو زين و اللي زرب على خبزتو ياكلها عجين")
        st.write("##")
        st.write(
            """
           "Everything has its own good time, and the one who kneads 
           his dough will eat it as bread."
           This expression conveys the idea that everything 
           has its proper time or season, and those who put in effort 
           and work patiently will eventually enjoy the rewards.
           The metaphor of kneading dough suggests that hard work 
           and dedication lead to the eventual fruition or success,
           akin to enjoying the bread after the labor of kneading.
            """
        )

    with t8:
        st.image([image3], width=350)

        #features1=load_lottiefile('fetures.json')
       
#!speesh to proverbe
def speech_to_proverb():
    global text

    r = sr.Recognizer()
   
    load_lottieurl=load_lottiefile('../Streamlit_code/Animation1.json')
    t7, t8 = st.columns((0.6,0.3))
    with t7:
        
        st.header('Speech-to-Proverb Feature Description:')

   
        st.markdown('<p style="font-size: 25px;">This feature allows users to verbally input phrases in Moroccan Darija through a microphone</p>', unsafe_allow_html=True)
     

    with t8:
        st_lottie(load_lottieurl, height=200, key="voice")
  
    
    if st.button("Start Talking"):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("Say something!")
            audio = r.listen(source, phrase_time_limit=5)

            try:
                # transcribe the speech to text using Google Speech Recognition
                text = r.recognize_google(audio, language='ar')
                st.write(f"You said: {text}", font_size=41)

                recognized_proverb = test_parser(text)
                if recognized_proverb != None: # check lexical syntaxique 
                    if recognized_proverb in proverbs_contexts: #semantique
                        context = proverbs_contexts[recognized_proverb]
                        
                        st.write(f'<div style="text-align: right;"><p style="font-size: 30px;">المعنى باللغة العربية: {context}</p></div>', unsafe_allow_html=True)


                        # Check if the recognized proverb has an associated image
                        image_path = photo_data.get(recognized_proverb)
                        if image_path:
                            st.image(image_path,width=800)
                        else:
                            st.error("Image not available for this proverb.")
                    

                    else:
                        st.error("Unrecognized proverb or undefined context.")
                else: 
                    st.error(msg__)

            except sr.UnknownValueError:
                st.write("Sorry, I did not understand what you said.")
            except sr.RequestError as e:
                st.write(f"Could not request results from Google Speech Recognition service; {e}")


#!proverbe into context
def proverb_into_context():
    global text
    
    load_lottieurl=load_lottiefile('../Streamlit_code/Animation2.json')
    t7, t8 = st.columns((0.6,0.3))
    with t7:
        
        st.header('Proverb into Context Description:')
        st.markdown('<p style="font-size: 25px;">This feature interprets spoken Moroccan Darija phrases, identifies recognized proverbs within them, and provides concise contextual,cultural information and linguistic understanding.</p>', unsafe_allow_html=True)
    with t8:
        st_lottie(load_lottieurl, height=200, key="voice")
    st.subheader('Choose the language')
    txt_mode=st.selectbox("Pick one", ["CONTEXE ARABE", "CONTEXE FRENCH","CONTEXE ENGLISH"])
    text = st.text_input("Enter text:")
    if st.button("Convert"):
        if txt_mode == "CONTEXE ARABE":
            recognized_proverb = test_parser(text)
            if recognized_proverb != None:         
                if recognized_proverb in proverbs_contexts:
                        context = proverbs_contexts[recognized_proverb]

                        #st.write(f'<p style="font-size: 30px;">المعنى باللغة العربية: {context}</p>',unsafe_allow_html=True)
                        st.write(f'<div style="text-align: right;"><p style="font-size: 30px;">المعنى باللغة العربية: {context}</p></div>', unsafe_allow_html=True)

                        frech_proverb = french_data.get(recognized_proverb)
                        # Check if the recognized proverb has an associated image
                        image_path = photo_data.get(recognized_proverb)
                        t18,t19=st.columns((0.3,1.7))
                        with t18:
                                st.write('')
                        with t19:
                            if image_path:
                                st.image(image_path,width=800)
                            else:
                                st.error("Image not available for this proverb.")
                        # Check if the recognized proverb has an associated video
                       
                else:
                        st.error("Unrecognized proverb or undefined context.")
            else:
                st.error(msg__)
                
        elif txt_mode == "CONTEXE FRENCH":
            recognized_proverb = test_parser(text)
            if recognized_proverb != None:
                if recognized_proverb in proverbs_contexts:
                        context = proverbs_contexts[recognized_proverb]
                        frech_proverb = french_data.get(recognized_proverb)
                        if frech_proverb:
                                st.write(f'<p style="font-size: 30px;">Proverbe en Francais: {frech_proverb}</p>',unsafe_allow_html=True)
                        french_context1 = french_context.get(recognized_proverb)
                        if french_context1:
                                st.write(f'<p style="font-size: 30px;">Signification en Francais: {french_context1}</p>',unsafe_allow_html=True)
                        # Check if the recognized proverb has an associated image
                        image_path = photo_data.get(recognized_proverb)
                        t18,t19=st.columns((0.3,1.7))
                        with t18:
                                st.write('')
                        with t19:
                            if image_path:
                                st.image(image_path,width=800)
                            else:
                                st.error("Image not available for this proverb.")
                        # Check if the recognized proverb has an associated video
                      
                else:
                        st.error("Unrecognized proverb or undefined context.")
            else:
                st.error(msg__)
                
        else:
            recognized_proverb = test_parser(text)
            if recognized_proverb != None:
                if recognized_proverb in proverbs_contexts:
                        context = proverbs_contexts[recognized_proverb]
                        english_proverb = english_data.get(recognized_proverb)
                        if english_proverb:
                            st.write(f'<p style="font-size: 30px;">Proverb In English: {english_proverb}</p>',unsafe_allow_html=True)
                        english_context1 = english_context.get(recognized_proverb)
                        if english_context1:
                            st.write(f'<p style="font-size: 30px;">Meaning in English: {english_context1}</p>',unsafe_allow_html=True)
                        # Check if the recognized proverb has an associated image
                        image_path = photo_data.get(recognized_proverb)
                        t18,t19=st.columns((0.3,1.7))
                        with t18:
                                st.write('')
                        with t19:
                            if image_path:
                                st.image(image_path,width=800)
                            else:
                                st.error("Image not available for this proverb.")
               
                else:
                        st.error("Unrecognized proverb or undefined context.")
            else:
                st.error(msg__)

                
def extract_text_between_quotes(input_text):
    start_quote = input_text.find('"')
    end_quote = input_text.rfind('"')
    if start_quote != -1 and end_quote != -1 and start_quote < end_quote:
        return input_text[start_quote + 1:end_quote]
    else:
        return None




def chatbot():
    global text
    check = 'تكون بخير في هاد الدنيا خاصك طبق'
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Initialize full_response outside the if statement
        full_response = ""

        if prompt == 'السلام و عليكم اش خبرك':
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                assistant_response = random.choice(
                    [
                        "بخير الحمد الله و انت واش بخير؟",

                    ]
                )
                # Simulate stream of response with milliseconds delay
                for chunk in assistant_response.split():
                    full_response += chunk + " "
                    time.sleep(0.05)
                    # Add a blinking cursor to simulate typing
                    message_placeholder.markdown(full_response + " ")
                    message_placeholder.markdown(full_response)

        elif check in prompt:
            text = extract_text_between_quotes(prompt)
            if text != None:
                recognized_proverb = chatbot_parser(text)
                if recognized_proverb in proverbs_contexts:# if lexical and syntaxique o kolchi s7i7
                    with st.chat_message("assistant"):
                        message_placeholder = st.empty()
                        assistant_response = random.choice(
                            [
                                "واش كتقصد بالعسل؟",             
                            ]
                        )
                        # Simulate stream of response with milliseconds delay
                        for chunk in assistant_response.split():
                            full_response += chunk + " "
                            time.sleep(0.05)
                            # Add a blinking cursor to simulate typing
                            message_placeholder.markdown(full_response + " ")
                            message_placeholder.markdown(full_response)
                else:
                    with st.chat_message("assistant"):
                        message_placeholder = st.empty()
                        assistant_response = random.choice(
                            [
                                "Rak : "+msg_error,             
                            ]
                        )
                        for chunk in assistant_response.split():
                            full_response += chunk + " "
                            time.sleep(0.05)
                            # Add a blinking cursor to simulate typing
                            message_placeholder.markdown(full_response + " ")
                            message_placeholder.markdown(full_response)   
            else:
                with st.chat_message("assistant"):
                        message_placeholder = st.empty()
                        assistant_response = random.choice(
                            [
                                "?واش كتقصد",             
                            ]
                        )
                        # Simulate stream of response with milliseconds delay
                        for chunk in assistant_response.split():
                            full_response += chunk + " "
                            time.sleep(0.05)
                            # Add a blinking cursor to simulate typing
                            message_placeholder.markdown(full_response + " ")
                            message_placeholder.markdown(full_response)
                
            # Display assistant response in chat message container 
        elif prompt == 'في المثل هاذا، العسل رمز للهموم والتحديات، والناس لازم تصبر عليها باش توصل للي تبغاه' :
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                assistant_response = random.choice(
                    [
                        "والله كيفما قالو الصبر مفتاح الفرج",
                    ]
                )
                # Simulate stream of response with milliseconds delay
                for chunk in assistant_response.split():
                    full_response += chunk + " "
                    time.sleep(0.05)
                    # Add a blinking cursor to simulate typing
                    message_placeholder.markdown(full_response + " ")
                    message_placeholder.markdown(full_response)
        else :
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                assistant_response = random.choice(
                    [
                        "مفهمتش أشنو كتبتي ليا",
                    ]
                )
                # Simulate stream of response with milliseconds delay
                for chunk in assistant_response.split():
                    full_response += chunk + " "
                    time.sleep(0.05)
                    # Add a blinking cursor to simulate typing
                    message_placeholder.markdown(full_response + " ")
                    message_placeholder.markdown(full_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})


def main():
    st.markdown("<h1 style='text-align: center;margin-bottom:50px;'>Welcome to our simulation.</h1>", unsafe_allow_html=True)

    # ...

    app_mode = st.sidebar.selectbox('Choose the App mode', ['About App', 'Contexte into proverbe', 'proverbe into contexte','ChatBot'])

    if app_mode == 'About App':
         about_app()
    elif app_mode == 'proverbe into contexte':
         proverb_into_context()
    elif app_mode=='Contexte into proverbe':
         speech_to_proverb()
    else:
         chatbot()


if __name__ == "__main__":
    main()