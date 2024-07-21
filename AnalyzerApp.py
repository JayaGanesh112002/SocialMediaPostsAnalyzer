import boto3
import json
import pandas as pd
import streamlit as st

# Creating a session to access Lambda
session = boto3.Session(
    aws_access_key_id='Your Access Key ID',
    aws_secret_access_key='Your Secret Key',
    region_name="Your region"
    )
# Creating a Lambda client
lambda_client = session.client('lambda')

# Creating a streamlit app
st.title("Social Media Posts Trend Analyzer")

# Creating a Sidebar for easy navigation
choice = ["Post", "Trending Hashtags"]
sidebar_selectbbox = st.sidebar.selectbox("Choose an action :", options = choice, index= None)

# If Post option was selected
if sidebar_selectbbox == "Post":
    # initializes the chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # displays chat messages 
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    post = st.chat_input(placeholder = "Type your post here")

    if post:
        with st.chat_message("user"):
            st.markdown(post)

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": post})

        # inputs for the Lambda function
        payload = {
            'content':post
            }
        
        # Invoking Lambda function to store the message
        response = lambda_client.invoke(
        FunctionName='Streamlit_Post_Lambda',
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
        )
        response_payload = json.loads(response['Payload'].read().decode('utf-8'))

        with st.chat_message("assistant"):
            st.markdown(response_payload)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response_payload})

#  If the trending hashtags option was selected
elif sidebar_selectbbox == "Trending Hashtags":
    limits = {"Trending Top 5":5, "Trending Top 10":10}
    trending_choice = limits.keys()
    limit = st.selectbox("Select an option to display the Trending Hashtags :", options= trending_choice, index=None)
    if limit:
        # Invoking a lambda function to store the retrieve data from DynamoDB
        response = lambda_client.invoke(
        FunctionName='Hashtag_analyzer',
        InvocationType='RequestResponse'
        )
        response_payload = json.loads(response['Payload'].read().decode('utf-8'))
        # Displaying the output 
        df = pd.DataFrame(response_payload[:limits[limit]])
        columns = {'Counts':'No_Of_Uses'}
        df.rename(columns = columns, inplace = True)
        st.write('\n')
        st.dataframe(df)
        st.write('\n')
        st.bar_chart(df, x='Hashtag', y='No_Of_Uses')
else:
    st.write("""A quick sneakpeak on this App : \n
    This is a Social Media Posts Trend Analyzer App. The Post Analyzer App \n
    can receive a post, and check for the hashtags used. In the backend which is \n
    then stored and processed in order to analyze the trend of the hashtags used \n
    while posting in this App. \n\n
    Exapnd the left pane and Enjoy the App!!!""")