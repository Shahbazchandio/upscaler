from app import db
from datetime import datetime

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    original_url = db.Column(db.String(200), nullable=False)
    upscaled_url = db.Column(db.String(200))
    enhanced_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'original_url': self.original_url,
            'upscaled_url': self.upscaled_url,
            'enhanced_url': self.enhanced_url,
            'created_at': self.created_at.isoformat(),
            'processed_at': self.processed_at.isoformat() if self.processed_at else None
        }