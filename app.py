from flask import Flask, render_template ,request, redirect, session, Markup
import psycopg2
from html import escape
import os
import openai
from make_image import create_image
import os
app = Flask(__name__)


@app.route('/')
def index():

    return render_template('index.html')



@app.route("/result",  methods=['GET', 'POST']) # POSTメソッドに対応した処理
def insert():

            if request.method == 'POST':
                # index.htmlのフォームから質問文を入手する

                select_font = request.form['select_font']
                                
                if select_font == 'a':
                    select_font = "./static/fonts/YuGothM.ttc"
                elif select_font == 'b':
                    select_font = "./static/fonts/msmincho.ttc"
                elif select_font == 'c':
                    select_font = "./static/fonts/HGRSMP.TTF"
                    
                select_colors = request.form['select_color']

                select_color = tuple(map(int, select_colors.strip('()').split(', ')))

                #入力値を変数化

                title = escape(request.form['title'])
                a_length_text = escape(request.form['length_text'])
                a_length_plot = escape(request.form['length_plot'])
                a_category = escape(request.form['category'])
                a_hero = escape(request.form['hero'])
                a_cast1 = escape(request.form['cast1'])
                a_cast2 = escape(request.form['cast2'])
                a_cast3 = escape(request.form['cast3'])
                a_story_term = escape(request.form['story_term'])
                a_keywords1 = escape(request.form['keywords1'])
                a_keywords2 = escape(request.form['keywords2'])
                a_keywords3 = escape(request.form['keywords3'])
                a_language = escape(request.form['language'])

                conn = psycopg2.connect(
                    host="localhost",
                    database="StoriesAI",
                    user="・・・",
                    password="・・・"
                )

                cursor = conn.cursor()

                #プロンプト文の作成

                text = title
                title = f"タイトル「{title}」で物語を作って。"
                length_text = f"約{a_length_text}文字にして。"
                length_plot = f"{a_length_plot}プロットにして。"
                category = f"物語のジャンルは「{a_category}」にして。"if a_category else ""
                hero = f"主人公は「{a_hero}」。" if a_hero else ""
                cast1 = f"2人目の登場人物は「{a_cast1}」。" if a_cast1 else ""
                cast2 = f"3人目の登場人物は「{a_cast2}」。" if a_cast2 else ""
                cast3 = f"4人目の登場人物は「{a_cast3}」。" if a_cast3 else ""
                story_term = f"条件は{a_story_term}。" if a_story_term else ""
                keywords1 = f"キーワード1は「{a_keywords1}」。" if a_keywords1 else "" 
                keywords2 = f"キーワード1は「{a_keywords2}」。" if a_keywords2 else ""
                keywords3 = f"キーワード1は「{a_keywords3}」。" if a_keywords3 else ""
                language = f"言語は{a_language}。"

                API_KEY = "・・・"
                openai.api_key = API_KEY

                prompt = f"{title}{length_text}{length_plot}{category}{hero}{cast1}{cast2}{cast3}{story_term}{keywords1}{keywords2}{keywords3}{language}"


                #gpt-3.5のAPI準備

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    max_tokens = 500,
                    messages=[
                        {"role": "user", "content": prompt},
                    ]
                )

                print(response)
                stories_text_data = response['choices'][0]['message']['content']  
                print(stories_text_data)
                stories_text = stories_text_data.replace('\n', Markup('<br>'))

                #データベースへの挿入

                cursor.execute("""
                    INSERT INTO storiestable (title, select_font, select_color, length_text, length_plot, category, hero, cast1, cast2, cast3, story_term, keywords1, keywords2, keywords3, language, prompt, stories_text_data)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (text, select_font, select_color, a_length_text, a_length_plot, a_category, a_hero, a_cast1, a_cast2, a_cast3, a_story_term, a_keywords1, a_keywords2, a_keywords3, a_language, prompt, stories_text_data))

                conn.commit()

                cursor.execute("SELECT MAX(id) FROM storiestable")
                max_id = cursor.fetchone()[0]         

                #写真生成
                
                create_image(text, select_color, select_font, max_id)

                return render_template('result.html', text=text,
                        id=max_id, select_font=select_font, select_color=select_color,
                        stories_text=Markup(stories_text), prompt=prompt, category=a_category,          
                        language=a_language, title=title, length_text=a_length_text, length_plot=a_length_plot,
                        hero=a_hero, cast1=a_cast1, cast2=a_cast2, cast3=a_cast3, story_term=a_story_term,
                        keywords1=a_keywords1, keywords2=a_keywords2, keywords3=a_keywords3)




if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost')
