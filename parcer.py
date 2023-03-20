import json
import vk_api
import re
import pandas as pd


def get_owner_id(link):
    short_name = re.sub(r'https://vk.com/', '', link)
    api_req = vk.groups.getById(group_id=short_name, v=5.131)
    req_json = json.dumps(api_req[0], ensure_ascii=False)
    req_py = json.loads(req_json)
    owner_id = "".join(["-", str(req_py["id"])])
    return owner_id


def get_posts(link):
    owner = get_owner_id(link)
    posts = list()
    wall = vk.wall.get(owner_id=int(owner), count=150, v=5.131)
    for post in wall['items']:
        posts.append(post['id'])
    return posts


def get_comments(link, post_ids):
    owner = get_owner_id(link)
    comments = list()
    comments_id = list()
    for post_id in post_ids:
        post_comments = vk.wall.getComments(owner_id=int(owner), post_id=int(post_id), thread_items_count=10, v=5.91)
        for post_comment in post_comments['items']:
            comments_id.append(post_comment['id'])
            comments.append(post_comment['text'])
            try:
                replies = vk.wall.getComments(owner_id=int(owner), post_id=int(post_id), comment_id=post_comment['id'], v=5.91)
                if replies['count'] != 0:
                    for reply in replies['items']:
                        comments.append(reply['text'])
            except vk_api.exceptions.VkApiError:
                print('ApiError')
    return comments


if __name__ == "__main__":
    gr_urls = [r"https://vk.com/altaikrai_ldpr", ]  # r"https://vk.com/barneos22", r"https://vk.com/chb_brn",
    # r"https://vk.com/leftbiysk", r"https://vk.com/incident22",
    token = "ca62f3d9ca62f3d9ca62f3d9c7ca1ea088cca62ca62f3d9a8077c79d0ec187ff848d27c"
    vk_session = vk_api.VkApi()
    vk_session.token = {'access_token': token, 'expires_in': 0}
    vk = vk_session.get_api()
    print("Список групп:")
    i=5  # 1
    for u in gr_urls:
        print(u)
    for url in gr_urls:
        print("Начат сбор данных для сообщества: " + url)
        all_posts = get_posts(url)
        posts_comments = get_comments(url, all_posts)
        group_series = pd.Series(posts_comments, copy=False, dtype=object)
        print("Собраны комментарии для сообщества: " + url)
        name = str(i) + '.csv'
        # i+=1
        group_series.to_csv(name)
        print(name)

