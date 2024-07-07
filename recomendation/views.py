from django.http import JsonResponse
from .models import Enrolledcourse, Course  # Ensure Course model is imported

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def fetchEnrollment(request, userid):
    enrollments = Enrolledcourse.objects.filter(userid=userid)
    all_courses = Course.objects.all()

    if enrollments.exists() and all_courses.exists():
        # Create a list to hold all enrollment details
        enrollment_details = []
        
        for enrollment in enrollments:
            details = {
                'userId': enrollment.userid.id,
                'userName': enrollment.userid.fullname,
                'courseId': enrollment.courseid.id,
                'courseName': enrollment.courseid.title,
                'courseCategory': enrollment.courseid.coursecategoryid.name,
                'courseDescription': enrollment.courseid.description,
                'objective': enrollment.courseid.objective,
                'requirement': enrollment.courseid.requirement,
                'syllabus': enrollment.courseid.syllabus
            }
            enrollment_details.append(details)

        # Create a list to hold all course details
        course_details = []
        
        for course in all_courses:
            details = {
                'courseId': course.id,
                'courseName': course.title,
                'courseCategory': course.coursecategoryid.name,
                'courseDescription': course.description,
                'objective': course.objective,
                'requirement': course.requirement,
                'syllabus': course.syllabus
            }
            course_details.append(details)

        # Convert to DataFrame
        df_user_courses = pd.DataFrame(enrollment_details)
        df_all_courses = pd.DataFrame(course_details)

        # Fill missing values with empty strings
        df_all_courses = df_all_courses.fillna('')

        # Combine relevant text fields into a single feature for all courses
        df_all_courses['content'] = (
            df_all_courses['courseName'] + " " +
            df_all_courses['courseCategory'] + " " +
            df_all_courses['courseDescription'] + " " +
            df_all_courses['objective'] + " " +
            df_all_courses['requirement'] + " " +
            df_all_courses['syllabus']
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
            
            # Return the top 10 recommended courses
            return df_all_courses.iloc[recommended_course_indices][:5]['courseName'].tolist()
        
        # Example usage
        recommendations = get_recommendations(userid, df_user_courses, df_all_courses, cosine_sim)
        
        return JsonResponse({'recommendations': recommendations})
    else:
        return JsonResponse({'error': 'Enrollment or Courses Not Found'})
