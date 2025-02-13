from __init__ import create_app, db
from models import Question

app = create_app()

def add_sample_questions():
    with app.app_context():
        # Önce tüm eski soruları temizle
        Question.query.delete()
        
        # Örnek soruları ekle
        questions = [
            # Discord.py Soruları (1. şık)
            {
                'question_text': 'Discord.py\'da bir bot oluştururken hangi dekoratör kullanılır?',
                'options': '@client.event,@bot.command(),@discord.event,@bot.create',
                'correct_answer': '@client.event'
            },
            # Flask Soruları (2. şık)
            {
                'question_text': 'Flask\'ta template render etmek için hangi fonksiyon kullanılır?',
                'options': 'show_template,render_template,display_html,create_view',
                'correct_answer': 'render_template'
            },
            # Yapay Zeka Soruları (3. şık)
            {
                'question_text': 'Yapay sinir ağlarında en çok kullanılan aktivasyon fonksiyonu hangisidir?',
                'options': 'Sigmoid,Tanh,ReLU,Linear',
                'correct_answer': 'ReLU'
            },
            # Computer Vision Soruları (4. şık)
            {
                'question_text': 'Görüntü işlemede kenar tespiti için hangi algoritma kullanılır?',
                'options': 'Sobel,Prewitt,Canny,Hepsi',
                'correct_answer': 'Hepsi'
            },
            # NLP Soruları (1. şık)
            {
                'question_text': 'NLTK kütüphanesinde tokenization ne işe yarar?',
                'options': 'Metni küçük parçalara böler,Metni tercüme eder,Metni sıkıştırır,Metni şifreler',
                'correct_answer': 'Metni küçük parçalara böler'
            },
            # Discord.py Event (2. şık)
            {
                'question_text': 'Discord.py\'da bir botun çevrimiçi olduğunu kontrol etmek için hangi event kullanılır?',
                'options': 'bot_online,on_ready,on_connect,is_ready',
                'correct_answer': 'on_ready'
            },
            # Flask Route (3. şık)
            {
                'question_text': 'Flask\'ta route tanımlarken hangi dekoratör kullanılır?',
                'options': '@flask.path,@web.route,@app.route,@path.new',
                'correct_answer': '@app.route'
            },
            # OpenCV (4. şık)
            {
                'question_text': 'OpenCV kütüphanesini Python\'da import ederken hangi kısaltma kullanılır?',
                'options': 'opencv,cvlib,openv,cv2',
                'correct_answer': 'cv2'
            },
            # TensorFlow (2. şık)
            {
                'question_text': 'Hangi kütüphane Python\'da derin öğrenme için en çok kullanılır?',
                'options': 'NumPy,TensorFlow,Pandas,Matplotlib',
                'correct_answer': 'TensorFlow'
            },
            # BeautifulSoup (3. şık)
            {
                'question_text': 'BeautifulSoup hangi amaçla kullanılır?',
                'options': 'Metin analizi,Duygu analizi,Web scraping,Makine öğrenmesi',
                'correct_answer': 'Web scraping'
            }
        ]
        
        # Soruları veritabanına ekle
        for q in questions:
            question = Question(
                question_text=q['question_text'],
                options=q['options'],
                correct_answer=q['correct_answer']
            )
            db.session.add(question)
        
        db.session.commit()
        print("Sorular başarıyla eklendi!")

if __name__ == '__main__':
    add_sample_questions()