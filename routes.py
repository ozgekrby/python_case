from flask import Blueprint, render_template, request, redirect, url_for, session
from models import Question, Score
from __init__ import db
import random

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        
        if not name or not surname:
            return render_template('login.html', error="Lütfen ad ve soyadınızı girin!")
        
        # İsim ve soyismi düzenle: Boşlukları temizle ve baş harfler büyük, diğerleri küçük
        name = ' '.join(name.strip().split()).title()  # Fazla boşlukları temizle ve düzenle
        surname = ' '.join(surname.strip().split()).title()  # Fazla boşlukları temizle ve düzenle
        display_name = f"{name} {surname}"  # Görüntülenecek isim
        
        # Veritabanı sorguları için kullanılacak isim (hepsi küçük harf ve tek boşluk)
        db_username = display_name.lower()
        
        # Session'da hem görüntülenecek hem de veritabanı için kullanılacak isimleri sakla
        session['username'] = display_name
        session['db_username'] = db_username
        
        # Kullanıcının en yüksek puanını al (küçük harfli isimle sorgula)
        user_scores = Score.query.filter_by(username=db_username).order_by(Score.score.desc()).first()
        if user_scores:
            session['user_high_score'] = user_scores.score
        else:
            session['user_high_score'] = 0
        
        return redirect(url_for('main.exam'))
    
    return render_template('login.html')

@main.route('/exam', methods=['GET', 'POST'])
def exam():
    if 'username' not in session:
        return redirect(url_for('main.login'))
        
    if request.method == 'POST':
        questions = Question.query.all()
        total_questions = len(questions)
        correct_answers = 0
        results = []
        
        for question in questions:
            user_answer = request.form.get(str(question.id))
            if not user_answer:
                continue
                
            is_correct = user_answer == question.correct_answer
            if is_correct:
                correct_answers += 1
            
            results.append({
                'question': question.question_text,
                'user_answer': user_answer,
                'correct_answer': question.correct_answer,
                'is_correct': is_correct
            })
        
        # 100 üzerinden puanı hesapla
        score = int((correct_answers / total_questions) * 100)
        
        # Puanı kaydet (küçük harfli isimle)
        new_score = Score(username=session['db_username'], score=score)
        db.session.add(new_score)
        db.session.commit()
        
        # Sonuçları session'da sakla
        session['last_results'] = results
        
        # Kullanıcının en yüksek puanını güncelle
        if score > session.get('user_high_score', 0):
            session['user_high_score'] = score
        
        return redirect(url_for('main.results', score=score))
    
    # Soruları karıştır
    questions = Question.query.all()
    random.shuffle(questions)
    
    # Kullanıcının en yüksek puanını al
    user_high_score = session.get('user_high_score', 0)
    
    # Tüm zamanların en yüksek puanını al
    all_time_high = Score.query.order_by(Score.score.desc()).first()
    all_time_high = all_time_high.score if all_time_high else 0

    return render_template('exam.html', 
                         questions=questions,
                         username=session['username'],  # Görüntülenecek isim (Baş harfler büyük)
                         overall_high_score=all_time_high,
                         user_high_score=user_high_score)

@main.route('/results/<int:score>')
def results(score):
    if 'username' not in session:
        return redirect(url_for('main.login'))
        
    # Kullanıcının en yüksek puanı (küçük harfli isimle sorgula)
    user_high_score = Score.query.filter_by(username=session['db_username']).order_by(Score.score.desc()).first()
    user_high_score = user_high_score.score if user_high_score else 0
    
    # Tüm zamanların en yüksek puanını al
    all_time_high = Score.query.order_by(Score.score.desc()).first()
    all_time_high = all_time_high.score if all_time_high else 0
    
    # Son sınavın sonuçlarını session'dan al
    results = session.get('last_results', [])
    
    return render_template('results.html', 
                         username=session['username'],  # Görüntülenecek isim (Baş harfler büyük)
                         score=score,
                         user_high_score=user_high_score,
                         overall_high_score=all_time_high,
                         results=results)

@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login')) 