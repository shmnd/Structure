from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
class SendEmail:

    def sendTemplateMail(self,subject,context,template,email_host,user_email):
        sending_status = False

        try:
            context=context
            print(context,'contexttttttttttttttttt')
            # html_content = render_to_string(str(template),context={'context':context})
            html_content = render_to_string(template, context=context)
            text_content = strip_tags(html_content)
            send_e = EmailMultiAlternatives(
                subject=str(subject),
                body=text_content,
                from_email=email_host,
                to=[str(user_email)]
            )
            send_e.attach_alternative(html_content,"text/html")

            send_e.send()
            sending_status = True
            print('Email sending succesfull')
        except Exception as e:
            print('Error while sending Email',e)
        return sending_status

