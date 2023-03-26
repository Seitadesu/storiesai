import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from html import escape
import openai
from googletrans import Translator
from io import BytesIO

def create_image(text, select_color, select_font, max_id):
                
                #openAIのAPIの準備

                API_KEY = "・・・"
                openai.api_key = API_KEY

                #プロンプトから画像生成・タイトルを英語化
                def generate_image_with_dalle2(prompt, path):
                    response = openai.Image.create(
                    prompt=prompt,
                    n=1,
                    size='{}x{}'.format(str(512), str(512))
                    )
                    image_url = response['data'][0]['url']

                    response = requests.get(image_url)
                    image = Image.open(BytesIO(response.content))
                    image.save(path)

                title_text = text
                translator = Translator()
                text_en = translator.translate(title_text, dest='en')
                text_en = text_en.text
                print(text_en)

                image_url = generate_image_with_dalle2(f'{text_en}', './static/image/generate/aititle'+str(max_id)+'.png')



                # 画像を読み込む
                img = Image.open("./static/image/generate/aititle" + str(max_id) + ".png")

                # 画像を薄くする
                img = img.point(lambda x: x * 0.3)

                # 画像を保存する
                img.save("./static/image/generate/weak" + str(max_id) + ".png")

                # 中央に文字を描画する
                img = Image.open("./static/image/generate/weak" + str(max_id) + ".png")
                draw = ImageDraw.Draw(img)

                text = title_text
                font_size = 50
                font_path = select_font
                font = ImageFont.truetype(font_path, font_size)
                text_width, text_height = draw.textsize(text, font)

                x = (img.width - text_width) // 2
                y = (img.height - text_height) // 2

                while x < 0 or y < 0:
                    font_size -= 1
                    font = ImageFont.truetype(font_path, font_size)
                    text_width, text_height = draw.textsize(text, font)
                    x = (img.width - text_width) // 2
                    y = (img.height - text_height) // 2

                if select_color != (255, 255, 255):
                    draw.multiline_text((x, y), text, font=font, fill=select_color, align='center', stroke_width=3, stroke_fill='white')
                else:
                    draw.multiline_text((x, y), text, font=font, fill=select_color, align='center')

                img.save("./static/image/generate/weak_center" + str(max_id) + ".png")



