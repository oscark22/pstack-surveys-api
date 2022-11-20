from fastapi import Body, FastAPI

from models import Comment
from database import Database


app = FastAPI()
db = Database()


@app.get('/loved_languages')
async def get_all_loved_languages():
    return db.read_question_data(6)
    
@app.get('/loved_languages/{limit}')
async def get_most_loved_languages(limit: int):
    return db.read_question_data_with_limit(6, limit)

@app.get('/loved_databases')
async def get_all_loved_databases():
    return db.read_question_data(8)

@app.get('/loved_databases/{limit}')
async def get_most_loved_databases(limit: int):
    return db.read_question_data_with_limit(8, limit)

@app.get('/loved_frameworks')
async def get_all_loved_frameworks():
    return db.read_question_data(9)

@app.get('/loved_frameworks/{limit}')
async def get_most_loved_frameworks(limit: int):
    return db.read_question_data_with_limit(9, limit)

@app.get('/comments')
async def get_all_comments():
    return db.read_comments_data()

@app.get('/comments/{limit}')
async def get_most_recent_comments(limit):
    return db.read_comments_data(limit)

@app.post('/comments')
async def post_comment(comment: Comment):
    return db.create_new_comment(comment.user_id, comment.text)

@app.put('/comments/{comment_id}')
async def put_comment(comment_id: int, comment: Comment):
    return db.update_comment(comment_id, comment.text)

@app.delete('/comments/{comment_id}')
async def delete_comment(comment_id: int):
    return db.delete_comment(comment_id)
