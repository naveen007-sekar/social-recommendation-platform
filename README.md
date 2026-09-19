# Social Commerce Post Recommendation System

## Overview

This project recommends social-commerce posts to users based on their interests and activity on the platform.

The system uses a hybrid recommendation approach instead of depending on only one signal. It considers user engagement, post embeddings, creator follows, post popularity, shopping activity, and post recency.

The API returns recommended posts along with score details and readable reasons behind every recommendation.

## Problem Statement

A social-commerce feed should not show the same posts to every user.

For example, a user who often watches fashion videos, follows a beauty creator, and adds skincare products to their cart should see content related to those interests.

The main goals of this project are:

- Recommend relevant posts for each user
- Rank posts in a meaningful order
- Avoid repeatedly showing already-seen posts
- Keep recommendations diverse across creators and categories
- Handle new users with no previous activity
- Explain why each post was recommended

## Technology Stack

- Python
- FastAPI
- MongoDB
- PyMongo
- NumPy
- Pydantic
- Pytest
- Uvicorn

## Project Structure

```text
social_recommendation_platform/
│
├── app/
│   ├── api/
│   │   └── routes.py
│   ├── models/
│   │   └── schemas.py
│   ├── recommender/
│   │   ├── engine.py
│   │   ├── user_profile.py
│   │   ├── candidate_generator.py
│   │   ├── feature_builder.py
│   │   ├── ranker.py
│   │   ├── diversity.py
│   │   └── cold_start.py
│   ├── services/
│   │   └── data_service.py
│   ├── utils/
│   │   └── helpers.py
│   ├── config.py
│   ├── database.py
│   └── main.py
│
├── scripts/
│   ├── inspect_db.py
│   └── demo.py
│
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── run.py

## How It Works

MongoDB
   |
   v
Data Service
   |
   +-----------------------------+
   |                             |
   v                             v
User Activity                Post Embeddings
   |                             |
   +-------------+---------------+
                 |
                 v
          User Interest Profile
                 |
                 v
        Candidate Post Selection
                 |
                 v
         Feature Score Calculation
                 |
                 v
           Hybrid Ranking
                 |
                 v
        Diversity and Seen Filter
                 |
                 v
        Final Recommended Feed
