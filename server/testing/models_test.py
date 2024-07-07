from datetime import date

from app import app
from models import db, Plant

class TestPlant:
    '''Plant model in models.py'''

    def test_can_instantiate(self):
        '''can be instantiated with a name, image, and price.'''
        p = Plant(name="Douglas Fir", image="https://example.com/douglas_fir.jpg", price=100.00)
        assert p is not None
    
    def test_can_be_created(self):
        '''can create records that can be committed to the database.'''
        with app.app_context():
            p = Plant(name="Douglas Fir", image="https://example.com/douglas_fir.jpg", price=100.00)
            db.session.add(p)
            db.session.commit()
            assert p.id is not None

            db.session.delete(p)
            db.session.commit()

    def test_can_be_retrieved(self):
        '''can be used to retrieve records from the database.'''
        with app.app_context():
            p = Plant(name="Douglas Fir", image="https://example.com/douglas_fir.jpg", price=100.00)
            db.session.add(p)
            db.session.commit()

            retrieved_p = Plant.query.all()
            assert retrieved_p is not None

            db.session.delete(p)
            db.session.commit()

    def test_can_be_serialized(self):
        '''can create records with a to_dict() method for serialization.'''
        with app.app_context():
            p = Plant(name="Douglas Fir", image="https://example.com/douglas_fir.jpg", price=100.00)
            db.session.add(p)
            db.session.commit()
            p_dict = Plant.query.filter_by(name="Douglas Fir").first().to_dict()
            assert isinstance(p_dict, dict) and p_dict["name"] == "Douglas Fir"
        
            db.session.delete(p)
            db.session.commit()
