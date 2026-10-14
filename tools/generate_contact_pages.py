#!/usr/bin/env python3
"""Generate the per-locale contact pages (<locale folder>/contact.html).

Run from anywhere:  python3 tools/generate_contact_pages.py [folder ...]
With no arguments every locale in LOCALES is generated.

To add a locale: add a LANGUAGES entry if its language isn't there yet, then add
a LOCALES entry. Navigation labels match each locale's index.html.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# language key -> (html lang, title, sentence, link text)
LANGUAGES = {
    "en": ("en", "Contact Us for Support",
           "Support for 359 North Apps is available by E-mail.",
           "Click Here to E-mail Support"),
    "de": ("de", "Kontaktieren Sie uns für Support",
           "Support für 359 North Apps ist per E-Mail verfügbar.",
           "Klicken Sie hier, um den Support per E-Mail zu kontaktieren"),
    "fr": ("fr", "Contactez-nous pour obtenir de l'aide",
           "L'assistance pour 359 North Apps est disponible par e-mail.",
           "Cliquez ici pour envoyer un e-mail à l'assistance"),
    "ja": ("ja", "サポートについてはお問い合わせください",
           "359 North Apps のサポートは電子メールで利用できます。",
           "サポートを電子メールで送信するにはここをクリック"),
    "es": ("es", "Contáctenos para soporte",
           "El soporte para 359 North Apps está disponible por correo electrónico.",
           "Haga clic aquí para enviar un correo electrónico a soporte"),
    "it": ("it", "Contattaci per ricevere assistenza",
           "Il supporto per 359 North Apps è disponibile tramite e-mail.",
           "Fai clic qui per inviare un'e-mail all'assistenza"),
    "sv": ("sv", "Kontakta oss för support",
           "Support för 359 North Apps är tillgängligt via e-post.",
           "Klicka här för att skicka e-post till support"),
    "pl": ("pl", "Skontaktuj się z nami w celu uzyskania pomocy",
           "Wsparcie dla 359 North Apps jest dostępne przez e-mail.",
           "Kliknij tutaj, aby uzyskać pomoc przez e-mail"),
    "ru": ("ru", "Свяжитесь с нами для получения поддержки",
           "Поддержка 359 North Apps доступна по электронной почте.",
           "Нажмите здесь, чтобы написать в службу поддержки по электронной почте"),
    "uk": ("uk", "Зв’яжіться з нами, щоб отримати підтримку",
           "Підтримка 359 North Apps доступна електронною поштою.",
           "Натисніть тут, щоб надіслати підтримку електронною поштою"),
    "da": ("da", "Kontakt os for support",
           "Support til 359 North Apps er tilgængelig via e-mail.",
           "Klik her for at sende en e-mail til support"),
    "nl": ("nl", "Neem contact met ons op voor ondersteuning",
           "Ondersteuning voor 359 North Apps is beschikbaar via e-mail.",
           "Klik hier om de ondersteuning te e-mailen"),
    "nb": ("nb", "Kontakt oss for støtte",
           "Støtte for 359 North Apps er tilgjengelig via e-post.",
           "Klikk her for å sende e-post til støtte"),
    "pt-PT": ("pt-PT", "Contacte-nos para obter suporte",
              "O suporte para 359 North Apps está disponível por e-mail.",
              "Clique aqui para enviar um e-mail ao suporte"),
    "pt-BR": ("pt-BR", "Entre em contato conosco para suporte",
              "O suporte para 359 North Apps está disponível por e-mail.",
              "Clique aqui para enviar um e-mail ao suporte"),
    "zh-Hans": ("zh", "联系我们寻求支持",
                "可通过电子邮件获得对 359 North Apps 的支持。",
                "单击此处发送电子邮件支持"),
    "zh-Hant": ("zh-Hant", "聯絡我們以取得支援",
                "359 North Apps 的支援可透過電子郵件取得。",
                "按一下此處以電子郵件聯絡支援"),
    "ko": ("ko", "지원이 필요하시면 문의해 주세요",
           "359 North Apps에 대한 지원은 이메일로 받으실 수 있습니다.",
           "지원팀에 이메일을 보내려면 여기를 클릭하세요"),
}

# folder -> page language, nav labels (home, contact, privacy), flag, and the
# language blocks to show. A block is (language key, flag shown before its title).
LOCALES = {
    "au": dict(lang="en", home="Home", contact="Contact", privacy="Privacy",
           flag="🇦🇺", blocks=[("en", "🇦🇺")]),
    "br": dict(lang="pt-BR", home="Início", contact="Contato", privacy="Privacidade",
           flag="🇧🇷", blocks=[("pt-BR", "🇧🇷")]),
    "ca": dict(lang="en", home="Home", contact="Contact", privacy="Privacy",
           flag="🇨🇦", blocks=[("en", "🇨🇦"), ("fr", "🇨🇦")]),
    "cn": dict(lang="zh", home="首页", contact="联系方式", privacy="隐私",
           flag="🇨🇳", blocks=[("zh-Hans", "🇨🇳")]),
    "de": dict(lang="de", home="Heim", contact="Kontakt", privacy="Privatsphäre",
           flag="🇩🇪", blocks=[("de", "🇩🇪")]),
    "dk": dict(lang="da", home="Hjem", contact="Kontakt", privacy="Privatliv",
           flag="🇩🇰", blocks=[("da", "🇩🇰")]),
    "es": dict(lang="es", home="Inicio", contact="Contacto", privacy="Privacidad",
           flag="🇪🇸", blocks=[("es", "🇪🇸")]),
    "fr": dict(lang="fr", home="Accueil", contact="Contact", privacy="Confidentialité",
           flag="🇫🇷", blocks=[("fr", "🇫🇷")]),
    "fr-ca": dict(lang="fr-CA", home="Accueil", contact="Contact", privacy="Confidentialité",
              flag="🇨🇦", blocks=[("fr", "🇨🇦"), ("en", "🇨🇦")]),
    "gb": dict(lang="en", home="Home", contact="Contact", privacy="Privacy",
           flag="🇬🇧", blocks=[("en", "🇬🇧")]),
    "it": dict(lang="it", home="Inizio", contact="Contatta", privacy="Privacy",
           flag="🇮🇹", blocks=[("it", "🇮🇹")]),
    "jp": dict(lang="ja", home="ホーム", contact="連絡先", privacy="プライバシー",
           flag="🇯🇵", blocks=[("ja", "🇯🇵")]),
    "kr": dict(lang="ko", home="홈", contact="연락처", privacy="개인정보",
           flag="🇰🇷", blocks=[("ko", "🇰🇷")]),
    "nl": dict(lang="nl", home="Home", contact="Contact", privacy="Privacy",
           flag="🇳🇱", blocks=[("nl", "🇳🇱")]),
    "no": dict(lang="nb", home="Hjem", contact="Kontakt", privacy="Personvern",
           flag="🇳🇴", blocks=[("nb", "🇳🇴")]),
    "pl": dict(lang="pl", home="Start", contact="Kontakt", privacy="Prywatność",
           flag="🇵🇱", blocks=[("pl", "🇵🇱")]),
    "pt": dict(lang="pt-PT", home="Início", contact="Contacto", privacy="Privacidade",
           flag="🇵🇹", blocks=[("pt-PT", "🇵🇹")]),
    "ru": dict(lang="ru", home="Главная", contact="Контакт", privacy="Конфиденциальность",
           flag="🇷🇺", blocks=[("ru", "🇷🇺")]),
    "se": dict(lang="sv", home="Hem", contact="Kontakt", privacy="Sekretess",
           flag="🇸🇪", blocks=[("sv", "🇸🇪")]),
    "tw": dict(lang="zh-Hant", home="首頁", contact="聯絡方式", privacy="隱私",
           flag="🇹🇼", blocks=[("zh-Hant", "🇹🇼")]),
    "ua": dict(lang="uk", home="Домашня сторінка", contact="Контакти", privacy="Конфіденційність",
           flag="🇺🇦", blocks=[("uk", "🇺🇦")]),
}

# hreflang -> folder ("" is the site root, i.e. /contact for the US page)
ALTERNATES = [
    ("en-AU", "au"), ("en-CA", "ca"), ("en-GB", "gb"), ("en-US", ""), ("fr-CA", "fr-ca"),
    ("de", "de"), ("fr", "fr"), ("es", "es"), ("it", "it"), ("pl", "pl"), ("sv", "se"),
    ("ru", "ru"), ("uk", "ua"), ("zh", "cn"), ("ja", "jp"), ("ko", "kr"), ("zh-Hant", "tw"),
    ("da", "dk"), ("nl", "nl"), ("nb", "no"), ("pt-BR", "br"), ("pt-PT", "pt"),
]

SUPPORT_EMAIL = "support@359north.com"

PAGE = """<!doctype html>
<html lang="{lang}">

	<head>
		<meta charset="utf-8"/>

		<title>359 North - {contact}</title>
		<meta name="viewport" content="width=device-width, initial-scale=1"/>

		<meta property="og:title" content="359 North"/>
		<meta property="og:site_name" content="359 North"/>
		<meta property="og:image" content="https://359north.com/images/359North.jpg"/>

		<meta property="twitter:card" content="summary"/>
		<meta property="twitter:site" content="@stevemykytyn"/>
		<meta property="twitter:title" content="359 North"/>

		<link rel="alternate" hreflang="x-default" href="https://359north.com/contact"/>
{alternates}

		<link rel="canonical" href="https://359north.com/{folder}/contact"/>

		<link rel="stylesheet" href="../stylesheets/style359.css"/>
		<style>
			.contact-text {{ width: 350px; max-width: 100%; float: left; padding-top: 10px; }}
			.contact-icons {{ width: 230px; float: right; }}
		</style>
	</head>

	<body style="background-image: linear-gradient(#FFFFFF, #D0E9FD); background-repeat: no-repeat; background-size: cover;">

		<div class="content">
			<div class="navigationwrapper">
				<span class='navigation-left'><a href="/{folder}/">{flag} {home}</a> | <a href="/{folder}/contact">{contact}</a></span>
				<span class='navigation-right'> <a href="/privacy-policy">{privacy}</a></span>
			</div>
			<div class="app">
				<div class="appbody contact-text">
{blocks}
				</div>

				<div class="appbody contact-icons">
					<center>
					<h4>MAX Daylight</h4>
					<img class="appicon-small" src="../icons/AppIcon-256-MAX-Daylight.png"/>
					<br/><br/>
					<h4>Mirror Day</h4>
					<img class="appicon-small" src="../icons/AppIcon-1024-MirrorDay.png"/>
					<br/><br/>
					<h4>Live Long!</h4>
					<img class="appicon-small" src="../icons/AppIcon-1024-LiveLong.png"/>
					</center>
				</div>
			</div>
		</div>

		<!-- Cloudflare Web Analytics --><script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{"token": "2909cbc5b7904a5e8185d6438968ff70"}}'></script><!-- End Cloudflare Web Analytics -->
	</body>

</html>
"""

BLOCK = """					<div lang="{lang}">
						<h3>{flag} {title}</h3>
						<h4>{sentence}</h4>
						<p><a href="mailto:{email}">{link}</a></p>
					</div>
"""


def alternates():
    return "\n".join(
        f'\t\t<link rel="alternate" hreflang="{code}" href="https://359north.com/{path + "/" if path else ""}contact"/>'
        for code, path in ALTERNATES)


def render(folder, locale):
    blocks = []
    for key, flag in locale["blocks"]:
        lang, title, sentence, link = LANGUAGES[key]
        blocks.append(BLOCK.format(lang=lang, flag=flag, title=title, sentence=sentence,
                                   link=link, email=SUPPORT_EMAIL))
    return PAGE.format(folder=folder, lang=locale["lang"], contact=locale["contact"],
                       home=locale["home"], privacy=locale["privacy"], flag=locale["flag"],
                       blocks="\n".join(blocks).rstrip("\n"), alternates=alternates())


def main(folders):
    for folder in folders or LOCALES:
        path = ROOT / folder / "contact.html"
        path.write_text(render(folder, LOCALES[folder]), encoding="utf-8")
        print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main(sys.argv[1:])
