import pymongo
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from django.http import JsonResponse
from django.shortcuts import render
from .models import Enrolledcourse,Searchhistory

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['course']
courses_collection = db['courses']

def fetchEnrollment(request, userid):
    if client:
        print("MongoDb Connected")


    enrollments = Enrolledcourse.objects.filter(userid=userid).values()

    if enrollments.exists():
        enrollment_details = []

        for enrollment in enrollments:
            course_id = enrollment['courseid_id']  # Get the course ID from the enrollment
            user_id = enrollment['userid_id']
            course = courses_collection.find_one({'courseId': course_id})

            if course:
                details = {
                    'userId': enrollment['userid_id'],
                    'courseId': course['courseId'],
                    'courseName': course['title'],
                    'courseDescription': course['description'],
                    'objective': course['objective'],
                    'requirement': course['requirement'],
                    'sections': course['sections'],
                    'titleVideoLink': course['titleVideoLink']
                }
                enrollment_details.append(details)

        course_details = []

        for course in courses_collection.find():
            details = {
                'courseId': course['courseId'],
                'courseName': course['title'],
                'courseDescription': course['description'],
                'objective': course['objective'],
                'requirement': course['requirement'],
                'sections': course['sections'],
                'titleVideoLink': course['titleVideoLink']
            }
            course_details.append(details)

        
        df_user_courses = pd.DataFrame(enrollment_details)
        df_all_courses = pd.DataFrame(course_details)

        # Fill missing values with empty strings
        df_all_courses = df_all_courses.fillna('')

        # Combine relevant text fields into a single feature for all courses
        df_all_courses['content'] = (
            df_all_courses['courseName'] + " " +
            df_all_courses['objective'] + " " +
            df_all_courses['requirement']
        )

        # TF-IDF Vectorizer and Cosine Similarity on all courses
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(df_all_courses['content'])
        cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

        def get_recommendations(userid, df_user_courses, df_all_courses, cosine_sim):
            user_courses = df_user_courses[df_user_courses['userId'] == userid]['courseId'].tolist()

            # Calculate the mean cosine similarity score for each course based on user's courses
            user_course_indices = df_all_courses[df_all_courses['courseId'].isin(user_courses)].index.tolist()
            sim_scores = cosine_sim[user_course_indices].mean(axis=0)
            
            # Sort courses based on similarity scores
            sim_scores = sorted(list(enumerate(sim_scores)), key=lambda x: x[1], reverse=True)
            recommended_course_indices = [i[0] for i in sim_scores if df_all_courses.iloc[i[0]]['courseId'] not in user_courses]
            return df_all_courses.iloc[recommended_course_indices][:3]['courseName'].tolist()

        # Example usage
        recommendations = get_recommendations(userid, df_user_courses, df_all_courses, cosine_sim)
        
        return JsonResponse({'recommendations': recommendations})
    else:
        return JsonResponse({'error': 'No enrollments found for this user'})


def recomendationFromSearch(request, userid):
    search_history_qs = Searchhistory.objects.filter(userid=userid).values_list('query', flat=True)
    search_history = " ".join(search_history_qs)  # Concatenate all queries into a single string

    # Fetch all courses from MongoDB
    course_details = []
    for course in courses_collection.find():
        details = {
            'courseId': course['courseId'],
            'courseName': course['title'],
            'courseDescription': course['description'],
            'objective': course['objective'],
            'requirement': course['requirement'],
            'sections': course['sections']
            
        }
        course_details.append(details)

    df_all_courses = pd.DataFrame(course_details)

    # Fill missing values with empty strings
    df_all_courses = df_all_courses.fillna('')

    # Combine relevant text fields into a single feature for all courses
    df_all_courses['content'] = (
        df_all_courses['courseName'].astype(str) + " " +
        df_all_courses['objective'].astype(str) + " " +
        df_all_courses['courseDescription'].astype(str) + " " +
        df_all_courses['requirement'].astype(str)
    )

    # Add search history only if it exists
    if search_history.strip():
        df_all_courses['content'] += " " + search_history

    # TF-IDF Vectorizer and Cosine Similarity on all courses
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df_all_courses['content'].values.astype('U'))
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    # Function to get course recommendations based on search history
    def get_recommendations_from_search(search_history, df_all_courses, cosine_sim):
        search_index = df_all_courses[df_all_courses['content'].str.contains(search_history)].index
        sim_scores = cosine_sim[search_index].mean(axis=0)

        # Sort courses based on similarity scores
        sim_scores = sorted(list(enumerate(sim_scores)), key=lambda x: x[1], reverse=True)
        recommended_course_indices = [i[0] for i in sim_scores]
        return df_all_courses.iloc[recommended_course_indices][:7]['courseName'].tolist()

    if search_history.strip():
        recommendations = get_recommendations_from_search(search_history, df_all_courses, cosine_sim)
    else:
        recommendations = []

    return JsonResponse({'recommendations': recommendations})
