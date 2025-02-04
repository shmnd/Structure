from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
class SendEmial:
    def __init__(self,*args, **kwargs):
        pass

    def sendTemplateMail(self,subject,context,template,email_host,user_email):
        sending_status = False

        try:
            context=context
            html_content = render_to_string(str(template),context={'context':context})
            text_content = strip_tags(html_content)
            send_e = EmailMultiAlternatives(str(subject),text_content,email_host,[str(user_email)])
            send_e.attach_alternative(html_content,"text/html")

            send_e.send()
            sending_status = True
            print('Email sending succesfull')
        except Exception as e:
            print('Error while sendin Email',e)
        return sending_status

