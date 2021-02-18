# THIS IS A COMIC API

## Set Up 

## Git Cloning Repo

git clone git@github.com:codertjay/Muse.git
#
cd Muse

## Activation Virtualenv
pip -h
#
pip install virtualenv
#
virtualenv env

## if you are using windows
env\Scripts\activate.bat
# else
source env/bin/activate

# installing packages ( make sure you are in the root folder)
pip install -r  requirements.txt


#                                            Api calls
### Comic list

#### http://127.0.0.1:8000
parameters can also be applied to filter through the comics 
_http://127.0.0.1:8000/comic/?ordering=view_count_ :`ascending view count ` <br/>
_http://127.0.0.1:8000/comic/?ordering=-view_count_ :`descending viewcount `<br/>
_http://127.0.0.1:8000/comic/?tag=Romance_ :`filter through tags ( To view list of tags we get it from ` `http://127.0.0.1:8000/comic_tags` )<br/>


#### this returns all the comic list 
[
    {
        "user": {
            "username": "demo4",<br/>
            "email": "begintjay@gmail.com",<br/>
            "first_name": "demo1",<br/>
            "last_name": "demo1"
        },<br/>
        "title": "helllo",<br/>
        "tag": "Action",<br/>
        "view_count": 2,<br/>
        "description": "dd",<br/>
        "timestamp": "2021-02-16T21:23:53.880610Z",<br/>
        "thumbnail": "http://127.0.0.1:8000/media/Screenshot_2021-02-07_132533_KBD0RxJ.jpg",<br/>
        "episode_count": 0,<br/>
        "comment_count": 1,<br/>
        "comic_detail_url": "http://127.0.0.1:8000/comic/helllo/",<br/>
        "comic_delete_url": "http://127.0.0.1:8000/comic/helllo/delete/",<br/>
        "comic_update_url": "http://127.0.0.1:8000/comic/helllo/update/"<br/>
    }....
]

## comic detail

### http://127.0.0.1:8000/comic/<str: slug>/ <br/>
The comic url uses slug field to ge the detail but you can also get the detail url from 
the comic list <br/>
The comic detail returns
{
    "id": 1,<br/>
    "slug": "helllo",<br/>
    "user": {
        "username": "demo4",<br/>
        "email": "begintjay@gmail.com",<br/>
        "first_name": "demo1",<br/>
        "last_name": "demo1"
    },<br/>
    "title": "helllo",<br/>
    "tag": "Action",<br/>
    "view_count": 4,<br/>
    "description": "dd",<br/>
    "timestamp": "2021-02-16T21:23:53.880610Z",<br/>
    "thumbnail": "http://127.0.0.1:8000/media/Screenshot_2021-02-07_132533_KBD0RxJ.jpg",<br/>
    "episode": [],<br/>
    "episode_count": 0,<br/>
    "comment": [
        {
            "user": {
                "username": "demo4",<br/>
                "email": "begintjay@gmail.com",<br/>
                "first_name": "demo1",<br/>
                "last_name": "demo1"
            },<br/>
            "id": 1,<br/>
            "content": "helllo",<br/>
            "reply_count": 1,<br/>
            "like": [],<br/>
            "dislike": [],<br/>
            "replies": [
                {
                    "user": {
                        "username": "demo4",<br/>
                        "email": "begintjay@gmail.com",<br/>
                        "first_name": "demo1",<br/>
                        "last_name": "demo1"
                    },<br/>
                    "id": 2,<br/>
                    "content": "helllo",<br/>
                    "timestamp": "2021-02-16T21:48:26.033127Z"
                }
            ],<br/>
            "timestamp": "2021-02-16T21:47:57.044172Z",<br/>
            "comment_delete_url": "http://127.0.0.1:8000/comment/1/delete/",<br/>
            "comment_update_url": "http://127.0.0.1:8000/comment/1/update/",<br/>
            "comment_detail_url": "http://127.0.0.1:8000/comment/1/"
        }
    ],<br/>
    "comment_count": 1
}

## Comic update 
 url  `http://127.0.0.1:8000/comic/<str: slug>/update` <br/>
 comic update fields  `title, tag,description ,thumbnail` and the token ` which should be sent through the authentication header`  <br/>
 Note we are using token authentication  so the user has to be authenticated to update his comic  <br/>

## Comic create 
 url  `http://127.0.0.1:8000/comic_create` <br/>
 comic update fields  `title, tag,description ,thumbnail` and the token ` which should be sent through the authentication header`  <br/>
 Note we are using token authentication  so the user has to be authenticated to update his comic and you have to be the owner of the comic <br/>

## Comic delete 
 url  `http://127.0.0.1:8000/comic/<str: slug>/delete` <br/>
 comic update fields  `title, tag,description ,thumbnail` and the token ` which should be sent through the authentication header`  <br/>
 Note we are using token authentication  so the user has to be authenticated to update his comic and you have to be the owner of the comic <br/>


## channel list 
### http://127.0.0.1:8000/channel <br/>
This returns list of channels base on publishers
[
    {
        "id": 5,<br/>
        "channel_detail_url": "http://127.0.0.1:8000/channel/codertjay/",<br/>
        "follower_count": 0,<br/>
        "about": "hello my name is favour i am a publisher",<br/>
        "profileImage": "http://127.0.0.1:8000/media/Profile/Screenshot_2021-01-18_222236_dproKH6.jpg",<br/>
        "backgroundImage": "http://127.0.0.1:8000/media/Background/Screenshot_2021-01-18_222236_if7q2TN.jpg",<br/>
        "user": "codertjay"
    }......
]

## channel detail
http://127.0.0.1:8000/channel/<str: username>/  `which could be http://127.0.0.1:8000/channel/codertjay  in here  codertjay is the username` <br/>

## channel follow
http://127.0.0.1:8000/channel_follow/  ` in here you have to send the username of the channel user to this url and you have to be autheticated ` <br/>

## channel unfollow
http://127.0.0.1:8000/channel_unfollow/  ` in here you have to send the username of the channel user to this url and you have to be autheticated ` <br/>


## channel or profile  update 
http://127.0.0.1:8000/user/<str: username>/ `to update a channels fields to be passes should be`

