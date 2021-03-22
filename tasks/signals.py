from django.db.models.signals import m2m_changed, post_delete, pre_delete, post_save, pre_save
from django.dispatch import receiver
from tasks.models import TodoItem, Category, PriorityCount
from collections import Counter


@receiver(m2m_changed, sender=TodoItem.category.through)
def task_cats_added(sender, instance, action, model, **kwargs):
    if action != "pre_add" and action != "post_add":
        return
    for cat in instance.category.all():
        slug = cat.slug
        todos_count = cat.todos_count
        if action == "pre_add":
            todos_count -= 1
            Category.objects.filter(slug=slug).update(todos_count=todos_count)
        elif action == "post_add":
            todos_count += 1
            Category.objects.filter(slug=slug).update(todos_count=todos_count)


@receiver(m2m_changed, sender=TodoItem.category.through)
def task_cats_removed(sender, instance, action, model, **kwargs):
    if action != "post_remove":
        return

    TODOS_COUNT_DEFAULT = 0

    cat_counter = Counter()
    for t in TodoItem.objects.all():
        for cat in t.category.all():
            cat_counter[cat.slug] += 1

    check_categories = Category.objects.all()

    for category in check_categories:
        todos_count = category.todos_count 
        if cat_counter[category.slug]:
            if todos_count != cat_counter[category.slug]:
                todos_count -= 1
            Category.objects.filter(slug=category.slug).update(todos_count=todos_count)
        else:
            Category.objects.filter(slug=category.slug).update(todos_count=TODOS_COUNT_DEFAULT)
        

@receiver(post_save, sender=TodoItem)
def check_change_priorities(sender, instance, **kwargs):
    id = instance.priority
    title = instance.get_priority_display()
    if instance.priority != instance.was_priority:
        if instance.was_priority != 0:
            was_priority = PriorityCount.objects.get(id= instance.was_priority)
            priority_count = was_priority.count
            priority_count -= 1
            PriorityCount.objects.filter(id=instance.was_priority).update(count=priority_count)
        priority, create = PriorityCount.objects.get_or_create(id= id, title=title)
        count = priority.count
        count += 1
        PriorityCount.objects.filter(id=priority.id).update(count=count)
        TodoItem.objects.filter(pk=instance.pk).update(was_priority=instance.priority)

    return


@receiver(pre_delete, sender=TodoItem)
def delete_count_of_priorities(sender, instance, **kwargs):
    id = instance.priority
    priority = PriorityCount.objects.get(id=id)
    count = priority.count
    count -= 1
    PriorityCount.objects.filter(id=id).update(count=count)


@receiver(pre_delete, sender=TodoItem)
def task_deleted(sender, instance, *args, **kwargs):
    categories = Category.objects.all()
    for category in categories:
        category.todoitem_set.remove(instance)