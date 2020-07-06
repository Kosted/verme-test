"""
Copyright 2020 ООО «Верме»
"""

from django.db import models
from django.db.models.expressions import RawSQL
from django.db.models import Q
from django.utils.functional import cached_property


class OrganizationQuerySet(models.QuerySet):
    def tree_downwards(self, root_org_id):
        """
        Возвращает корневую организацию с запрашиваемым root_org_id и всех её детей любого уровня вложенности
        TODO: Написать фильтр с помощью ORM или RawSQL запроса или функций Python

        :type root_org_id: int
        """

        search_org = self.filter(id=root_org_id)
        res = search_org
        while search_org:
            new = self.none()
            for org in search_org:
                new_child = self.filter(parent=org.id)
                res = res | new_child
                new = new | new_child
            search_org = new


        return res

    # def __repr__(self):
    #     return self.id



    def tree_upwards(self, child_org_id):
        """
        Возвращает корневую организацию с запрашиваемым child_org_id и всех её родителей любого уровня вложенности
        TODO: Написать фильтр с помощью ORM или RawSQL запроса или функций Python

        :type child_org_id: int
        """

        # search_org = self.filter(id=child_org_id)
        # res = search_org
        # while search_org:
        #
        #     for org in search_org:
        #         if org.parent:
        #             new_parent = self.filter(id=org.parent.id)
        #             res = res | new_parent
        #             new = new_parent
        #     search_org = new
        #     new = self.none()

        search_org = self.filter(id=child_org_id)
        res = search_org
        while search_org:

            if search_org.first().parent:
                next_parent = self.filter(id=search_org.first().parent.id)
                res = res | next_parent
            else:
                next_parent = self.none()
            search_org = next_parent

        return res


class Organization(models.Model):
    """ Организаци """

    objects = OrganizationQuerySet.as_manager()

    name = models.CharField(max_length=1000, blank=False, null=False, verbose_name="Название")
    code = models.CharField(max_length=1000, blank=False, null=False, unique=True, verbose_name="Код")
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.PROTECT, verbose_name="Вышестоящая организация",
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Организация"
        verbose_name = "Организации"

    def parents(self):
        """
        Возвращает всех родителей любого уровня вложенности
        TODO: Написать метод, используя ORM и .tree_upwards()

        :rtype: django.db.models.QuerySet
        """
        # return self.objects.tree_upwards(self.id)
        return OrganizationQuerySet(self).tree_upwards(self.id).exclude(id=self.id)

    def children(self):
        """
        Возвращает всех детей любого уровня вложенности
        TODO: Написать метод, используя ORM и .tree_downwards()

        :rtype: django.db.models.QuerySet
        """

        return OrganizationQuerySet(self).tree_downwards(self.id).exclude(id=self.id)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
