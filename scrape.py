import nltk
import spacy
import os
import openai
import base64
import time
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
import io
from streamlit_tags import st_tags
import streamlit as st
from pdfminer.high_level import extract_text
import pandas as pd
from selenium.webdriver.common.by import By
from selenium import webdriver


st.set_page_config(page_title="Resume Analyzer",layout='wide')





@st.cache_resource()
def load_model(model_name1,model_name2):
    nlp1=spacy.load(model_name1)
    nlp2=nltk.download(model_name2)
    return nlp1,nlp2

npl1=load_model('en_core_web_sm','stopwords')
openai.api_key='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'

@st.cache_data
def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

@st.cache_data
def show_pdf(path):
    with open(path ,'rb') as f:
        base64_pdf=base64.b64encode(f.read()).decode('utf-8')
    pdf_show = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="700" type="application/pdf"></iframe>'
    st.markdown(pdf_show, unsafe_allow_html=True)

@st.cache_data
def pdf_reader(file):
    resource_manager=PDFResourceManager()
    fake_file_handle=io.StringIO()
    conveter=TextConverter(resource_manager,fake_file_handle,laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager,conveter)
    with open(file,'rb') as fh:
        for page in PDFPage.get_pages(fh,caching=True,check_extractable=True):
            page_interpreter.process_page(page)
            print(page)
        text=fake_file_handle.getvalue()
    conveter.close()
    fake_file_handle.close()
    return text

@st.cache_data
def summarization(resume_text):
    output=openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{'role':'user',
              'content':f'Analyse {resume_text} and give a summary of the resume'}])
    return (output['choices'][0]['message']['content'])

@st.cache_data
def Streangth_weakness(resume_text):
    output=openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{'role':'user',
              'content':f'Analyse {resume_text} and give Strength of the resume and weakness of the resume'}])
    return (output['choices'][0]['message']['content'])

@st.cache_data
def impovement_recommadations(resume_test):
    output=openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{'role':'user',
              'content':f'Analyse {resume_test} and give Recommandation to imporve the resume '}])
    return (output['choices'][0]['message']['content'])

def get_score_topic(resume_text):
    resume_score = 0
    topics_covered = []
    topics_not_covered = []

    ### Predicting Whether these key points are added to the resume
    if 'Objective' or 'Summary' in resume_text:
        resume_score = resume_score + 6
        topics_covered.append(('Objective , Summary').upper())


    else:
        topics_not_covered.append(('Objective , Summary').upper())

    if 'Education' or 'School' or 'College' in resume_text:
        resume_score = resume_score + 12
        topics_covered.append(('Education , School , College').upper())
    else:
        topics_not_covered.append(('Education , School , College').upper())

    if 'EXPERIENCE' in resume_text:
        resume_score = resume_score + 16
        topics_covered.append('EXPERIENCE')

    elif 'Experience' in resume_text:
        resume_score = resume_score + 16
        topics_covered.append(('Experience').upper())
    else:
        topics_not_covered.append('EXPERIENCE')

    if 'INTERNSHIPS' in resume_text:
        resume_score = resume_score + 6
        topics_covered.append('INTERNSHIPS')
    elif 'INTERNSHIP' in resume_text:
        resume_score = resume_score + 6

    elif 'Internships' in resume_text:
        resume_score = resume_score + 6
        topics_covered.append(('Internships').upper())

    elif 'Internship' in resume_text:
        resume_score = resume_score + 6
        topics_covered.append(('Internships').upper())
    else:
        topics_not_covered.append('INTERNSHIP')

    if 'SKILLS' in resume_text:
        resume_score = resume_score + 7
        topics_covered.append('SKILLS')
    elif 'SKILL' in resume_text:
        resume_score = resume_score + 7
        topics_covered.append('SKILL')
    elif 'Skills' in resume_text:
        resume_score = resume_score + 7
        topics_covered.append(('Skills').upper())
    elif 'Skill' in resume_text:
        resume_score = resume_score + 7
        topics_covered.append(('Skill').upper())
    else:
        topics_not_covered.append('SKILLS')

    if 'HOBBIES' in resume_text:
        resume_score = resume_score + 4
        topics_covered.append('HOBBIES')
    elif 'Hobbies' in resume_text:
        resume_score = resume_score + 4
        topics_covered.append(('Hobbies').upper())
    else:
        topics_not_covered.append('HOBBIES')

    if 'INTERESTS' in resume_text:
        resume_score = resume_score + 5
        topics_covered.append('INTERESTS')
    elif 'Interests' in resume_text:
        resume_score = resume_score + 5
        topics_covered.append(('Interests').upper())
    else:
        topics_not_covered.append('INTERESTS')

    if 'ACHIEVEMENTS' in resume_text:
        resume_score = resume_score + 13
        topics_covered.append('ACHIEVEMENTS')
    elif 'Achievements' in resume_text:
        resume_score = resume_score + 13
        topics_covered.append(('Achievements').upper())
    else:
        topics_not_covered.append('ACHIEVEMENTS')

    if 'CERTIFICATIONS' in resume_text:
        resume_score = resume_score + 12
        topics_covered.append('CERTIFICATIONS')
    elif 'Certifications' in resume_text:
        resume_score = resume_score + 12
        topics_covered.append(('Certifications').upper())
    elif 'Certification' in resume_text:
        resume_score = resume_score + 12
        topics_covered.append(('Certification').upper())
    else:
        topics_not_covered.append('CERTIFICATIONS')

    if 'PROJECTS' in resume_text:
        resume_score = resume_score + 19
        topics_covered.append('PROJECTS')
    elif 'PROJECT' in resume_text:
        resume_score = resume_score + 19
        topics_covered.append('PROJECT')
    elif 'Projects' in resume_text:
        resume_score = resume_score + 19
        topics_covered.append(('Projects').upper())
    elif 'Project' in resume_text:
        resume_score = resume_score + 19
        topics_covered.append(('Project').upper())
    else:
        topics_not_covered.append('PROJECTS')

    return resume_score ,topics_covered , topics_not_covered





def run():

    st.title(":orange[*RESUME ANALYSER*]")
    c1, c2 = st.columns(2)
    with c1:
        st.header(":blue[Upload PDF]")
        pdf_file=st.file_uploader(':red[Choose your resume]',type=['pdf'])
    if pdf_file is not None:

        save_image_path = os.path.abspath(pdf_file.name)
        with c1:
                show_pdf(save_image_path)

        resume_data = ResumeParser(save_image_path).get_extracted_data()
        #st.write(resume_data['name'])
        #st.write(resume_data)
        if resume_data:
                resume_text = pdf_reader(save_image_path)
                with c2:
                    try:

                        st.write("")
                        st.write("")
                        st.write("")
                        st.write("")
                        st.write("")
                        st.write("")
                        st.write("")
                        st.write("")
                        st.write("")
                        st.write("")
                        st.subheader(':blue[INFO]')
                        name=st.text_input("Name:",resume_data['name'])
                        email=st.text_input('Email',resume_data['email'])
                        mobile_num=st.text_input('Mobile Number',resume_data['mobile_number'])
                        education=st.text_input('Qualification',resume_data['degree'])
                        Experience = st.text_input('Experience',resume_data['total_experience'])
                    except:
                        pass
                with c2:
                    ## Skills Analyzing and Recommendation


                    ds_keyword = ['data visualization', 'predictive analysis','statistical modeling',
                              'predictive model','data mining','clustering','classification',
                              'clustering & classification', 'data analytics',
                              'quantitative Analysis', 'Web Scraping', 'ml Algorithms', 'keras',
                              'Pytorch', 'probability', 'scikit-learn', 'tensorflow', "flask",
                               'streamlit','database','mysql','sql','mongodb','github',
                              'numpy','seaborn','matplotlib','pandas',]

                    web_keyword = ['react', 'django', 'node jS', 'react js', 'php', 'laravel', 'magento', 'wordpress',
                                   'javascript', 'angular js', 'c#', 'flask']
                    android_keyword = ['android', 'android development', 'flutter', 'kotlin', 'xml', 'kivy']
                    ios_keyword = ['ios', 'ios development', 'swift', 'cocoa', 'cocoa touch', 'xcode']
                    uiux_keyword = ['ux', 'adobe xd', 'figma', 'zeplin', 'balsamiq', 'ui', 'prototyping', 'wireframes',
                                    'storyframes', 'adobe photoshop', 'photoshop', 'editing', 'adobe illustrator',
                                    'illustrator', 'adobe after effects', 'after effects', 'adobe premier pro',
                                    'premier pro', 'adobe indesign', 'indesign', 'wireframe', 'solid', 'grasp',
                                    'user research', 'user experience']

                    matching_skills=[]
                    missing_skills=[]

                    for i in resume_text:
                        if i.lower() in ds_keyword:
                            reco_field = ['Data Analyst','Business Analyst','Data Science']



                    for i in resume_data['skills']:
                        if i.lower() in ds_keyword:
                            matching_skills.append(i)
                    for i in ds_keyword:
                        if i.lower() not in matching_skills:
                            missing_skills.append(i)


                    st.subheader(":blue[*Skill sets*]")
                    col1,col2=st.columns(2)
                    with col1:
                        st.markdown(
                        '''<h5 style='text-align: left; color: #1ed760;'>Skilled in : </h5>''',
                        unsafe_allow_html=True)
                        matching_skills_tags = st_tags( text='skills matching to the domain',
                                                           value=matching_skills, key='skill_match')
                    with col2:
                        st.markdown('''<h5 style='text-align: left; color: #A20B0E;'>Boost🚀 the resume with these skills:</h5>''',unsafe_allow_html=True)

                        missing_skills_tags = st_tags(label=':Skills',
                                                   text='Recommended skills generated from System',
                                                   value=missing_skills, key='skill_miss')

                    ## Resume Scorer & Resume Writing Tips
                    with c1:
                        st.subheader(":blue[**Resume Tips & Ideas ]🥂**")
                        resume_score,topics_covered,topics_not_covered=get_score_topic(resume_text)
                        col11,col12=st.columns(2)
                        with col11:
                            st.markdown(f'''<h5 style='text-align: left; color: #9EDDFF;'>[+] Awesome! You have added :\n</h4>''',unsafe_allow_html=True)
                            for i in topics_covered:
                                st.markdown(
                                    f'''<h5 style='text-align: left; color: #5CC33A;'>\t-{i}\n</h4>''', unsafe_allow_html=True)
                        with col12:
                            st.markdown(
                                f'''<h5 style='text-align: left; color: #9EDDFF;'>[-] Concentrate on these topics:</h4>''',
                                unsafe_allow_html=True)
                            for j in topics_not_covered:
                                st.markdown(
                                    f'''<h5 style='text-align: left; color: #FF6969;'>-{j}\n</h4>''', unsafe_allow_html=True)
                            st.markdown(
                                f'''<h5 style='text-align: left; color: #E9B824;'>It will give your career intension to the Recruiters.</h4>''',
                        unsafe_allow_html=True)
                    with c2:
                        st.subheader("**Resume Score 📝**")

                        st.markdown("""<style>.stProgress > div > div > div > div {background-color: #d73b5c;} </style>""",
                        unsafe_allow_html=True, )

                    ### Score Bar
                        if resume_score >70:
                            st.success('** Your Resume Writing Score: ' + str(resume_score) + '**')
                            my_bar = st.progress(resume_score)
                        elif resume_score<70:
                            st.error('** Your Resume Writing Score: ' + str(resume_score) + '**')
                            my_bar = st.progress(resume_score)

                        st.warning("** Note: This score is calculated based on the content that you have in your Resume. **")
        st.subheader(":orange[Take a look here]")
        t1,t2,t3=st.tabs(['summary','key points','Make strong'])
        with t1:
            summary_text = summarization(resume_text)
            st.subheader(":blue[Summarization Of Resume]")
            st.text(summary_text)
        with t2:
            good_bad_text = Streangth_weakness(resume_text)
            st.subheader(":blue[Strength and weekness of the resume]")
            st.text(good_bad_text)
        with t3:
            imporve_text = impovement_recommadations(resume_text)
            st.subheader(":blue[Can improve the resume with below points]")
            st.text(imporve_text)

        st.header(":red[Do you want related jobs from :blue[LinkedIn]  ?]")
        st.subheader("Where you want to relocate for job.?:")

        column1,column2,column3=st.columns([1,3,1])
        with column1:


            location = st.text_input("Location:")
        st.subheader(":green[Click here and seek jobs..!]")


        job_search=st.button('Seek Jobs')

        if 'job_search' not in st.session_state:
            st.session_state.job_search = False

        if job_search or st.session_state.job_search:
            st.session_state.job_search=True
            geocode = ''
            url1 = f'https://www.linkedin.com/jobs/search?keywords={job_role}&location={location}&geoId={geocode}&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'

            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--incognito")
            chrome_options.add_experimental_option("detach", True)
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url1)


        st.markdown(''':red[Note:]
                            :orange[Seek jobs will get to another tab ,where ] :blue[linkedin],:orange[application will open directly and land on job portal ,
                            if you want to apply , please sign in and apply for jobs]''')

    st.subheader("Detials:")
    st.write("")







print('Done')
print('Done')
run()
