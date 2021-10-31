import io
import re
import uuid
import pickle
import json
import os
import base64
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

st.title('Interactive plots using streamlit')


def download_button(object_to_download, download_filename, button_text, pickle_it=False):
    """
    Generates a link to download the given object_to_download.

    Params:
    ------
    object_to_download:  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv,
    some_txt_output.txt download_link_text (str): Text to display for download
    link.
    button_text (str): Text to display on download button (e.g. 'click here to download file')
    pickle_it (bool): If True, pickle file.

    Returns:
    -------
    (str): the anchor tag to download object_to_download

    Examples:
    --------
    download_link(your_df, 'YOUR_DF.csv', 'Click to download data!')
    download_link(your_str, 'YOUR_STRING.txt', 'Click to download text!')

    """
    if pickle_it:
        try:
            object_to_download = pickle.dumps(object_to_download)
        except pickle.PicklingError as e:
            st.write(e)
            return None

    else:
        if isinstance(object_to_download, bytes):
            pass

        elif isinstance(object_to_download, pd.DataFrame):
            object_to_download = object_to_download.to_csv(index=False)

        # Try JSON encode for everything else
        else:
            object_to_download = json.dumps(object_to_download)

    try:
        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(object_to_download.encode()).decode()

    except AttributeError as e:
        b64 = base64.b64encode(object_to_download).decode()

    button_uuid = str(uuid.uuid4()).replace('-', '')
    button_id = re.sub('\d+', '', button_uuid)

    custom_css = f""" 
        <style>
            #{button_id} {{
                border: 0;
                font-size: 16px;
                font-weight: bold;
                padding: 10px 30px;
                border-radius: 50px;
                color: white;
                outline: none;
                position: relative;
                text-decoration: none;
            }} 

            #{button_id}:before {{
                content: '';
                display: block;
                background: linear-gradient(to left, rgba(255, 255, 255, 0) 50%, rgba(255, 255, 255, 0.4) 50%);
                background-size: 210% 100%;
                background-position: right bottom;
                height: 100%;
                width: 100%;
                position: absolute;
                top: 0;
                bottom:0;
                right:0;
                left: 0;
                border-radius: 50px;
                transition: all 1s;
                -webkit-transition: all 1s;
            }}

            #{button_id} {{
                background-image: linear-gradient(to right, #6253e1, #852D91);
                box-shadow: 0 4px 15px 0 rgba(236, 116, 149, 0.75);
            }}
            
            #{button_id}:hover:before {{
                background-position: left bottom;
            }}
        </style> """

    dl_link = custom_css + \
        f'<a download="{download_filename}" id="{button_id}" href="data:file/txt;base64,{b64}">{button_text}</a><br></br>'

    return dl_link


def y_pred(F, R, C, a, b): return (R*pow(10, a)) / \
    (1+1j*2*3.14*F*(R*pow(10, a))*(C*pow(10, b)))


def log(x): return np.log(x)/np.log(10)


def save_fig(plt):
    return st.pyplot(plt)


@st.cache(suppress_st_warning=True)
def expensive_computation(F, y_p, r, i, R, C, a, b):
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_figheight(6)
    fig.set_figwidth(15)
    ax1.plot(log(F), log(y_p.real), color='r')
    ax1.plot(log(F), log(r), color='k', marker="*",
             linestyle='', markersize=10)
    ax1.set_title("Real: R-value : "+str(R)+"e^" + str(a) +
                  " C-value : "+str(C)+"e^"+str(b), fontsize=12)

    ax2.plot(log(F), log(y_p.imag), color='b')
    ax2.plot(log(F), log(i), color='c', marker="*",
             linestyle='', markersize=10)
    ax2.set_title("Imaginary: R-value : "+str(R) +
                  "e^"+str(a)+"C-value : "+str(C)+"e^"+str(b), fontsize=12)
    st.pyplot(fig)
    # if st.button('Download Pic'):
    #     fig.savefig("export1.png")
    st.write("")
    filename = 'export_'+str(np.random.randint(10**5, 10**6))+'.png'
    plot2 = io.BytesIO()
    plt.savefig(plot2, format='png', bbox_inches="tight")
    download_button_str = download_button(
        plot2.getvalue(), filename, f'Download figure as .png file', pickle_it=False)
    st.markdown(download_button_str, unsafe_allow_html=True)
    plt.show()
    time.sleep(2)
    return plt

# def download_pic(plt):
#     if st.button('Download Pic'):
#         result = 10
#         st.write('result: %s' % result)


val, df, target, tType, Real, Img = False, None, None, None, None, None
step = 0

if step not in [1] and step == 0:
    if val == False:
        val = st.file_uploader('File uploader')
    if val:
        # st.write(val.name)
        # download = st.button('Download Excel File')
        # if download:
        #     'Download Started!'
        #     liste = ['A', 'B', 'C']
        #     df_download = pd.DataFrame(liste)
        #     df_download.columns = ['Title']
        #     df_download

        if val.name.split(".")[1] == "xlsx" or val.name.split(".")[1] == "xls":
            df = pd.read_excel(val.name)
            step = 1
        elif val.name.split(".")[1] == "csv":
            df = pd.read_csv(val.name)
            step = 1
        else:
            st.write("Invalid file Type")
            step = 0
if step == 1:
    st.write("file uploaded successfully")
    eqn = st.text_input("enter the equation: ")
    constants = st.text_input("enter the constants separated with comma: ")
    variables = st.text_input("enter the variables separated with comma: ")

    const_dict = {}
    var_dict = {}

    if len(eqn) >= 1 and len(constants) >= 1 and len(variables) >= 1:
        for i in constants.split(","):
            const_dict[i] = 0

        for i in variables.split(","):
            var_dict[i] = None

        # for i in const_dict.keys():
        #     temp = ""
        #     while len(temp)==0:
        #         temp = st.text_input("Enter the value of "+str(i)+": ",key = "const_dict-"+str(i))
        #     const_dict[i] = float(temp)

        # for i in var_dict.keys():
        #     temp = ""
        #     while len(temp)==0:
        #         temp = st.text_input("Enter the value of "+str(i)+": ",key = "var_dict-"+str(i))
        #         step = 2
        #     var_dict[i] = float(temp)

        for i in const_dict.keys():
            exec("%s = %f" % (i, const_dict[i]))
            step = 2

        # for i in var_dict.keys():
        #     exec("%s = %f"%(i,var_dict[i]))

# R/(1+1j*2*3.14*R*F*C)

if step == 2:
    tType = st.radio(
        "Target Type",
        ("None", 'Real', 'Complex'))

    if tType not in "None":
        if tType in "Complex":
            Real = st.selectbox("select the Real Part of the Target Variable", [
                                    None, *list(df.columns)])
            Img = st.selectbox("select the Imaginary Part of the Target Variable", [
            None, *list(df.columns)])
        elif tType in "Real":
            if not target:
                target = st.selectbox("select the target variable", [
                                    None, *list(df.columns)])

    if target != None or (Real != None and Img):
        if tType in "Complex":
            Real = df[Real].values
            Img = df[Img].values
            # st.write(Real+Img*1j)
        elif tType in "Real":
            target = df[target].values
            st.write(target)
        for i in var_dict.keys():
            if var_dict[i] == None:
                var_dict[i] = st.selectbox(
                    "match for the independent variable "+str(i), [None, *list(df.columns)])
                if var_dict[i] != None:
                    var_dict[i] = df[var_dict[i]].values
                    globals()[i] = var_dict[i]
        try:
            none_check = [sum(i == None) for i in var_dict.values()]
            if sum(np.array(none_check)) == 0:
                step = 3
        except:
            pass
if step == 3:
    st.container()
    col1, col2 = st.columns(2)

    for i in const_dict.keys():
        val = col1.slider(i+' value', -100, 100, 0)
        power = col2.slider('10th power of '+i, -100, 100, 0)
        globals()[i] = val * pow(10, power)

    pred = eval(eqn)

    if tType in "Complex":
        col1, col2 = st.columns(2)
        
        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.set_figheight(6)
        fig.set_figwidth(15)
        ax1.plot(log(globals()[list(var_dict.keys())[0]]), log(pred.real), color='r')
        ax1.plot(log(globals()[list(var_dict.keys())[0]]), log(Real), color='k', marker="*",
                linestyle='', markersize=10)
        ax1.set_title("Real", fontsize=12)

        ax2.plot(log(globals()[list(var_dict.keys())[0]]), log(pred.imag), color='b')
        ax2.plot(log(globals()[list(var_dict.keys())[0]]), log(Img), color='c', marker="*",
                linestyle='', markersize=10)
        ax2.set_title("Imaginary", fontsize=12)
        plt = fig
        
    elif tType in "Real":
        plt.plot(globals()[list(var_dict.keys())[0]], target, color='r')
        plt.plot(globals()[list(var_dict.keys())[0]], pred, color='k',
                marker="*", linestyle='', markersize=10)
    st.pyplot(plt)
    # if st.button('Download Pic'):
    #     fig.savefig("export1.png")
    st.write("")
    filename = 'export_'+str(np.random.randint(10**5, 10**6))+'.png'
    plot2 = io.BytesIO()
    plt.savefig(plot2, format='png', bbox_inches="tight")
    download_button_str = download_button(
        plot2.getvalue(), filename, f'Download figure as .png file', pickle_it=False)
    st.markdown(download_button_str, unsafe_allow_html=True)
    plt.show()
