from typing import List, Dict, Any
from xuepy.client.api.base import BaseAPI


class Interaction(BaseAPI):
    def _update_refer(self, question_id):
        refer = {"Referer": self.baseurl + f"app/exercise/{question_id}"}
        self._session.headers.update(refer)

    def comments(self, question_id_or_chapter_path):
        """获取评论"""
        if type(question_id_or_chapter_path) == int:
            _type = f"questions"
        elif type(question_id_or_chapter_path) == str:
            _type = f"posts"
        api = (
            self.baseurl
            + f"api/{_type}/{question_id_or_chapter_path}/comments?limit=10&offset=0&order_by=created_at_desc"
        )
        return self._get(api).get("comments") or []

    def hint(self, question_id, comment_id):
        """有用的提示"""
        self._update_refer()
        api = self.baseurl + f"api/comment/tags/hint/{question_id}"
        return self._post(api, {"comment_id": comment_id})

    def solution(self, question_id, comment_id):
        """好解答"""
        self._update_refer()
        api = self.baseurl + f"api/comment/tags/solution/{question_id}"
        return self._post(api, {"comment_id": comment_id})

    def upvote(self, question_id, comment_id):
        """点赞"""
        self._update_refer()
        api = self.baseurl + f"api/comments/{comment_id}/up_vote"
        return self._post(api, {"object_type": "comment"})

    def reply(self, question_id, comment_id, content):
        """回复某条评论"""
        self._update_refer()
        api = self.baseurl + "api/comment"
        data = {
            "content": content,
            "object_id": question_id,
            "object_type": "questions",
            "thread_id": comment_id,
        }
        return self._post(api, data)
