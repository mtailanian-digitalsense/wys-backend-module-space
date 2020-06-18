import unittest
import os
import json
import jwt
from main import Subcategory, Space, app, db, Category, load_constants_seed_data

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


class Test(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                                os.path.join('.', 'test.db')

        self.app = app.test_client()
        db.create_all()
        load_constants_seed_data()

    def test_data_to_create_spaces(self):
        with app.test_client() as client:

            client.environ_base['HTTP_AUTHORIZATION'] = jwt.encode({'some': 'payload'}, app.config['SECRET_KEY'],
                                                                   algorithm='HS256')
            rv = client.get('/api/spaces/create')
            resp_dict = json.loads(rv.data.decode("utf-8"))
            assert len(resp_dict) == Category.query.count()

            subcategories = []

            for category in resp_dict:
                for subcategory in category['subcategories']:
                    subcategories.append(subcategory)

            assert len(subcategories) == Subcategory.query.count()

    def test_new_space(self):
        raw_data = {
            "active": True,
            "down_gap": 0.5,
            "height": 0,
            "left_gap": 0,
            "model_2d": IMAGE_BASE64,
            "model_3d": IMAGE_BASE64,
            "name": "Test1",
            "regular": True,
            "right_gap": 1,
            "subcategory_id": 2,
            "up_gap": 1,
            "width": 1
        }
        with app.test_client() as client:
            client.environ_base['HTTP_AUTHORIZATION'] = jwt.encode({'some': 'payload'}, app.config['SECRET_KEY'],
                                                                   algorithm='HS256')
            rv = client.post('/api/spaces/create', data=json.dumps(raw_data), content_type='application/json')
            assert rv.status_code == 201
            resp_dict = json.loads(rv.data.decode("utf-8"))

            for key, val in raw_data.items():
                assert resp_dict[key] == val
            Space.query.delete()
            return

    def test_get_all_spaces(self):
        datas = [
            {
                "active": True,
                "down_gap": 0.5,
                "height": 0,
                "left_gap": 0,
                "model_2d": IMAGE_BASE64,
                "model_3d": IMAGE_BASE64,
                "name": f"Test{i}",
                "regular": True,
                "right_gap": 1,
                "subcategory_id": 2,
                "up_gap": 1,
                "width": 1
            }
            for i in range(10)
        ]

        with app.test_client() as client:
            client.environ_base['HTTP_AUTHORIZATION'] = jwt.encode({'some': 'payload'}, app.config['SECRET_KEY'],
                                                                   algorithm='HS256')
            for data in datas:
                client.post('/api/spaces/create', data=json.dumps(data), content_type='application/json')

            rv = client.get('/api/spaces/')
            resp_dict = json.loads(rv.data.decode("utf-8"))
            assert len(resp_dict) == len(datas)

    def tearDown(self):
        db.session.remove()
        db.drop_all()


IMAGE_BASE64 = "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"