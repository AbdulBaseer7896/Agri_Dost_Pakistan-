"""
Quick setup script: creates admin user, default site settings, and sample data.
Run after migrations: python setup_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agri_dost.settings')
django.setup()

from django.contrib.auth.models import User
from api.models import Category, Product, SiteSettings, Testimonial, HeroBanner


def create_admin():
    if not User.objects.filter(username='saeedadmin').exists():
        User.objects.create_superuser('saeedadmin', 'saeedadmin@gmail.com', 'saeed@786')
        print('✓ Admin user created (username: saeedadmin / password: saeed@786)')
    else:
        print('• Admin already exists')


def create_site_settings():
    SiteSettings.get_settings()  # creates default if missing
    print('✓ Site settings ready')


def create_categories():
    cats = [
        {'name_en': 'Seeds', 'name_ur': 'بیج', 'order': 1},
        {'name_en': 'Fertilizers', 'name_ur': 'کھاد', 'order': 2},
        {'name_en': 'Pesticides', 'name_ur': 'کیڑے مار ادویات', 'order': 3},
        {'name_en': 'Tools', 'name_ur': 'اوزار', 'order': 4},
        {'name_en': 'Animal Feed', 'name_ur': 'جانوروں کی خوراک', 'order': 5},
        {'name_en': 'Irrigation', 'name_ur': 'آبپاشی', 'order': 6},
    ]
    created = 0
    for c in cats:
        _, was_created = Category.objects.get_or_create(name_en=c['name_en'], defaults=c)
        if was_created:
            created += 1
    print(f'✓ Categories: {created} new, {Category.objects.count()} total')


def create_products():
    if Product.objects.exists():
        print(f'• Products already exist ({Product.objects.count()})')
        return

    seeds = Category.objects.filter(name_en='Seeds').first()
    fertilizers = Category.objects.filter(name_en='Fertilizers').first()
    pesticides = Category.objects.filter(name_en='Pesticides').first()

    products = [
        {
            'name_en': 'Premium Wheat Seeds (Galaxy-2013)',
            'name_ur': 'پریمیم گندم کے بیج (گیلیکسی-2013)',
            'short_description_en': 'High-yield wheat variety, disease resistant',
            'short_description_ur': 'زیادہ پیداوار، بیماریوں سے محفوظ',
            'description_en': 'Galaxy-2013 is one of the highest yielding wheat varieties in Pakistan. It produces 60-70 maunds per acre under good conditions. Disease resistant and suitable for all Punjab regions.',
            'description_ur': 'گیلیکسی-2013 پاکستان میں سب سے زیادہ پیداوار دینے والی گندم کی اقسام میں سے ایک ہے۔ یہ اچھے حالات میں فی ایکڑ 60-70 من پیداوار دیتی ہے۔',
            'price': 4500, 'discount_price': 3999,
            'unit_en': 'per 40kg bag', 'unit_ur': 'فی 40 کلو بوری',
            'stock': 100, 'is_featured': True, 'category': seeds,
        },
        {
            'name_en': 'Hybrid Cotton Seeds (FH-Lalazar)',
            'name_ur': 'ہائبرڈ کپاس کے بیج (ایف ایچ-لالہ زار)',
            'short_description_en': 'BT cotton, high yield variety',
            'short_description_ur': 'بی ٹی کپاس، زیادہ پیداوار',
            'description_en': 'Premium BT cotton seeds with excellent boll size and fiber quality. Suitable for Punjab and Sindh climate.',
            'description_ur': 'بہترین کوالٹی کے بی ٹی کپاس کے بیج۔ پنجاب اور سندھ کے موسم کے لیے موزوں۔',
            'price': 8500,
            'unit_en': 'per kg', 'unit_ur': 'فی کلو',
            'stock': 50, 'is_featured': True, 'category': seeds,
        },
        {
            'name_en': 'Urea Fertilizer (50kg bag)',
            'name_ur': 'یوریا کھاد (50 کلو بوری)',
            'short_description_en': 'Sona Urea, 46% Nitrogen',
            'short_description_ur': 'سونا یوریا، 46% نائٹروجن',
            'description_en': 'Sona Urea by FFC contains 46% nitrogen. Essential for crop growth, leaf development, and overall yield improvement.',
            'description_ur': 'ایف ایف سی کا سونا یوریا، 46% نائٹروجن پر مشتمل۔ فصلوں کی نشوونما کے لیے ضروری۔',
            'price': 5800,
            'unit_en': 'per 50kg bag', 'unit_ur': 'فی 50 کلو بوری',
            'stock': 200, 'is_featured': True, 'category': fertilizers,
        },
        {
            'name_en': 'DAP Fertilizer (50kg bag)',
            'name_ur': 'ڈی اے پی کھاد (50 کلو بوری)',
            'short_description_en': 'High quality DAP, 18-46-0',
            'short_description_ur': 'اعلیٰ معیار کی ڈی اے پی، 18-46-0',
            'description_en': 'Diammonium Phosphate fertilizer ideal for sowing time. Provides phosphorus essential for root growth.',
            'description_ur': 'ڈائی امونیم فاسفیٹ کھاد، بوائی کے وقت کے لیے بہترین۔',
            'price': 12500, 'discount_price': 11800,
            'unit_en': 'per 50kg bag', 'unit_ur': 'فی 50 کلو بوری',
            'stock': 150, 'is_featured': True, 'category': fertilizers,
        },
        {
            'name_en': 'Hybrid Maize Seeds',
            'name_ur': 'ہائبرڈ مکئی کے بیج',
            'short_description_en': 'Pioneer hybrid, 110-day variety',
            'short_description_ur': 'پائیونیر ہائبرڈ، 110 دن میں تیار',
            'description_en': 'Pioneer hybrid maize seeds. Mature in 110-115 days. Average yield 80-100 maunds per acre.',
            'description_ur': 'پائیونیر ہائبرڈ مکئی کے بیج۔ 110-115 دن میں تیار۔ اوسط پیداوار فی ایکڑ 80-100 من۔',
            'price': 3200,
            'unit_en': 'per kg', 'unit_ur': 'فی کلو',
            'stock': 80, 'is_featured': False, 'category': seeds,
        },
        {
            'name_en': 'Insecticide Spray (1 Litre)',
            'name_ur': 'کیڑے مار سپرے (1 لیٹر)',
            'short_description_en': 'Effective against bollworm and aphids',
            'short_description_ur': 'سنڈیوں اور تیلے کے خلاف مؤثر',
            'description_en': 'Broad spectrum insecticide effective against most cotton and vegetable pests. Safe when used as per instructions.',
            'description_ur': 'وسیع رینج کا کیڑے مار، کپاس اور سبزیوں کے زیادہ تر کیڑوں کے خلاف مؤثر۔',
            'price': 2800,
            'unit_en': 'per litre', 'unit_ur': 'فی لیٹر',
            'stock': 60, 'is_featured': True, 'category': pesticides,
        },
        {
            'name_en': 'Sugarcane Seedlings (CPF-247)',
            'name_ur': 'گنے کی پنیری (سی پی ایف-247)',
            'short_description_en': 'High sugar content variety',
            'short_description_ur': 'زیادہ چینی والی قسم',
            'description_en': 'Premium quality sugarcane variety with high sugar content. Disease resistant and suitable for early sowing.',
            'description_ur': 'اعلیٰ معیار کی گنے کی قسم، زیادہ چینی پیدا کرنے والی۔',
            'price': 350,
            'unit_en': 'per 100 sets', 'unit_ur': 'فی 100 سیٹ',
            'stock': 1000, 'is_featured': False, 'category': seeds,
        },
        {
            'name_en': 'NPK Compound Fertilizer',
            'name_ur': 'این پی کے مرکب کھاد',
            'short_description_en': 'Balanced 15-15-15 NPK',
            'short_description_ur': 'متوازن 15-15-15 این پی کے',
            'description_en': 'Balanced NPK fertilizer suitable for all crops. Provides nitrogen, phosphorus, and potassium in equal ratios.',
            'description_ur': 'تمام فصلوں کے لیے متوازن این پی کے کھاد۔',
            'price': 9500,
            'unit_en': 'per 50kg bag', 'unit_ur': 'فی 50 کلو بوری',
            'stock': 75, 'is_featured': False, 'category': fertilizers,
        },
    ]
    for p in products:
        Product.objects.create(**p)
    print(f'✓ Created {len(products)} sample products')


def create_testimonials():
    if Testimonial.objects.exists():
        print(f'• Testimonials already exist ({Testimonial.objects.count()})')
        return
    items = [
        {
            'customer_name': 'Muhammad Aslam',
            'location': 'Multan, Punjab',
            'title_en': 'Best wheat seeds I ever used',
            'title_ur': 'بہترین گندم کے بیج جو میں نے استعمال کیے',
            'description_en': 'I bought wheat seeds from Agri Dost last year and got 65 maunds per acre. Quality is excellent and delivery was fast.',
            'description_ur': 'پچھلے سال میں نے زرعی دوست سے گندم کے بیج خریدے اور فی ایکڑ 65 من پیداوار حاصل کی۔ معیار بہترین ہے۔',
            'rating': 5, 'order': 1,
        },
        {
            'customer_name': 'Allah Ditta',
            'location': 'Bahawalpur',
            'title_en': 'Trusted source for quality fertilizer',
            'title_ur': 'اعلیٰ معیار کی کھاد کا قابل اعتماد ذریعہ',
            'description_en': 'Original DAP and urea at fair prices. Never had any complaints in 2 years.',
            'description_ur': 'اصلی ڈی اے پی اور یوریا مناسب قیمت پر۔ 2 سال میں کبھی شکایت نہیں ہوئی۔',
            'rating': 5, 'order': 2,
        },
        {
            'customer_name': 'Ghulam Mustafa',
            'location': 'Sahiwal',
            'title_en': 'Excellent customer service',
            'title_ur': 'بہترین کسٹمر سروس',
            'description_en': 'They helped me choose the right seeds for my soil. Great experience!',
            'description_ur': 'انہوں نے میری زمین کے لیے صحیح بیج چننے میں میری مدد کی۔',
            'rating': 5, 'order': 3,
        },
    ]
    for it in items:
        Testimonial.objects.create(**it)
    print(f'✓ Created {len(items)} sample testimonials')


if __name__ == '__main__':
    print('=== Setting up Agri Dost Pakistan ===\n')
    create_admin()
    create_site_settings()
    create_categories()
    create_products()
    create_testimonials()
    print('\n=== Setup complete! ===')
    print('\nLogin credentials:')
    print('  Username: admin')
    print('  Password: admin123')
    print('\n⚠️  IMPORTANT: Change the password after first login!')
