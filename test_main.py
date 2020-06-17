import unittest
import os
import json
import jwt
from main import Subcategory, Space, app, db, load_constants_seed_data

class SpaceTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
        os.path.join('.', 'test.db')
        self.app = app.test_client()
        
        db.create_all()
        load_constants_seed_data()

        subcat_1 = Subcategory.query.filter_by(id=1).first()
        subcat_2 = Subcategory.query.filter_by(id=2).first()
        subcat_3 = Subcategory.query.filter_by(id=4).first()

        test_space_1 = Space(name = "test_space_1",
                            model_2d = None,
                            model_3d = None,
                            height = 1.1,
                            width =  1.1,
                            active =  True,
                            regular =  True,
                            up_gap =  1,
                            down_gap =  1,
                            left_gap = 1,
                            right_gap = 1)

        test_space_2 = Space(name = "test_space_2",
                            model_2d = None,
                            model_3d = None,
                            height = 1.1,
                            width =  1.2,
                            active =  True,
                            regular =  False)

        test_space_3 = Space(name = "test_space_3",
                            model_2d = None,
                            model_3d = None,
                            height = 2,
                            width =  2,
                            active =  True,
                            regular =  True)

        test_space_4 = Space(name = "test_space_4",
                            model_2d = None,
                            model_3d = None,
                            height = 3,
                            width =  2,
                            active =  True,
                            regular =  False)

        subcat_1.spaces.append(test_space_1)
        subcat_2.spaces.append(test_space_2)
        subcat_3.spaces.append(test_space_3)
        subcat_3.spaces.append(test_space_4)

        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_space_by_id(self):
        with app.test_client() as client:
            client.environ_base['HTTP_AUTHORIZATION'] = jwt.encode({'some': 'payload'}, app.config['SECRET_KEY'], algorithm='HS256')
            rv = client.get('/api/spaces/1')
            self.assertEqual(rv.status_code, 200)
   
    def test_update_space(self):
        with app.test_client() as client:
            client.environ_base['HTTP_AUTHORIZATION'] = jwt.encode({'some': 'payload'}, app.config['SECRET_KEY'], algorithm='HS256')
            rv = client.get('/api/spaces/1')
            space = json.loads(rv.get_data(as_text=True))
            space['name'] = "UpdateName"

            rvu = client.put('/api/spaces/1', data = json.dumps(space), content_type='application/json')

            updated_space = json.loads(rvu.get_data(as_text=True))
            if rvu.status_code == 200:
                self.assertEqual("UpdateName", updated_space['name'])
            
            self.assertEqual(rvu.status_code, 200)

    def test_delete_space(self):
        with app.test_client() as client:
            client.environ_base['HTTP_AUTHORIZATION'] = jwt.encode({'some': 'payload'}, app.config['SECRET_KEY'], algorithm='HS256')
            rv = client.delete('/api/spaces/2')
            self.assertEqual(rv.status_code, 200)

if __name__ == '__main__':
    unittest.main()