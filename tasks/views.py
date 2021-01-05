from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from .models import Task, Comment
from .serilizers import TaskSerializer, CommentSerializer, FileSerializer
import datetime
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.parsers import FileUploadParser
from rest_framework import status
class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return

class BaseView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

class LoginView(BaseView):
    def post(self, request):
        data=request.data.get('data')
        user = authenticate(request, username=data["name"], password=data["pasw"])
        if user is not None:
            login(request, user)
            return Response({'Вход выполнен'})
        else:
            return Response({'Неверные данные'})

class LogoutView(BaseView):
    def post(self, request):
        logout(request)
        return Response({'Выход выполнен'})

class TaskView(BaseView):
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response({"tasks": serializer.data})

    def post(self, request):
        task = request.data.get('task')
        task["customer_id"]=request.user.pk
        serializer = TaskSerializer(data=task)
        if serializer.is_valid(raise_exception=True):
            task_saved = serializer.save()
        return Response({"Задача '{}' создана".format(task_saved.name)})

    def put(self, request, pk):
        saved_task = get_object_or_404(Task.objects.all(), pk=pk)
        if saved_task.executor==None and request.user.pk==saved_task.author.customer.pk:
            data = request.data.get('task')
            serializer = TaskSerializer(instance=saved_task, data=data,partial=True)
            if serializer.is_valid(raise_exception=True):
                task_saved = serializer.save()
            return Response({"Задача '{}' отредактирована".format(task_saved.name)})
        else:
            return Response({"Не удалось отредактироват задачу"})


class CommentView(BaseView):
    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response({"comments": serializer.data})

    def post(self, request):
        comment = request.data.get('comment')
        comment["author_id"]=request.user.pk
        serializer = CommentSerializer(data=comment)
        serializer.customer_id=request.user.pk
        if serializer.is_valid(raise_exception=True):
            comment_saved = serializer.save()
        return Response({"Комментарий '{}' создан".format(comment_saved)})

    def put(self,request, pk):
        saved_comment = get_object_or_404(Comment.objects.all(), pk=pk)
        now = timezone.now()
        if now-saved_comment.created<=datetime.timedelta(minutes=30) and request.user.pk==saved_comment.author.id:
            data = request.data.get('comment')
            serializer = CommentSerializer(instance=saved_comment, data=data,partial=True)
            if serializer.is_valid(raise_exception=True):
                comment_saved = serializer.save()
            return Response({"Комментарий '{}' отредактирован".format(comment_saved)})
        else:
            return Response({"Не удалось отредактироват комментарий"})



class FileUploadView(BaseView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        str_file=str(request.data["file"])
        str_file=str_file.split(".")
        data=request.data
        data["name"]=str_file[0]
        data["type"] = str_file[1]
        if  (not "comment" in data.keys()) and (not "task" in data.keys()):
            return Response({"Не указана задача или коммент"})
        if "comment" in data.keys():
            comment = get_object_or_404(Comment.objects.all(), pk=data["comment"])
            now = timezone.now()
            if now-comment.created>=datetime.timedelta(minutes=30):
                return Response({"Слишком старый comment"})
            if comment.author.pk!=request.user.pk:
                return Response({"Комментарий другого пользователя"})

        if "task" in data.keys():
            task = get_object_or_404(Task.objects.all(), pk=data["task"])
            if task.customer.pk!=request.user.pk:
                return Response({
                    "Задача другого пользователя"})

        file_serializer = FileSerializer(data=data)
        if file_serializer.is_valid():
            saved_file=file_serializer.save()
            return Response({"Файл {} добавлен".format(saved_file)})
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDeleteView(BaseView):
    def post(self, request, pk):
        comment = get_object_or_404(Comment.objects.all(), pk=pk)
        now = timezone.now()
        if request.user.pk==comment.author.pk and now-comment.created<=datetime.timedelta(minutes=30):
            comment.delete()
            return Response({"Комментарий `{}` удалён".format(pk)}, status=204)
        else:
            return Response({"Вы не можете удалить коммент"})

class TakeTaskView(BaseView):
    def post(self, request, pk):
        saved_task = get_object_or_404(Task.objects.all(), pk=pk)
        if saved_task.executor==None:
            saved_task.executor=request.user
            saved_task.save()
            return Response({"Задача {} взята {}".format(saved_task,request.user)})
        else:
            return Response({"Задача {} занята".format(saved_task)})

class CloseTaskView(BaseView):
    def post(self, request, pk):
        saved_task = get_object_or_404(Task.objects.all(), pk=pk)
        if not "comment" in request.data:
            return Response({"Отсутствует финальный комментарий"})
        if saved_task.executor!=None and saved_task.executor==request.user and saved_task.completed==None:
            saved_task.completed=timezone.now()
            saved_task.save()
            comment = request.data.get('comment')
            comment["author_id"] = request.user.pk
            comment["task_id"]=saved_task.pk
            serializer = CommentSerializer(data=comment)
            serializer.customer_id = request.user.pk
            if serializer.is_valid(raise_exception=True):
                comment_saved = serializer.save()
            return Response({"Задача '{}' закрыта".format(saved_task)})

class AnswerCommentView(BaseView):
    def post(self, request, pk):
        comment = get_object_or_404(Comment.objects.all(), pk=pk)
        if comment.task.executor==request.user:
            comment.answer=request.data["answer"]
            comment.save()
            return Response({"Ответ отправлен"})
        else:
            return Response({"Ответ не может быть отправлен"})