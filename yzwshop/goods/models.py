from django.db import models


# Create your models here.
# 商品分类
# 模型类 对应了一张表
class GoodsCategory(models.Model):
    # 名称，样式，图片
    # 字符串类型必须定义max_length
    cag_name = models.CharField(max_length=30)
    cag_css = models.CharField(max_length=20)
    # 路径
    cag_img = models.ImageField(upload_to='cag')


class GoodsInfo(models.Model):
    goods_name=models.CharField(max_length=100)
    goods_price=models.IntegerField(default=0)
    goods_desc=models.CharField(max_length=2000)
    goods_img=models.ImageField(upload_to='goods')
    goods_cag=models.ForeignKey('GoodsCategory', on_delete=models.CASCADE)