from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import os
import random as r
import json

load_dotenv()

def find_text():
    header = {
        'Accepted-Language': os.environ['ACCEPTED_LANGUAGE'],
        'User-Agent': os.environ['USER_AGENT'],
        'referer': "https://www.google.com/"}

    url = 'https://www.pornhub.com/video?o=ht&cc=world'
    response = requests.get(url=url, headers=header)
    content = response.text

    soup = BeautifulSoup(content, "html.parser")
    links = soup.select("a.linkVideoThumb")
    selected_link = f"https://www.pornhub.com{r.choice(links).get('href')}"

    subheader = {
        'Accepted-Language': os.environ['ACCEPTED_LANGUAGE'],
        'User-Agent': os.environ['USER_AGENT'],
        'referer': url}

    response = requests.get(url=selected_link, headers=subheader)
    content = response.text

    soup = BeautifulSoup(content, "html.parser")
    comment_container = soup.select_one("div.videoViewPage")
    comment_blocks = comment_container.select("div.topCommentBlock")
    selected_block = r.choice(comment_blocks)
    selected_text = selected_block.select_one('div.commentMessage>span').getText()
    selected_speaker = selected_block.select_one('div.usernameWrap a[data-label="Profile View"]').getText()

    if "commentMessage" not in selected_text:
        print("Comment found!")
        return selected_text, selected_speaker
    else:
        print("Retrying...")
        return find_text()

class Post:
    def __init__(self, upvote=0, message=None, speaker=None):
        self.upvote = upvote
        self.message = message
        self.speaker = speaker
    def random_draw(self):
        self.message, self.speaker = find_text()


class PostMaster:
    def __init__(self):
        self.quote_list = []  # List of Post objects
        self.load_info()

    def save_info(self):
        dict_quote = {i: {'speaker': entry.speaker, 'message': entry.message, 'upvote': entry.upvote} for i, entry in
                      enumerate(self.quote_list)}
        with open(file="all_posts.json", mode="w", encoding='utf-8') as overwrite_file:
            json.dump(dict_quote, overwrite_file, indent=4)

    def load_info(self):
        with open(file="all_posts.json", mode="r", encoding='utf-8') as file:
            content = json.load(file)
        for entry in content.values():
            new_post = Post(
                upvote=entry['upvote'],
                message=entry['message'],
                speaker=entry['speaker']
            )
            self.quote_list.append(new_post)

    def add_entry(self):
        new_post = Post()
        new_post.random_draw()
        self.quote_list.append(new_post)
        return new_post


if __name__ == "__main__":
    my_postmaster = PostMaster()
    for entry in my_postmaster.quote_list:
        print(f"{entry.speaker}: {entry.message}.\n {entry.upvote} upvotes")