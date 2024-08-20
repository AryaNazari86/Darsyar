from .credintials import SUPPORT_USERNAME

start = """سلام {}  👋
🏫 به کمک درسیار میتونی در هر زمان و مکانی به سوالات درسی دسترسی داشته باشی!

🔔 لطفا در [کانال اطلاع رسانی درسیار](ble.ir/join/33meCDte4u) در بله عضو شو 🔔

📖 ویژگی های درسیار:
💫 دسترسی به سوالات درسی در هر پایه و مبحثی
💫 تصحیح پاسخ شما به وسیله هوش مصنوعی
💫 ساخت آزمون به صورت فایل pdf

🏅با ارسال پاسخ به هوش مصنوعی از طریق بخش سوال جدید، می‌تونی امتیاز کسب کنی و با بقیه‌ی کاربران برای جایزه رقابت کنی.

📋 در طول مسیر، از راهنمایی ها و منویی که زیر پیام‌ها و در مکان کیبورد برای تو باز میشه استفاده کن. اگر هنگام کار با ربات منو برات نیومد، یک بار باز و بستَش کن!

🙋‍♂️ برای شروع، نقش خودت رو انتخاب کن:"""

new_grade = """⚙️ *تغییر پایه تحصیلی* ⚙️

پایه تحصیلی‌تون رو انتخاب کنید:"""

confirm_grade = """🎓 شما در {} هستید.

🙋‍♂️ هر جا مشکلی داشتی، از دستور /help استفاده کن."""

check_if_joined = "🔍 بررسی عضویت"

join_channel = """🙋‍♂️ کاربر عزیز! *این ربات کاملا رایگانه!*

⬅️ اما ممنون میشیم برای حمایت از ما عضو کانال درسیار بشی: [کانال درسیار](ble.ir/join/33meCDte4u)

⚠️ بعد از عضویت در کانال، روی گزینه *بررسی عضویت* بزن تا ربات برات فعال بشه"""

log = """{}

 👤 {} : {} 

🎓 {}، {}، {}, {}"""

channel = """🔔 لینک کانال اطلاع رسانی بات درسیار در بله:‌ [لینک کانال](ble.ir/join/33meCDte4u)

🗣️ بات ما را به دوستان خود معرفی کنید"""

support = """💬 برای پشتیبانی با آیدی @arya_nazari در بله در تماس باشید.

📧 همچنین می‌توانید به آدرس darsyar.balebot@gmail.com ایمیل بزنید."""

unknown = """🥺 متاسفانه متوجه پیامت نشدم.

✅ لطفا برای استفاده از بات، از منوی زیر گزینه‌ی مد نظرت رو انتخاب کن."""

student = "👨‍🎓 دانش آموز"
teacher = "👨‍🏫 مدرس"

choose_class = """? برای حل چند سوال جدید آماده هستی ¿

⏳ لطفا درس مورد نظر را انتخاب کنید :"""

choose_unit = """✅ شما درس *{}* را انتخاب کرده‌اید.

💯 درسیار به *{}* سوال در این درس دسترسی دارد.

⏳ لطفا فصل مورد نظر را انتخاب کنید: """

show_answer = "نمایش پاسخ 👀"

answer_text = """✅ شما درخواست نمایش پاسخ را کرده‌اید.

⁉️ سوال
{}

🙋‍♂️ پاسخ
{}"""

invite_text = """🙋‍♂️ *{}* شما را به بات هوشمند کمک درسیِ *درسیار* دعوت می‌کند

⁉️ دسترسی به سوالات درسی در هر پایه و مبحثی
🤖 تصحیح پاسخ شما به وسیله هوش مصنوعی
📝 ساخت آزمون به صورت فایل pdf

🔗 [لینک ورود به درسیار](https://ble.ir/darsyarbot?start={})

🎓 درسیار | بات هوشمند کمک درسی در بله
@darsyarbot"""

hint = "گرفتن راهنمایی از هوش مصنوعی 💡"

show_hint = """✅ شما درخواست گرفتن راهنمایی از هوش مصنوعی را کرده‌اید.

⁉️ سوال
{}

💡 راهنمایی
{}"""

invite_text2 = "🎁 پیام دعوت زیر رو برای دوستات بفرست و ۱۰۰۱ امتیاز به ازای هر نفری که از لینک دعوتت عضو بشه جایزه بگیر 👇"

guide = """📖 *راهنما* 

⁉️ سوال جدید: به کمک این قابلیت به سوالات درسی در هر پایه و مبحثی دسترسی کامل داری!
⚡ [سوال جدید](send:⁉️ سوال جدید) یا /question

📝 آزمون جدید: به کمک این قابلیت میتونی یک آزمون به صورت فایل pdf بسازی!
⚡ [ساخت آزمون](send:📝 آزمون جدید) یا /test

⚠️ راستی همیشه میتونی در مِنوی ربات هم به این قابلیت ها دسترسی داشته باشی! ممکنه این منو برات بسته باشه، میتونی اون رو از بقل کیبوردت باز کنی!"""

next_question = "سوال بعدی ⏭️"

wait = "⏳ لطفا منتظر بمانید. ⏳"
question = """✅ شما فصل *{}* را انتخاب کرده‌اید.

⁉️ سوال
*{}*

⚠️ در صورت وجود مشکل در صورت سوال، لطفا به [پشتیبانی](send:☎️ ارتباط با ما) اطلاع دهید (در صورت خبری بودن صورت سوال، احتمالا سوال درست یا نادرست است).

💬 برای استفاده از قابلیت هوش مصنوعی، اول گزینه را از منوی زیر انتخاب کنید و سپس پاسختان را ارسال کنید.

⬅️ برای ادامه، یکی از گزینه‌های زیر را انتخاب کنید:"""

show_help = "نمایش منو 📋"

help = "📋 لطفا برای دسترسی به قابلیت‌های بات درسیار، منوی زیر را استفاده کنید."

ai_answer = """💯 نمره پاسخ شما: *{}* از ۵

💬 توضیح هوش مصنوعی: {}

✅ پاسخ صحیح: 
{}
"""

check_answer = "چک کردن پاسخ با هوش مصنوعی 🤖"

send_answer = """✅ شما گزینه‌ی *چک کردن پاسخ با هوش مصنوعی* را انتخاب کرده‌اید.

⏳ لطفا پاسخ خود را به سوال فوق ارسال کنید:

📝 کاربر محترم لطفا دقت کنید که در هنگام انتظار بات برای پاسخ شما، هر ورودی به نشانه‌ی پاسخ بوده و قابلیت‌های دیگر بات تا زمانی که پاسخ را ارسال کنید غیرفعال می‌شود."""

score = """💯 شما تا الان *{}* امتیاز به دست آورده‌اید.

🏅 شما نفر *{}* ام بین تمام کاربران درسیار هستید.

📝 توجه کنید که کسب امتیاز فقط از طریق حل سوالاتی که تا به حال حل نکرده‌اید اتفاق میفتد و امتیاز کسب شده بر اساس نمره‌ی تعلق گرفته به شما از طرف هوش مصنوعی است."""

test_caption = """📄 آزمون *{}*
🏛️ درس: *{}*
📌 مبحث: *{}*

🎓 درسیار | بات هوشمند کمک درسی در بله
@darsyarbot"""
making_pdf = "در حال ساخت آزمون"
leaderboard = """```[🏆🏅مشاهده جدول🏅🏆]🏅 جدول مسابقات 🏅
{}```
📊 برای دسترسی به جدول امتیاز های {} نفر برتر این هفته درسیار کلیک کنید.

🏅کم کم منتظر جوایز برای نفرات برتر باشید...

🎓 درسیار | بات هوشمند کمک درسی در بله
@darsyarbot"""

class MenuStrings():
    show_score = "💯 نمایش امتیاز"
    new_question="⁉️ سوال جدید"
    new_test = "📝 آزمون جدید"
    change_grade="⚙️ تغییر پایه تحصیلی"
    support="☎️ ارتباط با ما"
    invite = "📮 دعوت دوستان"