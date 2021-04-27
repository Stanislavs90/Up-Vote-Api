Intro:
    An api that allows users to make a post, and upvote a post.
    Authentication feature also included.



Setup:

   python3 -m venv venv
   
   source env/bin/activate

   pip install -r requirements.txt

   cd into directory 

   python manage.py createsuperuser

   python manage.py runserver

Overview: 

    Navigate to http://127.0.0.1:8000/api/posts to view or create posts

    http://127.0.0.1:8000/api/posts/<int:pk> to delete posts

    http://127.0.0.1:8000/api/posts/<int:pk>/vote to vote on posts

    To vote use must be logged in , to do so push log in button on top right corner
    when on http://127.0.0.1:8000/api/posts

