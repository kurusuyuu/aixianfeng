from datetime import datetime

from django.utils.deprecation import MiddlewareMixin

from shop.models import UserTicket


class login(MiddlewareMixin):

    def process_request(self,request):

        ticket = request.COOKIES.get('ticket')

        if not ticket:
            return None

        userticket = UserTicket.objects.filter(ticket=ticket)
        if userticket:
            # 判断令牌是否有效，无效则删除
            out_time = userticket[0].out_time.replace(tzinfo=None)
            now_time = datetime.utcnow()

            if out_time >now_time:
                # 没有失效
                request.user = userticket[0].user
            else:
                userticket.delete()
