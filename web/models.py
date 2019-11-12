from django.db import models

from ckeditor.fields import RichTextField
# Create your models here.


class Tag(models.Model):
    tag_type_choices = ((0, "用户注册标签"), (1, "文章标签"),)
    tag_type = models.SmallIntegerField(default=0)
    name = RichTextField()
    order = models.SmallIntegerField(verbose_name="用于排序字段", default=0)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "api_tag"


class Article(models.Model):
    title = models.CharField(max_length=32)
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE)


class Comment(models.Model):
    """
    通用的评论表
    """
    # content_type = models.ForeignKey(ContentType, blank=True, null=True, verbose_name="类型", on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField(blank=True, null=True)
    # content_object = GenericForeignKey('content_type', 'object_id')
    p_node = models.ForeignKey("self", null=True, verbose_name="父级评论", on_delete=models.CASCADE)
    content = models.TextField(max_length=1024)
    # account = fields.ForeignKeyField("models.Account", verbose_name="会员名")
    comment_type_choices = ((0, '评论'), (1, '讲师回复'), (2, '官方客服'))
    comment_type = models.SmallIntegerField(choices=comment_type_choices, default=0, verbose_name="评论类型")
    date = models.DateTimeField(auto_now_add=True)

