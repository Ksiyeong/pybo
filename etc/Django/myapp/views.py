from django.http import HttpResponse
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt

Now_id = 4
topics = [
    {'id':1, 'title':'Create', 'body':'Create is ..'},
    {'id':2, 'title':'Read', 'body':'Read is ..'},
    {'id':3, 'title':'Update', 'body':'Update is ..'},
    {'id':4, 'title':'Delete', 'body':'Delete is ..'}
]

def HTMLTemplate(articleTag, id=None):
    global topics
    mybtn = ''
    if id != None:
        mybtn = f'''
        <li><a href="/update/{id}">update</a></li>
        <li>
            <form action="/delete/" method="POST">
                <input type="hidden" name="id" value={id}>
                <input type="submit" value="delete">
            </form>
        </li>
        '''
    ol = ''
    for topic in topics:
        ol += f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'
    return f'''
    <html>
    <body>
        <h1><a href="/">Django</a></h1>
        <ul>
            {ol}
        </ul>
            {articleTag}
        <ul>
            <li><a href="/create/">create</a></li>
            {mybtn}
        </ul>
    </body>
    </html>
    '''

def index(request):
    article = '''
    <h2>Welcome!</h2>
    This is Home.
    '''
    return HttpResponse(HTMLTemplate(article))

def read(request, id):
    global topics
    for topic in topics:
        if topic['id'] == int(id):
            article = f'''
            <h2>{topic['title']}</h2>
            {topic['body']}
            '''
            return HttpResponse(HTMLTemplate(article, id))

@csrf_exempt
def create(request):
    if request.method == "GET":
        article = '''
        <form action="/create/" method="POST">
            <p><input type="text" name="title" placeholder="title"></p>
            <p><textarea placeholder="body" name="body"></textarea></p>
            <p><input type="submit"></p>
        </form>
        '''
        return HttpResponse(HTMLTemplate(article))
    elif request.method == "POST":
        global topics
        global Now_id
        title = request.POST["title"]
        body = request.POST["body"]
        Now_id += 1
        New = {"id":Now_id, "title":title, "body":body}
        topics.append(New)
        return redirect(f'/read/{Now_id}')

@csrf_exempt
def update(request, id):
    global topics
    if request.method == "GET":
        for topic in topics:
            if topic["id"] == int(id):
                title = topic["title"]
                body = topic["body"]
                article = f'''
                <form action="/update/{id}/" method="POST">
                    <p><input type="text" name="title" placeholder="title" value="{title}"></p>
                    <p><textarea placeholder="body" name="body">{body}</textarea></p>
                    <p><input type="submit"></p>
                </form>
                '''
                return HttpResponse(HTMLTemplate(article, id))
    elif request.method == "POST":
        title = request.POST["title"]
        body = request.POST["body"]
        for topic in topics:
            if topic["id"] == int(id):
                topic["title"] = title
                topic["body"] = body
                return redirect(f'/read/{id}')

@csrf_exempt
def delete(request):
    if request.method == "POST":
        id = request.POST["id"]
        global topics
        New_topics = []
        for topic in topics:
            if topic['id'] != int(id):
                New_topics.append(topic)
        topics = New_topics
        return redirect('/')