import praw
import csv
import json
from prawcore.exceptions import Forbidden, NotFound
import configparser


saved_posts_file = "input/saved_posts_test.csv"
not_saved = []
counter = 1
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
# Call with None for list
save_json = make_json_saver()



# Get the 'Fields' section
fields = config['Fields_To_Store']

def submission_to_dict(submission):
    result = {}

    for field, should_include in fields.items():
        if config.getboolean('Fields_To_Store', field):  # this returns True if field value is 'true', False otherwise
            if field == "subreddit":
                subreddit_name = submission.subreddit.display_name
                result[field] = str(subreddit_name)
            else:
                result[field] = getattr(submission, field, None)  # gets the attribute from the submission if it exists, otherwise returns None
            
            
    return result

def save_saved_list_json(list):
    data = []
    
    data.append(list)
    with open('saved_data/saved_posts_json.json', 'w') as f:
        json.dump(list, f, indent=4)

def count_lines(filename="saved_posts.csv"):
    start_counting = False
    line_counter = 0
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for line_num, row in enumerate(reader, start=1):
            if start_counting:
                line_counter += 1
            elif "id" in row[0]:
                start_counting = True
    return line_counter

def save_not_saved(not_saved):
    with open('saved_data/not_saved_posts.json', 'w') as f:
        json.dump(not_saved, f, indent=4)

with open(saved_posts_file, 'r') as f:
    reader = csv.reader(f)
    posts_count = count_lines(saved_posts_file)
    print(f"There are {posts_count} posts to save\n\n")
    next(reader)  # Skip header
    for row in reader:
        post_id = row[0]
        post = reddit.submission(id=post_id)
        try:
            print(f'Count: {counter}/{posts_count}\nTitle: {post.title}\nSubreddit: {post.subreddit}\n')
            save_json(submission_to_dict(post))
        except Forbidden:
            print(f"Access forbidden for post with id: {post_id}\n")
            not_saved.append(row)
        except NotFound:
            print(f"404: {post_id} data not found!")
            not_saved.append(row)
        except Exception as e:
            print("Other exception")
            print(f"{e}")
            not_saved.append(row)
        finally:
            counter += 1

save_saved_list_json(save_json(None))
save_not_saved(not_saved)


