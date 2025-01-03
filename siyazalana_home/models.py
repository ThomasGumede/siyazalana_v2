from django.db import models
from accounts.models import AbstractCreate
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.urls import reverse
from django.template.defaultfilters import slugify
from tinymce.models import HTMLField

from siyazalana_home.utilities.file_handlers import handle_post_file_upload

class BlogCategory(AbstractCreate):
    thumbnail = models.ImageField(upload_to="category/", null=True, blank=True)
    slug = models.SlugField(max_length=350, unique=True, db_index=True)
    label = models.CharField(max_length=250, unique=True)
    

    def __str__(self):
        return str(self.label)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.label)
        super(BlogCategory, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Categorie")
        verbose_name_plural = _("Categories")
   
class Blog(AbstractCreate):
    image = models.ImageField(help_text=_("Upload news image."), upload_to=handle_post_file_upload, blank=True, null=True)
    title = models.CharField(help_text=_("Enter title for your news"), max_length=150)
    description = models.CharField(help_text=_("Write a short description about this post"), max_length=200)
    slug = models.SlugField(max_length=250, blank=True, unique=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_DEFAULT, default=None, related_name="posts", null=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.PROTECT, related_name="posts")
    content = HTMLField()

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def save(self, *args, **kwargs):
        original_slug = slugify(self.title)
        queryset =  Blog.objects.all().filter(slug__iexact=original_slug).count()

        count = 1
        slug = original_slug
        while(queryset):
            slug = original_slug + '-' + str(count)
            count += 1
            queryset = Blog.objects.all().filter(slug__iexact=slug).count()

        self.slug = slug
        super(Blog, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.title}"
    

    
    def get_absolute_url(self):
        return reverse("bbgi_home:details-blog", kwargs={"post_slug": self.slug})

class Comment(AbstractCreate):
    commenter = models.ForeignKey(get_user_model(), related_name="comments", on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

class EmailModel(AbstractCreate):
    subject = models.CharField(max_length=70)
    from_email = models.EmailField()
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    message = models.TextField(max_length=500)
    task_id = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Email'
        verbose_name_plural = 'Emails'
        ordering = ["created"]

    def __str__(self) -> str:
        return self.subject

    def save(self, *args, **kwargs):
        super(EmailModel, self).save(*args, **kwargs)

PRIVACY_TITLES = (
    ("Website Terms and Community Guidlines", "Website Terms and Community Guidlines"),
    ("Refund Policy", "Refund Policy"),
    ("Privacy Policy", "Privacy Policy"),
    ("Terms of use: Consumers", "Terms of use: Consumers"),
    ("Terms of use: Organisers", "Terms of use: Organisers")
)

class Privacy(AbstractCreate):
    title = models.CharField(max_length=150, unique=True, choices=PRIVACY_TITLES)
    slug = models.SlugField(max_length=250, unique=True, db_index=True)
    description = models.CharField(max_length=160)
    content = HTMLField()

    class Meta:
        verbose_name = 'Privacy'
        verbose_name_plural = 'Privacys'
        ordering = ['created']

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("home:privacy", kwargs={"terms_slug": self.slug})
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Privacy, self).save(*args, **kwargs)

class FAQ(AbstractCreate):
    question = models.CharField(max_length=250)
    answer = models.CharField(max_length=550)

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question

class Member(AbstractCreate):
    image = models.ImageField(help_text = _(""), upload_to="home/images/team", null=True, blank=True)
    full_names = models.CharField(help_text=_("Enter member full names"), max_length=250)
    slug = models.SlugField(max_length=350)
    role = models.CharField(help_text=_("Enter member role"), max_length=250)
    decription = HTMLField(blank=True, null=True, help_text=_("Describe the team member"))

    def __str__(self):
        return self.full_names
    
    def save(self, *args, **kwargs):
        original_slug = slugify(self.full_names)
        queryset =  Member.objects.all().filter(slug__iexact=original_slug).count()

        count = 1
        slug = original_slug
        while(queryset):
            slug = original_slug + '-' + str(count)
            count += 1
            queryset = Member.objects.all().filter(slug__iexact=slug).count()

        self.slug = slug
        super(Member, self).save(*args, **kwargs)

@receiver(pre_delete, sender=Blog)
def delete_Post_image_hook(sender, instance, using, **kwargs):
    instance.image.delete()

