# post_comment_downloader
Download saved comments and saved posts.


How
Make new reddit app here
https://www.reddit.com/prefs/apps
remember id and secret

Get all saved posts and coments
(Se have to get it here, as reddit api only serves the last 1000 saved items)
https://www.reddit.com/settings/data-request
GDPR request works
In this folder there will be a saved_posts.csv and a saved_comments.csv file. 
we need both for later


Download post_comment_downloader
You will need python3 and praw (reddit api framework).
Insert app id and secret in the settings_template.ini file.
rename file to settings.ini

In terminal run createfolders.py

move saved_posts.csv and saved_coments.csv (the files from the data request) to input folder

Then to download all posts run 
save_posts.py

to download all comments run
save_comments.py

This will take a long time. Atleast 2 sec for each post, and 6 for each comment.
the saved data will apear in json format in saved_data

# post_comment_downloader
This Python script allows you to download saved posts and comments from Reddit.

## Setup Instructions

1. **Create a new Reddit app:** Go to [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps) and create a new app. Note down the 'id' and 'secret' values.

2. **Request your data from Reddit:** You need to do this because the Reddit API only serves the last 1000 saved items. Visit [https://www.reddit.com/settings/data-request](https://www.reddit.com/settings/data-request) and make a GDPR request. After it's processed, download the files 'saved_posts.csv' and 'saved_comments.csv'.

3. **Install post_comment_downloader:** Clone this repository to your local machine. Ensure you have Python3 and praw (a Python Reddit API Wrapper) installed. 

4. **Configure Settings:** Open the 'settings_template.ini' file and insert your Reddit app's 'id' and 'secret'. Save this file as 'settings.ini'.

5. **Prepare Folders:** Run `createfolders.py` to generate the necessary directories for the script.

6. **Move Data Files:** Move the 'saved_posts.csv' and 'saved_comments.csv' files (from the data request) to the 'input' folder.

## Usage

To download all saved posts, run:

```bash
python3 save_posts.py

To download all saved comments, run:

bash

python3 save_comments.py

Please note that downloading can take some time, at least 2 seconds per post and 6 seconds per comment due to Reddit's rate limits.
