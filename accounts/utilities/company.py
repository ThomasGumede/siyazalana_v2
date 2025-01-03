from django.utils import timezone
from accounts.models import AboutCompany

try:
    company = AboutCompany.objects.get(slug="about-bbgi-model")
    COMPANY = {
        "facebook": company.facebook,
        "tiktok": "https://wwww.tiktok.com/@BBGInitiative",
        "instagram": company.instagram,
        "linkedIn": company.linkedIn,
        "website": "https://bbgi.co.za",
        "company_support_mail": company.email,
        "phone": company.phone,
        "youtube": "https://www.youtube.com/@blackbusinessgrowthinitiat6153",
        "address": f"{company.city}, {company.province}, {company.zipcode}, RSA", 
        "company_city": company.city,
        "company_state": company.province,
        "company_zipcode": company.zipcode,
        "vision": company.vision,
        "mission": company.mission

    }
except:

    COMPANY = {
        "facebook": "https://www.facebook.com/blackbusinessgrowthinitiave",
        "tiktok": "https://wwww.tiktok.com/@BBGInitiative",
        "instagram": "https://www.instagram.com/blackbusinessgrowthinitiave",
        "linkedIn": "https://www.linkedin.com/company/black-business-growth-initiative/posts/",
        "website": "https://bbgi.co.za",
        "company_support_mail": "info@bbgi.co.za",
        "phone": "021 830 5415",
        "youtube": "https://www.youtube.com/@blackbusinessgrowthinitiat6153",
        "address": "Cape Town, 7441, RSA",
        "company_city": "COMPANY.city",
        "company_state": "COMPANY.province",
        "company_zipcode": "zipcode",
        "vision": """To become the leading platform that unites and empowers Black African entrepreneurs and professionals, fostering a
                        thriving, collaborative community that drives economic growth, innovation, and sustainable success across
                        South Africa and beyond.""",
        "mission": """
        Our mission is to support and promote the growth of Black African businesses and careers by providing a platform to
                        showcase expertise, facilitating impactful networking opportunities, delivering business education and mentorship,
                        fostering unity and collaboration, and driving initiatives that empower and sustain Black-owned businesses.
        """

    }

def generate_order_number(model) -> str:
    order_id_start = f'BBGI{timezone.now().year}{timezone.now().month}'
    queryset = model.objects.filter(order_id__iexact=order_id_start).count()
      
    count = 1
    order_id = order_id_start
    while(queryset):
        order_id = f'BBGI{timezone.now().year}{timezone.now().month}{count}'
        count += 1
        queryset = model.objects.all().filter(order_id__iexact=order_id).count()

    return order_id