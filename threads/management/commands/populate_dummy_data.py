import os
import random
import django
from django.utils import text

# Setup for standalone script execution
# Change 'your_project_name' to your actual project name
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')
django.setup()

from django.contrib.auth import get_user_model
from courses.models import Department, Course, Resource
from threads.models import Category, Tag, Thread, Reply, Report

User = get_user_model()

def populate_data():
    print("--- Starting Population Script ---")

    # 1. Create Users (Students and Moderators)
    # Task requirement: Authenticated BITS Email users 
    users = []
    for i in range(5):
        user, _ = User.objects.get_or_create(
            username=f'student{i}',
            email=f'f2023{i}@pilani.bits-pilani.ac.in',
            first_name=f'Student {i}',
            last_name='User'
        )
        users.append(user)
    
    admin_user, _ = User.objects.get_or_create(
        username='moderator_pro',
        email='admin@pilani.bits-pilani.ac.in',
        is_staff=True
    )
    users.append(admin_user)

    # 2. Create Departments & Courses [cite: 52-55]
    cs_dept, _ = Department.objects.get_or_create(name="Computer Science")
    phy_dept, _ = Department.objects.get_or_create(name="Physics")

    courses_data = [
        {"code": "CS F111", "title": "Computer Programming", "dept": cs_dept},
        {"code": "CS F211", "title": "Data Structures and Algorithms", "dept": cs_dept},
        {"code": "PHY F111", "title": "Mecht Oscil & Waves", "dept": phy_dept},
    ]

    courses = []
    for data in courses_data:
        course, _ = Course.objects.get_or_create(
            code=data['code'], 
            title=data['title'], 
            department=data['dept']
        )
        courses.append(course)

    # 3. Create Resources [cite: 56-59]
    resources = []
    for course in courses:
        res, _ = Resource.objects.get_or_create(
            course=course,
            title=f"{course.code} Handout",
            type="PDF",
            link=f"https://studydeck.bits/res/{course.code.replace(' ', '')}"
        )
        resources.append(res)

    # 4. Create Categories & Tags [cite: 69, 87]
    categories = []
    for cat_name in ["General Queries", "Exam Prep", "Resource Sharing"]:
        cat, _ = Category.objects.get_or_create(name=cat_name)
        categories.append(cat)

    tags = []
    tag_data = [("#midsem", "#FF5733"), ("#urgent", "#C70039"), ("#quiz1", "#33FF57")]
    for name, color in tag_data:
        tag, _ = Tag.objects.get_or_create(name=name, color=color)
        tags.append(tag)

    # 5. Create Threads (Discussions) [cite: 73-77]
    threads = []
    for i in range(10):
        thread = Thread.objects.create(
            title=f"Question about {random.choice(courses).code} - Topic {i}",
            raw_content=f"Can someone help me understand the concept in topic {i}?",
            author=random.choice(users),
            category=random.choice(categories)
        )
        # Link Courses and Tags
        thread.tagged_courses.add(random.choice(courses))
        thread.tags.add(random.choice(tags))
        threads.append(thread)

    # 6. Create Replies and Upvotes [cite: 79, 86]
    for thread in threads:
        for j in range(random.randint(1, 4)):
            reply = Reply.objects.create(
                thread=thread,
                author=random.choice(users),
                raw_content=f"This is a helpful response number {j} for this thread."
            )
            # Add some random upvotes
            for _ in range(random.randint(0, 3)):
                reply.update_upvotes(random.choice(users))
        
        # Add upvotes to thread
        for _ in range(random.randint(0, 5)):
            thread.update_upvotes(random.choice(users))

    # 7. Create Reports [cite: 89-91]
    Report.objects.create(
        reporter=users[0],
        thread=threads[0],
        reason="Inappropriate language in the discussion.",
        status=Report.StatusChoices.PENDING
    )

    print(f"--- Population Complete! ---")
    print(f"Created: {len(users)} Users, {len(courses)} Courses, {len(threads)} Threads.")

if __name__ == "__main__":
    populate_data()
