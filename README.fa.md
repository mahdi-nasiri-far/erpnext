<div align="center">
    <a href="https://frappe.io/erpnext">
	<img src="./erpnext/public/images/v16/erpnext.svg" alt="لوگوی ERPNext" height="80px" width="80px"/>
    </a>
    <h2>ERPNext</h2>
    <div align="center">
        <p>سیستم ERP قدرتمند، کاربرپسند و متن‌باز</p>
    </div>

[![Learn on Frappe School](https://img.shields.io/badge/Frappe%20School-Learn%20ERPNext-blue?style=flat-square)](https://frappe.school)<br><br>
[![CI](https://github.com/frappe/erpnext/actions/workflows/server-tests-mariadb.yml/badge.svg?event=schedule)](https://github.com/frappe/erpnext/actions/workflows/server-tests-mariadb.yml)
[![docker pulls](https://img.shields.io/docker/pulls/frappe/erpnext.svg)](https://hub.docker.com/r/frappe/erpnext)

</div>

<div align="center">
	<img src="./erpnext/public/images/v16/hero_image.png" alt="تصویر شاخص ERPNext"/>
</div>

<div align="center">
	<a href="https://erpnext-demo.frappe.cloud/api/method/erpnext_demo.erpnext_demo.auth.login_demo">دموی زنده</a>
	-
	<a href="https://frappe.io/erpnext">وب‌سایت</a>
	-
	<a href="https://docs.frappe.io/erpnext/">مستندات</a>
</div>

## ERPNext

سیستم ERP کاملاً متن‌باز برای اداره کسب‌وکار شما.

### انگیزه

اداره یک کسب‌وکار کار پیچیده‌ای است — رسیدگی به فاکتورها، پیگیری موجودی کالا، مدیریت پرسنل و دیگر عملیات روزمره. در بازاری که نرم‌افزارهای مدیریت هر یک از این کارها جداگانه فروخته می‌شوند، ERPNext همه موارد بالا و حتی بیشتر را به‌رایگان انجام می‌دهد.

### امکانات کلیدی

- **حسابداری**: همه ابزارهای مورد نیاز برای مدیریت جریان نقدی در یک جا؛ از ثبت تراکنش‌ها گرفته تا خلاصه‌سازی و تحلیل گزارش‌های مالی.
- **مدیریت سفارش‌ها**: پیگیری سطوح موجودی، تأمین مجدد کالا و مدیریت سفارش‌های فروش، مشتریان، تأمین‌کنندگان، حمل‌ونقل‌ها، تحویل‌ها و انجام سفارش‌ها.
- **تولید**: چرخه تولید را ساده می‌کند، به پیگیری مصرف مواد کمک می‌کند، برنامه‌ریزی ظرفیت را نمایش می‌دهد، پیمانکاری فرعی را مدیریت می‌کند و امکانات بیشتر!
- **مدیریت دارایی**: از خرید تا واگذاری، از زیرساخت فناوری اطلاعات تا تجهیزات. همه بخش‌های سازمان شما را در یک سیستم متمرکز پوشش می‌دهد.
- **پروژه‌ها**: تحویل پروژه‌های داخلی و خارجی در موعد مقرر، بودجه و سودآوری مورد نظر. پیگیری وظایف، کاربرگ‌ها و مشکلات هر پروژه.

<details open>

<summary>بیشتر</summary>
	<img src="https://erpnext.com/files/v16_bom.png"/>
	<img src="https://erpnext.com/files/v16_stock_summary.png"/>
	<img src="https://erpnext.com/files/v16_job_card.png"/>
	<img src="https://erpnext.com/files/v16_tasks.png"/>
</details>

### زیر کاپوت

- [**Frappe Framework**](https://github.com/frappe/frappe): یک فریم‌ورک وب‌اپلیکیشن فول‌استک نوشته‌شده با Python و JavaScript. این فریم‌ورک بنیانی محکم برای ساخت وب‌اپلیکیشن‌ها فراهم می‌کند و شامل لایه انتزاع پایگاه داده، احراز هویت کاربر و یک REST API است.

- [**Frappe UI**](https://github.com/frappe/frappe-ui): یک کتابخانه رابط کاربری مبتنی بر Vue برای ارائه رابط کاربری مدرن. کتابخانه Frappe UI مجموعه متنوعی از کامپوننت‌ها را ارائه می‌دهد که می‌توان از آن‌ها برای ساخت برنامه‌های تک‌صفحه‌ای بر بستر Frappe Framework استفاده کرد.

## راه‌اندازی در محیط عملیاتی (Production)

### میزبانی مدیریت‌شده

می‌توانید [Frappe Cloud](https://frappecloud.com) را امتحان کنید؛ پلتفرمی ساده، کاربرپسند و پیشرفته و [متن‌باز](https://github.com/frappe/press) برای میزبانی قابل‌اعتماد و امن اپلیکیشن‌های Frappe.

این پلتفرم نصب، راه‌اندازی، ارتقا، پایش، نگهداری و پشتیبانی استقرارهای Frappe شما را بر عهده می‌گیرد. پلتفرمی تمام‌عیار برای توسعه‌دهندگان، با قابلیت مدیریت و کنترل چندین استقرار Frappe.

<div>
	<a href="https://erpnext-demo.frappe.cloud/app/home" target="_blank" rel="noopener noreferrer">
		<picture>
			<source media="(prefers-color-scheme: dark)" srcset="https://frappe.io/files/try-on-fc-white.png">
			<img src="https://frappe.io/files/try-on-fc-black.png" alt="امتحان روی Frappe Cloud" height="28" />
		</picture>
	</a>
</div>


### میزبانی اختصاصی (Self-Hosted)
#### Docker

برای مستندات کامل و پرسش‌های متداول درباره راه‌اندازی Docker، به [مستندات Frappe Docker](https://github.com/frappe/frappe_docker) مراجعه کنید

#### پیش‌نیازها

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose v2](https://docs.docker.com/compose/)
- [git](https://docs.github.com/en/get-started/getting-started-with-git/set-up-git)

> برای مبانی Docker و بهترین شیوه‌ها به [مستندات](https://docs.docker.com) Docker مراجعه کنید

### امتحان در محیط خودتان

> **⚠️ فقط دموی موقت**
>
> **این راه‌اندازی برای ارزیابی سریع در نظر گرفته شده است؛ انتظار داشته باشید که محیط را دور بیندازید.** امکان نصب اپلیکیشن‌های سفارشی روی این راه‌اندازی را نخواهید داشت. برای استقرارهای عملیاتی، پیکربندی‌های سفارشی و توضیحات کامل، به مستندات کامل مراجعه کنید.

ابتدا مخزن را کلون کنید:

```sh
git clone https://github.com/frappe/frappe_docker
cd frappe_docker
```

سپس اجرا کنید:

```sh
docker compose -f pwd.yml up -d
```
چند دقیقه صبر کنید تا سایت ERPNext ساخته شود یا پیش از باز کردن مرورگر روی پورت `8080`، لاگ‌های کانتینر `create-site` را بررسی کنید. (نام کاربری: `Administrator`، گذرواژه: `admin`)

برای راه‌اندازی Docker روی معماری ARM به [Frappe Docker](https://github.com/frappe/frappe_docker/blob/main/docs/01-getting-started/03-arm64.md) مراجعه کنید


## راه‌اندازی محیط توسعه (Development)
### نصب دستی

راه آسان: اسکریپت نصب ما برای bench، همه وابستگی‌ها (مانند MariaDB) را نصب می‌کند. برای جزئیات بیشتر به https://github.com/frappe/bench مراجعه کنید.

گذرواژه‌های جدیدی برای کاربر «Administrator» در ERPNext، کاربر root در MariaDB و کاربر Frappe ساخته می‌شود (اسکریپت، گذرواژه‌ها را نمایش می‌دهد و در فایل ‎~/frappe_passwords.txt ذخیره می‌کند).


### راه‌اندازی محلی

برای راه‌اندازی مخزن به‌صورت محلی، مراحل زیر را دنبال کنید:

1. با دنبال کردن [مراحل نصب](https://frappeframework.com/docs/user/en/installation)، bench را راه‌اندازی کنید و سرور را اجرا کنید
   ```
   bench start
   ```

2. در یک ترمینال جداگانه، دستورات زیر را اجرا کنید:
   ```
   # ایجاد یک سایت جدید
   bench new-site erpnext.localhost
   ```

3. اپلیکیشن ERPNext را دریافت و نصب کنید
   ```
   # دریافت اپلیکیشن ERPNext
   bench get-app https://github.com/frappe/erpnext

   # نصب اپلیکیشن
   bench --site erpnext.localhost install-app erpnext
   ```

4. نشانی `http://erpnext.localhost:8000/app` را در مرورگر خود باز کنید؛ باید برنامه را در حال اجرا ببینید

## بومی‌سازی ایران

این نسخه برای استفاده در ایران آماده شده است. کافی است در هنگام ساخت شرکت، کشور را روی **Iran** بگذارید تا موارد زیر به‌صورت خودکار نصب شوند:

| مورد | توضیح | مسیر |
| --- | --- | --- |
| ترجمهٔ فارسی رابط کاربری | ترجمهٔ کامل فارسی (بیش از ۱۱ هزار رشته)؛ زبان کاربر را روی `fa` بگذارید | `erpnext/locale/fa.po` |
| طرح حساب‌های نمونه ایران | هنگام ساخت شرکت قابل انتخاب است (۶ گروه اصلی، ۱۱۸ حساب، مطابق ساختار دارایی/بدهی/سرمایه/درآمد/بهای تمام‌شده/هزینه) | `erpnext/accounts/doctype/account/chart_of_accounts/verified/ir_chart_of_accounts.json` |
| الگوهای مالیات بر ارزش افزوده | ۹٪ مالیات + ۱٪ عوارض، فروش صادراتی با نرخ صفر، فروش/خرید معاف و خرید وارداتی ۱۰٪ با دسته‌های مالیاتی داخلی/صادرات/معاف | `erpnext/setup/setup_wizard/data/country_wise_tax.json` |
| شناسه‌های قانونی | فیلدهای **شناسه ملی**، **کد اقتصادی** و **شماره ثبت** برای شرکت، مشتری و تأمین‌کننده | `erpnext/regional/iran/setup.py` |
| گزارش مالیات بر ارزش افزوده (ایران) | جمع‌بندی فروش/خرید مشمول، صادراتی و معاف همراه با محاسبهٔ خالص مالیات و عوارض قابل پرداخت یا اعتبار مالیاتی، در قالب اظهارنامهٔ فصلی | `erpnext/regional/report/iran_vat_report` |
| صورت معاملات فصلی (ماده ۱۶۹) | فهرست معاملات هر طرف حساب همراه با کد اقتصادی و شناسه ملی، مبلغ خالص، مالیات و عوارض | `erpnext/regional/report/iran_periodic_transactions` |
| قالب‌های چاپ صورت‌های مالی | ترازنامه، صورت سود و زیان و صورت گردش وجوه نقد در چیدمان استاندارد ایران همراه با بخش امضاها (تهیه‌کننده، مدیر مالی، مدیرعامل، رئیس هیئت‌مدیره) | `erpnext/regional/print_format/iran_*` |

> **نکته:** گزارش‌های مالیاتی از فیلترهای «شرکت»، «از تاریخ» و «تا تاریخ» استفاده می‌کنند؛ برای اظهارنامهٔ فصلی، بازهٔ سه‌ماههٔ مورد نظر را وارد کنید.

## آموزش و انجمن

1. [Frappe School](https://school.frappe.io) - آموزش Frappe Framework و ERPNext از طریق دوره‌های مختلف، توسط نگهدارندگان پروژه یا انجمن.
2. [مستندات رسمی](https://docs.erpnext.com/) - مستندات جامع ERPNext.
3. [انجمن گفتگو](https://discuss.frappe.io/c/erpnext/6) - با انجمن کاربران و ارائه‌دهندگان خدمات ERPNext در ارتباط باشید.
4. [گروه تلگرام](https://erpnext_public.t.me) - از جامعه بزرگ کاربران، کمک فوری بگیرید.


## مشارکت

1. [راهنمای ثبت مشکل](https://github.com/frappe/erpnext/wiki/Issue-Guidelines)
2. [گزارش آسیب‌پذیری‌های امنیتی](https://erpnext.com/security)
3. [الزامات Pull Request](https://github.com/frappe/erpnext/wiki/Contribution-Guidelines)
4. [ترجمه‌ها](https://crowdin.com/project/frappe)


## سیاست لوگو و علامت تجاری

لطفاً [سیاست لوگو و علامت تجاری](TRADEMARK_POLICY.md) ما را مطالعه کنید.

<br />
<br />
<div align="center" style="padding-top: 0.75rem;">
	<a href="https://frappe.io" target="_blank">
		<picture>
			<source media="(prefers-color-scheme: dark)" srcset="https://frappe.io/files/Frappe-white.png">
			<img src="https://frappe.io/files/Frappe-black.png" alt="Frappe Technologies" height="28"/>
		</picture>
	</a>
</div>
