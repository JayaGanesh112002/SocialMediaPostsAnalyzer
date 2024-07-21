In the era of social media dominance, users crave platforms that offer seamless posting experiences while also providing insights into trending topics. To address this need, we aim to develop a Streamlit application that allows users to compose and publish posts, same as popular social media platforms. This application will integrate with AWS Lambda and DynamoDB to facilitate post processing and hashtag analysis. <br><br>

<strong>Tools used : Python, AWS Lambda, Dynamodb, Streamlit</strong><br><br>

<h3>Basic Workflow :</h3>
1. Either Post or Get the analysis on trending hashtags<br>
>> If Post is selected:<br>
>> 2. Compose and post your message with hashtags<br>
>> 3. On posting, an AWS Lambda function will be triggered and the post will be stored in a DynamoDB table and the hashtags will be stored in a seperate DynamoDB Table. Thus, securing the integrity of posts and easily maintaining the hashtags for analysis.<br><br>
>> If Trending Hashtags option is selected :<br>
>> 2. You can either view the Top 5 or Top 10 hashtags that are trending.<br>
>> 3. On selecting the option, an AWS Lambda function is triggered which will fecth the rquired data.<br><br>

> [!CAUTION]
> <strong>Note : <br>
> 1.Make sure you enter appropriate AWS User credentials for Lambda function.<br>
> 2.Feel free to change the DynamoDB table name and Lambda function names as per your needs before executing.<br>
> 3.Make sure you've installed the following packages : Streamlit, Pandas and Boto3.<br>
