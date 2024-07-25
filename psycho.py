# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Assignment(models.Model):
    courseid = models.ForeignKey('Course', models.DO_NOTHING, db_column='courseId')  # Field name made lowercase.
    title = models.TextField()
    instruction = models.TextField()
    deadline = models.DateTimeField()
    points = models.FloatField()
    attachment = models.TextField()
    instructorid = models.ForeignKey('User', models.DO_NOTHING, db_column='instructorId')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Assignment'


class Assignmentsubmission(models.Model):
    assignmentid = models.ForeignKey(Assignment, models.DO_NOTHING, db_column='assignmentId')  # Field name made lowercase.
    studentid = models.ForeignKey('User', models.DO_NOTHING, db_column='studentId')  # Field name made lowercase.
    attachment = models.TextField()
    points = models.FloatField()
    feedback = models.TextField()
    submittedat = models.DateTimeField(db_column='submittedAt')  # Field name made lowercase.
    comment = models.TextField()
    isreturn = models.BooleanField(db_column='isReturn')  # Field name made lowercase.
    returnedat = models.DateTimeField(db_column='returnedAt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AssignmentSubmission'


class Cart(models.Model):
    courseid = models.ForeignKey('Course', models.DO_NOTHING, db_column='courseId')  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    craetedat = models.DateTimeField(db_column='craetedAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.
    ischeckout = models.BooleanField(db_column='isCheckout')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Cart'


class Conversation(models.Model):
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Conversation'


class Course(models.Model):
    coursecategoryid = models.ForeignKey('Coursecategory', models.DO_NOTHING, db_column='courseCategoryId')  # Field name made lowercase.
    language = models.TextField()  # This field type is a guess.
    price = models.FloatField()
    discountpercent = models.FloatField(db_column='discountPercent', blank=True, null=True)  # Field name made lowercase.
    rating = models.FloatField(blank=True, null=True)
    ratingcount = models.IntegerField(db_column='ratingCount')  # Field name made lowercase.
    enrollcount = models.IntegerField(db_column='enrollCount')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.
    authorid = models.ForeignKey('User', models.DO_NOTHING, db_column='authorId')  # Field name made lowercase.
    isverified = models.BooleanField(db_column='isVerified')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Course'


class Coursecategory(models.Model):
    name = models.TextField()
    coursedomainid = models.ForeignKey('Coursedomain', models.DO_NOTHING, db_column='courseDomainId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CourseCategory'


class Coursedomain(models.Model):
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'CourseDomain'


class Coursereview(models.Model):
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    description = models.CharField(max_length=500)
    rating = models.FloatField()
    updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.
    courseid = models.ForeignKey(Course, models.DO_NOTHING, db_column='courseId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CourseReview'


class Coursereviewreply(models.Model):
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    description = models.CharField(max_length=500)
    updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.
    idcoursereview = models.IntegerField(db_column='idCourseReview')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CourseReviewReply'


class Enrolledcourse(models.Model):
    courseid = models.ForeignKey(Course, models.DO_NOTHING, db_column='courseId')  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    enrolledat = models.DateTimeField(db_column='enrolledAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EnrolledCourse'


class Game(models.Model):
    viewscount = models.IntegerField(db_column='viewsCount')  # Field name made lowercase.
    coursecategoryid = models.ForeignKey(Coursecategory, models.DO_NOTHING, db_column='courseCategoryId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Game'


class Gameview(models.Model):
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    gameid = models.ForeignKey(Game, models.DO_NOTHING, db_column='gameId')  # Field name made lowercase.
    viewtime = models.TextField(db_column='viewTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GameView'


class Gamificationdata(models.Model):
    text = models.TextField()
    imageurl = models.TextField(db_column='imageUrl', blank=True, null=True)  # Field name made lowercase.
    gameid = models.ForeignKey(Game, models.DO_NOTHING, db_column='gameId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GamificationData'


class Message(models.Model):
    message = models.TextField()
    senderid = models.ForeignKey('User', models.DO_NOTHING, db_column='senderId')  # Field name made lowercase.
    receiverid = models.ForeignKey('User', models.DO_NOTHING, db_column='receiverId')  # Field name made lowercase.
    conversationid = models.ForeignKey(Conversation, models.DO_NOTHING, db_column='conversationId')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Message'


class Oauthuser(models.Model):
    fullname = models.TextField(db_column='fullName')  # Field name made lowercase.
    email = models.TextField()
    avatarurl = models.TextField(db_column='avatarUrl', blank=True, null=True)  # Field name made lowercase.
    oauthid = models.TextField(db_column='oauthId')  # Field name made lowercase.
    oauthprovider = models.TextField(db_column='oauthProvider', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'OAuthUser'





class Payment(models.Model):
    paymentmethod = models.TextField(db_column='paymentMethod')  # Field name made lowercase.
    amount = models.FloatField()
    txnid = models.OneToOneField('Transaction', models.DO_NOTHING, db_column='txnId')  # Field name made lowercase.
    userid = models.IntegerField(db_column='userId')  # Field name made lowercase.
    courseid = models.IntegerField(db_column='courseId')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Payment'


class Qna(models.Model):
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    description = models.CharField(max_length=500)
    updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.
    responsecount = models.IntegerField(db_column='responseCount')  # Field name made lowercase.
    courseid = models.ForeignKey(Course, models.DO_NOTHING, db_column='courseId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QnA'


class Qnareply(models.Model):
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    description = models.CharField(max_length=500)
    updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.
    idqna = models.IntegerField(db_column='idQnA')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QnAReply'


class Searchhistory(models.Model):
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    query = models.TextField()

    class Meta:
        managed = False
        db_table = 'SearchHistory'


class Socialhandle(models.Model):
    website = models.TextField(unique=True, blank=True, null=True)
    twitter = models.TextField(unique=True, blank=True, null=True)
    youtube = models.TextField(unique=True, blank=True, null=True)
    linkdin = models.TextField(unique=True, blank=True, null=True)
    facebook = models.TextField(unique=True, blank=True, null=True)
    userid = models.OneToOneField('User', models.DO_NOTHING, db_column='userId', blank=True, null=True)  # Field name made lowercase.
    google = models.TextField(unique=True, blank=True, null=True)
    oauthuserid = models.ForeignKey(Oauthuser, models.DO_NOTHING, db_column='oAuthUserId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SocialHandle'


class Swiper(models.Model):
    image = models.TextField()
    isvisible = models.BooleanField(db_column='isVisible')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Swiper'


class Transaction(models.Model):
    amt = models.FloatField()
    oid = models.TextField(unique=True)
    refid = models.TextField()
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Transaction'


class User(models.Model):
    fullname = models.TextField(db_column='fullName')  # Field name made lowercase.
    email = models.TextField(unique=True)
    password = models.TextField()
    role = models.TextField()  # This field type is a guess.
    avatar = models.TextField(blank=True, null=True)
    birthdate = models.DateTimeField(blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    oauthid = models.TextField(db_column='oauthId', blank=True, null=True)  # Field name made lowercase.
    oauthprovider = models.TextField(db_column='oauthProvider', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'User'


class Conversationtouser(models.Model):
    a = models.ForeignKey(Conversation, models.DO_NOTHING, db_column='A')  # Field name made lowercase.
    b = models.ForeignKey(User, models.DO_NOTHING, db_column='B')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '_ConversationToUser'
        unique_together = (('a', 'b'),)


class PrismaMigrations(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    checksum = models.CharField(max_length=64)
    finished_at = models.DateTimeField(blank=True, null=True)
    migration_name = models.CharField(max_length=255)
    logs = models.TextField(blank=True, null=True)
    rolled_back_at = models.DateTimeField(blank=True, null=True)
    started_at = models.DateTimeField()
    applied_steps_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = '_prisma_migrations'
