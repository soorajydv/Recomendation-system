import pymongo
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from django.http import JsonResponse
from django.shortcuts import render
from .models import Enrolledcourse

# Establish connection to MongoDB
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['course']
courses_collection = db['courses']

def fetchEnrollment(request, userid):
    if client:
        print("MongoDb Connected")

    # Fetch enrollments from PostgreSQL
    enrollments = Enrolledcourse.objects.filter(userid=userid).values()

    if enrollments.exists():
        enrollment_details = []

        for enrollment in enrollments:
            course_id = enrollment['courseid_id']  # Get the course ID from the enrollment
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

        # Convert to DataFrame
        df_user_courses = pd.DataFrame(enrollment_details)
        df_all_courses = pd.DataFrame(course_details)

        # Debug: Print columns of the DataFrame to verify column names
        print("Columns in df_user_courses:", df_user_courses.columns)
        print("Columns in df_all_courses:", df_all_courses.columns)

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

        # Function to get course recommendations
        def get_recommendations(userid, df_user_courses, df_all_courses, cosine_sim):
            # Find all courses taken by the given user
            user_courses = df_user_courses[df_user_courses['userId'] == userid]['courseId'].tolist()

            # Calculate the mean cosine similarity score for each course based on user's courses
            user_course_indices = df_all_courses[df_all_courses['courseId'].isin(user_courses)].index.tolist()
            sim_scores = cosine_sim[user_course_indices].mean(axis=0)
            
            # Sort courses based on similarity scores
            sim_scores = sorted(list(enumerate(sim_scores)), key=lambda x: x[1], reverse=True)
            
            # Get the top recommended courses indices excluding user's own courses
            recommended_course_indices = [i[0] for i in sim_scores if df_all_courses.iloc[i[0]]['courseId'] not in user_courses]
            
            # Return the top 3 recommended courses
            return df_all_courses.iloc[recommended_course_indices][:3]['courseName'].tolist()

        # Example usage
        recommendations = get_recommendations(userid, df_user_courses, df_all_courses, cosine_sim)
        
        return JsonResponse({'recommendations': recommendations})
    else:
        return JsonResponse({'error': 'No enrollments found for this user'})



def course_list(request):
    # Fetch all documents from the 'courses' collection and convert the cursor to a list
    courses = list(courses_collection.find())

    # Render the template with the courses data
    return render(request, 'courses/course_list.html', {'courses': courses})


