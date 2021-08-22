# Documentation

## iCook

[icook.gq](https://icook.gq/)

by **Ivailo Ignatov** - _IvoBass_  
09.08.2021

# Table of Contents

- 1 [Introduction](#1-introduction)

- 2 [Product Overview](#2-product-overview)

  - 2.1 [Product Features ](#21-product-features)
  - 2.2 [User Characteristics](#22-user-characteristics)
  - 2.3 [Profile objects](#23-profile-objects)
  - 2.4 [Recipe objects](#24-recipe-objects)
  - 2.5 [Ingredient objects](#25-ingredient-objects)

- 3 [Additional Sevices](#3-additional-services)
  - 3.1 [Claudianry](#31-cloudianry)

[comment]: <> ( \* 3.2 [Celery]&#40;#32-celery&#41;)

- 4 [Requirements Met](#4-requirements-met)

  - 4.1 [Mandatory Requirements](#41-mandatory-requirements--must-haves)
  - 4.2 [Optional Requirements](#42-optional--bonuses)

- 5 [Test Coverage](#5-tests-coverage)

- 6 [Video Presentation](#6-video-presentation)

- 7 [Deployment](#7-deployment)

## 1. Introduction

The purpose of this document is to present a description of the Web Project. It will explain the purpose and features of
the system, the interfaces of the system, what the system will do.

## 2. Product Overview

iCook is a digital cookbook and cooking guide alike, that helps home cooks of every level discover, save and organize
the best recipes, while also helping them become better.

### 2.1 Product Features

- Custom user
- Cloud storage
- Dark/Light Mode
- Email verification

---

- Create private recipes
- Perform search for recipes by keywords
- Classify recipes by view, like and comment counts
- Create, read, update, delete, like and comment recipes

---

- Provide suggestions to the authenticated users (**_Suggest_**)
- Keep track on liked recipes (**_Liked Recipes_**)
- Save suggestion as a todo item (**_Choice_**)
- Keep track on user choices (**_History_**)

---

- Create update and delete own user profile
- Develop profile rating (**_Rang_**)
- Change or Reset password
- View other profiles

### 2.2 User Characteristics

#### 2.2.1 Anonymous User

Anonymous user has only get permissions to all **_public_** recipes.

They can perform searches, view details for a recipe and view top recipes. This user is able to sing up with email and
password. The sign-up includes an **email verification** process. Anonymous user has access to the top navigation bar
but does not see the sidebar.

#### 2.2.1 Regular User

All registered users by default are regular users.

This user can sign-in with email and password. Post authentication the user is able to navigate through the sidebar.  
The user has their own **_profile_** with username, image, first name and last name and all CRUD operations related to
it.  
This user has all CRUD permissions to their own recipes. They can like and comment to all public recipes in the system.

#### 2.2.1 Admin User

The admin user gets enabled through the admin site by another admin user, setting their '_is_staff_' field to **True**.

This user has all CRUD permissions over other users, their profiles and all recipes in the database. After
authentication this user can access the admin site through the top navigation panel.

### 2.3 Profile Objects

**Profile** is created on user creation with auto-generated username.  
The user profile has a profile completion **_progress_** based on filled profile fields.  
The user profiles has a **_rang_**. The **_rang_** is based on the count of likes, comments and recipes created by the
user.

#### Components:

- User - _foreign-key relation with the user_
- Username - _char-field auto-generated based on the email of the user_
- First name - _char-field_
- Last name - _char-field_
- Image - _cloudinary-field_
- Dark theme - _boolean-field_
- Rang - _property_
- Progress - _property_

### 2.4 Recipe Objects

The **_Recipe_** object could be either public or private. It can be viewed by all types of users, but created, edited
and deleted only by its author.

#### Components:

- Author - _foreign-key relation with the user_
- Title - _char-field_
- Type - _char-field with choices_
- Short description - _char-field_
- Image - _cloudinary-field_
- Time of preparation - _integer-field_
- Count fo servings - _integer-field_
- Preparation methods - _textarea_
- Vegetarian - _boolean-field_
- Public - _boolean-field_
- Views count - _property_
- **Ingredients** - _set of ingredient objects related with a foreign-key to the recipe_
- **Likes** - _set of like objects related with a foreign-key to the recipe_
- **Comments** - _set of comment objects related with a foreign-key to the recipe_

### 2.5 Ingredient Objects

The **_Ingredient_** objects are created on recipe creation.

#### Components:

- Recipe - _foreign-key relation with the recipe_
- Name - _char-field_
- Quantity - _float-field_
- Measure - _char-field with choices_

## 3. Additional Services

### 3.1 Cloudianry

The system uses [**Cloudinary's** Python SDK](https://cloudinary.com/documentation/django_integration) to store all
media files - profile images and recipe images.  
The images are cropped to occupy less space in the cloud - 200x200 for profiles and 580x326 for recipes.  
**_Static_** directory contain default images which are rendered by the template if no image is uploaded in the cloud.

## 4. Requirements Met

[| link to exam requirements |](https://softuni.bg/trainings/resources/officedocument/60950/project-requirements-python-web-framework-july-2021/3356)

### 4.1 Mandatory requirements / _Must haves_

- [x] The application must be implemented using Django Framework
- [x] The application must have at least 10 endpoints
- [x] The application must have login/register functionality
- [x] The application must have public part (A part of the website, which is accessible by everyone – un/authenticated
      users and admins)
- [x] The application must have private part (accessible only by authenticated user and admins)
- [x] The application must have admin part (accessible only to admins)
- [x] Unauthenticated users (public part) have only 'get' permissions e.g., landing page, details, about page
- [x] Authenticated users (private part) have full CRUD for all their created content
- [x] Admins have full CRUD functionalities
- [x] Form validations
- [x] To avoid crashes, implement Error Handling and Data Validations
- [x] Use PostgreSQL as a database.
- [x] Write tests for at least 60% coverage on your business logic
- [x] Templates (your controllers/views must return HTML files) – one and the same template could be re-used/used
      multiple times (with the according adjustments, if such needed)
- [x] Use a source control system by choice – Github or Gitlab. You must have at least 5 commits + README

### 4.2 Optional / _Bonuses_

- [x] Responsive web design
- [x] Class-based views
- [x] Extended Django user
- [x] Documentation/ Swagger
- [x] Use a file storage cloud API e.g., **Cloudinary**, Dropbox, Google Drive or other for storing the files
- [x] Implement Microservice architecture in your application.

## 5. Tests Coverage

![Views Coverage](/github-images/views_coverage.png)

![Models Coverage](/github-images/models_coverage.png)

![Forms Coverage](/github-images/forms_coverage.png)

## 6. Video Presentation

[![Presentation Video](https://img.youtube.com/vi/zMhGDAGEAIM/default.jpg)](https://youtu.be/zMhGDAGEAIM)

## 7. Deployment

[icook.gq](https://icook.gq/)

Docker, AWS - EC2, Nginx, Certbot
