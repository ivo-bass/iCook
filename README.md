# iCook

**Django Template Project** with responsive design.

Deployed on ...

## Video Presentation

[![Cars Game Video](https://img.youtube.com/vi/R9M6HYdyTB0/default.jpg)](https://youtu.be/R9M6HYdyTB0)

# Software Documentation

## iCook

Prepared by Ivailo Ignatov  
05.08.2021

Table of Contents
=================

* 1 [Introduction](#1-introduction)
* 2 [Product Overview](#2-product-overview)
    * 2.1 [Product Functions](#21-product-functions)
    * 2.2 [User Characteristics](#22-user-characteristics)
    * 2.3 [Profile objects](#23-profile-objects)
    * 2.4 [Recipe objects](#24-recipe-objects)
    * 2.5 [Ingredient objects](#25-ingredient-objects)
* 3 [Additional Sevices](#3-additional-services)
    * 3.1 [Claudianry](#31-cloudianry)
    * 3.2 [Celery](#32-celery)
* 4 [Requirements Met](#4-requirements-met)
    * 4.1 [Mandatory Requirements](#41-mandatory-requirements--must-haves)
    * 4.2 [Optional Requirements](#42-optional--bonuses)

## 1. Introduction

The purpose of this document is to present a description of the Web Project. It will explain the purpose and features of
the system, the interfaces of the system, what the system will do.

## 2. Product Overview

iCook is a digital cookbook and cooking guide alike, that helps home cooks of every level discover, save and organize
the best recipes, while also helping them become better.

### 2.1 Product Functions

* A database of cooking recipes
* Perform search for recipes by keywords
* Create, read, update and delete recipes
* Like and comment recipes
* Classify recipes by view, like and comment counts
* Provide suggestions to the authenticated users (***Suggest***)
* Save suggestion as a todo item (***Choice***)
* Keep track on user choices (***History***)
* Keep track on liked recipes (***Liked Recipes***)
* Create update and delete own user profile
* View foreign profiles

### 2.2 User Characteristics

#### 2.2.1 Anonymous User

Anonymous user has only get permissions to all ***public*** recipes.

They can perform searches, view details for a recipe and view top recipes. This user is able to sing up with email and
password. The sign-up includes an **email verification** process. Anonymous user has access to the top navigation bar
but does not see the sidebar.

#### 2.2.1 Regular User

All registered users by default are regular users.

This user can sign-in with email and password. Post authentication the user is able to navigate through the sidebar.  
The user has their own ***profile*** with username, image, first name and last name and all CRUD operations related to
it.  
This user has all CRUD permissions to their own recipes. They can like and comment to all public recipes in the system.

#### 2.2.1 Admin User

The admin user gets enabled through the admin site by another admin user, setting their '*is_staff*' field to **True**.

This user has all CRUD permissions over other users, their profiles and all recipes in the database. After
authentication this user can access the admin site through the top navigation panel.

### 2.3 Profile Objects

**Profile** is created on user creation with auto-generated username.  
The user profile has a profile completion ***progress*** based on filled profile fields.  
The user profiles has a ***rang***. The ***rang*** is based on the count of likes, comments and recipes created by the
user.

#### Components:

- User - *foreign-key relation with the user*
- Username - *char-field auto-generated based on the email of the user*
- First name - *char-field*
- Last name - *char-field*
- Image - *resized-image-field - [link](https://pypi.org/project/django-resized/)*
- Dark theme - *boolean-field*
- Rang - *property*
- Progress - *property*

### 2.4 Recipe Objects

The ***Recipe*** object could be either public or private. It can be viewed by all types of users, but created, edited
and deleted only by its author.

#### Components:

- Author - *foreign-key relation with the user*
- Title - *char-field*
- Type - *char-field with choices*
- Short description - *char-field*
- Image - *resized-image-field - [link](https://pypi.org/project/django-resized/)*
- Time of preparation - *integer-field*
- Count fo servings - *integer-field*
- Preparation methods - *textarea*
- Vegetarian - *boolean-field*
- Public - *boolean-field*
- Views count - *property*
- **Ingredients** - *set of ingredient objects related with a foreign-key to the recipe*
- **Likes** - *set of like objects related with a foreign-key to the recipe*
- **Comments** - *set of comment objects related with a foreign-key to the recipe*

### 2.5 Ingredient Objects

The ***Ingredient*** objects are created on recipe creation.

#### Components:

- Recipe - *foreign-key relation with the recipe*
- Name - *char-field*
- Quantity - *float-field*
- Measure - *char-field with choices*

## 3. Additional Services

### 3.1 Cloudianry

asdasdasdasdasdasd

### 3.2 Celery

asdasdasdasdasasda

## 4. Requirements Met

[| link to exam requirements |](https://softuni.bg/trainings/resources/officedocument/60950/project-requirements-python-web-framework-july-2021/3356)

### 4.1 Mandatory requirements / *Must haves*

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

### 4.2 Optional / *Bonuses*

- [x] Responsive web design
- [x] Class-based views
- [x] Extended Django user
- [x] Documentation/ Swagger
- [ ] Use a file storage cloud API e.g., Cloudinary, Dropbox, Google Drive or other for storing the files
- [ ] Implement Microservice architecture in your application.
