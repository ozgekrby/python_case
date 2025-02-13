from __init__ import create_app, db
from models import Score

app = create_app()

def reset_scores():
    with app.app_context():
        # Tüm skorları sil
        Score.query.delete()
        db.session.commit()
        print("Tüm skorlar başarıyla silindi!")

if __name__ == '__main__':
    reset_scores() 