# API Endpoints for Spaces

Port: 8083

## Show all categories and subcategories to be attached to spaces 

**URL** : `/api/spaces/create`

**Method** : `GET`

**Auth required** : YES

### Success Response

**Code** : `200 OK`

**Content example**

Before to create a space, the frontend must call to this method to get all categories
and subcategories. One of these categories-subcategories pair must be added to the new space.   

```json
[{
    "id": 1,
    "name": "Category 1",
    "subcategories": [{
      "id": 1,
      "name": "subcat1"    
    },
    {
      "id": 2,
      "name": "subcat2"    
    }] 
},{
    "id": 4,
    "name": "Category 4",
    "subcategories": [{
      "id": 5,
      "name": "subcat5"    
    },
    {
      "id": 6,
      "name": "subcat6"    
    }] 
}] 
```

### Error Responses

**Condition** :  If server has some error.

**Code** : `500 Internal Error Server`

**Content** : `{error_message}`


## Create a new Space 

**URL** : `/api/spaces/create`

**Required Body** :
````json
{
    "name": name, //String
    "model_2d" : model_2d, //base 64 file
    "model_3d" : model_3d, //base 64 file
    "height" : height, //in cm
    "width" :  width, //in cm
    "active" :  active, //bool
    "regular" :  regular, //bool
    "up_gap" :  up_gap, //float in cm
    "down_gap" :  down_gap, //float in cm
    "left_gap" : left_gap, // float in cm
    "right_gap" : right_gap, // float in cm
    "subcategory_id" : subcategory_id // gotten in "/api/spaces/create"
}
````

**Method** : `POST`

**Auth required** : YES

### Success Response

**Code** : `201 CREATED`

**Content example**

````json
{
    "id": 1, //Integer
    "name": "Space1", //String
    "model_2d" : "asdkasdjkasjdkajd", //base 64 file
    "model_3d" : "aaksdaksdkasjdkasjd", //base 64 file
    "height" : 300.5, //in cm
    "width" :  400.9, //in cm
    "active" :  true, //bool
    "regular" :  true, //bool
    "up_gap" :  1.0, //float in cm
    "down_gap" :  1.0, //float in cm
    "left_gap" : 1.0, // float in cm
    "right_gap" : 1.0, // float in cm
    "subcategory_id" : 2 // gotten in "/api/spaces/create"
}
````

### Error Responses

**Condition** :  If server has some error.

**Code** : `500 Internal Error Server`

**Content** : `{error_message}`

## Get all spaces 

**URL** : `/api/spaces/`

**Method** : `GET`

**Auth required** : YES

### Success Response

**Code** : `200 OK`

**Content example:**
Show all spaces in DB
````json
[{
        "id": 1, //Integer,
        "name": "Space1", //String
        "model_2d" : "asdkasdjkasjdkajd", //base 64 file
        "model_3d" : "aaksdaksdkasjdkasjd", //base 64 file
        "height" : 300.5, //in cm
        "width" :  400.9, //in cm
        "active" :  true, //bool
        "regular" :  true, //bool
        "up_gap" :  1.0, //float in cm
        "down_gap" :  1.0, //float in cm
        "left_gap" : 1.0, // float in cm
        "right_gap" : 1.0, // float in cm
        "subcategory_id" : 2 // gotten in "/api/spaces/create"
    },
    {
        "id": 1, //Integer,
        "name": "Space2", //String
        "model_2d" : "asdkasdjkasjdkajd", //base 64 file
        "model_3d" : "aaksdaksdkasjdkasjd", //base 64 file
        "height" : 300.5, //in cm
        "width" :  400.9, //in cm
        "active" :  true, //bool
        "regular" :  true, //bool
        "up_gap" :  1.0, //float in cm
        "down_gap" :  1.0, //float in cm
        "left_gap" : 1.0, // float in cm
        "right_gap" : 1.0, // float in cm
        "subcategory_id" : 2 // gotten in "/api/spaces/create"
        }]
````

### Error Responses

**Condition** :  If server has some error.

**Code** : `500 Internal Error Server`

**Content** : `{error_message}`

## Get a single space

**URL** : `/api/spaces/{space_id}`

**Method** : `GET`

**Auth required** : YES

### Success Response

**Code** : `200 OK`

**Content example:**
If the space's id is 1, then the response will be: 
````json
{
    "id": 1, //Integer,
    "name": "Space1", //String
    "model_2d" : "asdkasdjkasjdkajd", //base 64 file
    "model_3d" : "aaksdaksdkasjdkasjd", //base 64 file
    "height" : 300.5, //in cm
    "width" :  400.9, //in cm
    "active" :  true, //bool
    "regular" :  true, //bool
    "up_gap" :  1.0, //float in cm
    "down_gap" :  1.0, //float in cm
    "left_gap" : 1.0, // float in cm
    "right_gap" : 1.0, // float in cm
    "subcategory_id" : 2 // gotten in "/api/spaces/create"
}
````

### Error Responses

**Condition** :  If server has some error.

**Code** : `500 Internal Error Server`

**Content** : `{error_message}`

## Update a space

**URL** : `/api/spaces/update`

**Required Body** :
````json
{
    "id": id, //Integer
    "name": name, //String
    "model_2d" : model_2d, //base 64 file
    "model_3d" : model_3d, //base 64 file
    "height" : height, //in cm
    "width" :  width, //in cm
    "active" :  active, //bool
    "regular" :  regular, //bool
    "up_gap" :  up_gap, //float in cm
    "down_gap" :  down_gap, //float in cm
    "left_gap" : left_gap, // float in cm
    "right_gap" : right_gap, // float in cm
    "subcategory_id" : subcategory_id // gotten in "/api/spaces/create"
}
````

**Method** : `PUT`

**Auth required** : YES

### Success Response

**Code** : `200 OK`

**Content example:**
Space Updated Successfully
````json
{
    "id": 1, //Integer,
    "name": "Space1", //String
    "model_2d" : "asdkasdjkasjdkajd", //base 64 file
    "model_3d" : "aaksdaksdkasjdkasjd", //base 64 file
    "height" : 300.5, //in cm
    "width" :  400.9, //in cm
    "active" :  true, //bool
    "regular" :  true, //bool
    "up_gap" :  1.0, //float in cm
    "down_gap" :  1.0, //float in cm
    "left_gap" : 1.0, // float in cm
    "right_gap" : 1.0, // float in cm
    "subcategory_id" : 2 // gotten in "/api/spaces/create"
}
````

### Error Responses

**Condition** :  The space id was not found.

**Code** : `400 Bad Request`

**Content** : `{error_message}`

### Or

**Condition** :  If server has some error.

**Code** : `500 Internal Error Server`

**Content** : `{error_message}` 

**Method** : `PUT`

**Auth required** : YES

## Desable a space

**URL** : `/api/spaces/{space_id}`

**Method** : `DELETE`

**Auth required** : YES

### Success Response

**Code** : `200 OK`

### Error Responses

**Condition** :  The space id was not found.

**Code** : `400 Bad Request`

**Content** : `{error_message}`

### Or

**Condition** :  If server has some error.

**Code** : `500 Internal Error Server`

**Content** : `{error_message}` 

**Method** : `PUT`

**Auth required** : YES

## Show all Subcategories

**URL** : `/api/spaces/subcategories`

**Method** : `GET`

**Auth required** : YES

### Success Response

**Code** : `200 OK`

**Content example**

```json
[
    {
      "id": 1,
      "name": "Sala Reunión",
      "subcategories": [
        {
          "area": 8.64,
          "category_id": 1,
          "id": 1,
          "name": "Pequeña",
          "people_capacity": 5,
          "unit_area": 1.73,
          "usage_percentage": 0.45
        },
        ...
    ]
  },
  {
    "id": 2,
    "name": "Privado",
    "subcategories": [
      {
        "area": 11.93,
        "category_id": 2,
        "id": 4,
        "name": "Pequeño",
        "people_capacity": 1,
        "unit_area": 11.93,
        "usage_percentage": null
      },
      ...
    ]
  }
  ...
]
```

### Error Responses

**Condition** : If an error occurs with the database.

**Code** : `500 Internal Server Error`

**Content** : `{exception_message}`