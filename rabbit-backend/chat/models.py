from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


def deserialize_user(user):
    """JSON으로 인스턴스 deserialize"""
    return {
        'id': user.id, 'username': user.username, 'email': user.email,
        'first_name': user.first_name, 'last_name': user.last_name
    }


class TrackableDateModel(models.Model):
    """생성 시간, 업데이트 시간을 위한 추상 모델"""

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def _generate_unique_uri():
    """채팅 세션을 위한 유니크한 uri 생성"""
    return str(uuid4()).replace('-', '')[:15]


class ChatSession(TrackableDateModel):
    """채팅 세션 모델, 생성된 uri에서 15자리를 사용"""

    members = models.ManyToManyField(User, through='ChatSessionMember')
    uri = models.URLField(default=_generate_unique_uri)


class ChatSessionMessage(TrackableDateModel):
    """채팅 세션에 해당하는 메세지 모델"""

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    chat_session = models.ForeignKey(
        ChatSession, related_name='messages', on_delete=models.PROTECT
    )
    content = models.TextField(max_length=2000)

    def to_json(self):
        """JSON으로 메세지 deserialize"""
        return {'user': deserialize_user(self.user), 'message': self.content}


class ChatSessionMember(TrackableDateModel):
    """채팅 세션에 있는 유저 정보"""

    chat_session = models.ForeignKey(ChatSession, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
