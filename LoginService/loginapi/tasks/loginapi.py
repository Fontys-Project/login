from loginapi.extensions import celery

TASK_CUSTOMER_CREATE_USER = "loginapi.tasks.loginapi.create_user"


def invoke_create_user(username):
    data = {
        "username": username
    }

    invoke_user = celery.signature(TASK_CUSTOMER_CREATE_USER, kwargs=data)

    return invoke_user.delay()


@celery.task
def delete_user(*args, **kwargs):
    # TODO implement, this will come from customer service
    return "OK"
