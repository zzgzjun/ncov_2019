from django.db import models

# Create your models here.


class History(models.Model):
    date = models.DateField(verbose_name='日期', db_column='date')
    confirm=models.IntegerField(verbose_name='累计确诊',db_column='confirm',null=True,blank=True)
    confirm_add=models.IntegerField(verbose_name='新增确诊',db_column='confirm_add',null=True,blank=True)
    suspect=models.IntegerField(verbose_name='剩余疑似',db_column='suspect',null=True,blank=True)
    suspect_add=models.IntegerField(verbose_name='新增疑似',db_column='suspect_add',null=True,blank=True)
    dead=models.IntegerField(verbose_name='累计死亡',db_column='dead',null=True,blank=True)
    dead_add=models.IntegerField(verbose_name='新增死亡',db_column='dead_add',null=True,blank=True)
    heal=models.IntegerField(verbose_name='累计治愈',db_column='heal',null=True,blank=True)
    heal_add=models.IntegerField(verbose_name='新增治愈',db_column='heal_add',null=True,blank=True)

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = '历史数据'
        verbose_name_plural = verbose_name
        db_table = 'history'


class Detail(models.Model):
    date = models.DateTimeField(verbose_name='更新时间', db_column='date')
    province=models.CharField(max_length=15,verbose_name="省",db_column='province')
    city=models.CharField(max_length=15,verbose_name="市",db_column='city')
    nowConfirm = models.IntegerField(verbose_name='现有确诊', db_column='nowConfirm', null=True, blank=True)
    confirm=models.IntegerField(verbose_name='累计确诊',db_column='confirm',null=True,blank=True)
    suspect=models.IntegerField(verbose_name='新增确诊',db_column='suspect',null=True,blank=True)
    dead=models.IntegerField(verbose_name='累计死亡',db_column='dead',null=True,blank=True)
    heal=models.IntegerField(verbose_name='累计治愈',db_column='heal',null=True,blank=True)

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = '详细数据'
        verbose_name_plural = verbose_name
        db_table = 'detail'


class HotSearch(models.Model):
    date = models.DateTimeField(verbose_name='更新时间', db_column='date')
    name=models.CharField(max_length=30,verbose_name="热搜内容",db_column='name')
    value=models.IntegerField(verbose_name='热搜指数',db_column='value')

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = '热搜数据'
        verbose_name_plural = verbose_name
        db_table = 'hotsearch'

