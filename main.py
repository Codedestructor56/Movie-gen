from flask import Flask, render_template, request, redirect, url_for, session
import openai

app=Flask(__name__)

openai.api_key = 'YOUR_API_KEY'

def prompt_creator(genre,description,num=1):
  if num==1:
    return f'Give me the name of a {genre} movie about {description} in a python list\n\nname:'
  elif num>1:
    return f'Give me the names of {num} {genre} movies about{description} in a python list\n\nnames:'

def res_gen(prompt,temp=0.7):
  response = openai.Completion.create(
    model="text-davinci-002",
    prompt=prompt,
    temperature=temp,
    max_tokens=964,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )
  return response['choices'][0]['text'].strip('\n\n').split('\n')

@app.route('/')
def home():
  return render_template('base.html')

@app.route('/generate',methods=['GET','POST'])
def generate():
  if request.method=='POST':
    genre = request.form['genre']
    description = request.form['description']
    numbers= int(request.form['new_num'])
    rand_num=int(request.form['rand_num'])
    print(genre,description, numbers)
    gen=res_gen(prompt_creator(genre,description,numbers),rand_num/10)
    return render_template('generate.html',user=gen)

if __name__=='__main__':
  app.run(debug=True)
