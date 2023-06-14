import configparser
import csv
import json
import os
import praw
from prawcore.exceptions import Forbidden

counter = 1
comment_file_name = "input/saved_comments_test.csv"

# Read the configuration file
config = configparser.ConfigParser()
config.read('settings.ini')


reddit_client = config['reddit_client']
reddit = praw.Reddit(client_id=reddit_client['client_id'],
                    client_secret=reddit_client['client_secret'],
                    user_agent=reddit_client['user_agent'])

quarantined_section = config['quarantined']
for quarantined_subreddit in quarantined_section:
    reddit.subreddit(quarantined_subreddit).quaran.opt_in()

def make_json_saver():
    obj_list = []
    def save_json(obj):
        if obj != None:
            obj_list.append(obj)
        return obj_list
    return save_json
# Saves json to a list and returns the list
save_json = make_json_saver()

def save_to_json(dict_list):
    filename = "saved_data/saved_comments_json.json"
    
    if os.path.exists(filename) and os.path.getsize(filename) > 0:  # check if file exists and is not empty
        with open(filename, 'r') as f:
            data = json.load(f)
        data.extend(dict_list)
    else:
        data = dict_list  # if file does not exist or is empty, start with your new data

    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def get_next_five_replies(comment):
    try:    # Ensure we're working with the most up-to-date comment structure
        comment.refresh()

        # comment.replies.list() flattens the structure
        flat_comments = comment.replies.list()

        # If there are at least five comments, return the first five
        if len(flat_comments) >= 5:
            return flat_comments[:5]
        # Otherwise, return all available comments
        else:
            return flat_comments
    except praw.exceptions.ClientException as e:
        print(f"{e}\n5 next comments excluded\n")
        return None
    except Exception as e:
        print(f"{e}\n5 next comments excluded\n")
        return None

def count_lines(filename="saved_comments.csv"):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        row_count = sum(1 for row in reader)
        return row_count


def comment_to_dict(comment):
    replies = get_next_five_replies(comment)
    next_comments = [{'body': reply.body, 'author': str(reply.author), 'score': reply.score} for reply in replies] if replies is not None else []
    try:
        return {
            'body': comment.body,
            'author': str(comment.author),
            'score': comment.score,
            'id': comment.id,
            'created': comment.created_utc,
            'subreddit': comment.subreddit.display_name,
            'permalink': comment.permalink,
            'subreddit': str(comment.subreddit),
            'five_next_comments': next_comments,
            'body_html': comment.body_html,
            "post_info": {
            "title": comment.submission.title,
            "post_selftext": comment.submission.selftext,
            "post_id": comment.submission.id,
            "post_score": comment.submission.score,
            "post_url": comment.submission.url,
            "post_permalink": comment.submission.permalink,
            }
        }
    except praw.exceptions.ClientException as e:
        print(f"{e}\n{comment.id} not saved")
        return None


        
with open(comment_file_name, 'r') as f:
    reader = csv.reader(f)
    line_counter = count_lines(comment_file_name)
    print(f"\nThere are {line_counter} lines in the file\n\n")
    next(reader)  # Skip header
    for row in reader:
        # Save to file if there are more than 50 saved comments
        if len(save_json(None)) >= 50:
            save_to_json(save_json(None))
        comment_id = row[0]
        try:
            print(f"Saving number {counter}/{line_counter} id: {comment_id}")
            comment = reddit.comment(id=comment_id)
            comment_dict = comment_to_dict(comment)
            #pprint(dict(comment_dict.items()))
            save_json(comment_dict)
        except Forbidden:
            print(f"Access forbidden for comment with id: {comment_id}")
        except Exception as e:
            print(f"{e}\n Something went wrong, comment with id: {comment_id} not saved")
        finally: counter += 1

save_to_json(save_json(None))
print("\nAll done!\n")

