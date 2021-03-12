## Django Rest Api Blog

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all requirements.

```bash
pip install -r requirements.txt
```


## Usage

To run local server

```bash
python manage.py runserver
```

### Urls

/users = User creation - returns token for authorization

/posts = Get or Post posts

/posts/id/like/ Like post with method POST

/posts/id/unlike/ Unlike post with method POST

/posts/id/favor/ Add post to favourites with method POST

/posts/id/unfavour/ Delete post from favourites

/posts/favourites See current user's favourites posts

### Filters
You may use addition parameters to get post you want <br>
Examples: <br>
/posts?hashtags=first,second&likes=5

/posts?likes_gte=10&pub_date__gte=2021-03-12